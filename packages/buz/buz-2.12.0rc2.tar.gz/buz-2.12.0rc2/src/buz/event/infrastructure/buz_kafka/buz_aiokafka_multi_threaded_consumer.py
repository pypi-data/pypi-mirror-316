import asyncio
import traceback
from asyncio import Future, create_task, gather, Semaphore, Event as AsyncIOEvent, sleep
from datetime import timedelta, datetime
from logging import Logger
from queue import Queue
from threading import Thread
from typing import Optional, Sequence, Type, TypeVar

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

from buz.event import Event, Subscriber
from buz.event.async_consumer import AsyncConsumer
from buz.event.domain.queue.queue_repository import QueueRepository
from buz.event.infrastructure.buz_kafka.consume_strategy.consume_strategy import KafkaConsumeStrategy
from buz.event.infrastructure.buz_kafka.consume_strategy.kafka_on_fail_strategy import KafkaOnFailStrategy
from buz.event.infrastructure.buz_kafka.in_memory_queue_repository import InMemoryQueueRepository
from buz.event.infrastructure.buz_kafka.kafka_event_subscriber_executor import KafkaEventSubscriberExecutor
from buz.event.middleware.consume_middleware import ConsumeMiddleware
from buz.event.strategies.retry.consume_retrier import ConsumeRetrier
from buz.event.strategies.retry.reject_callback import RejectCallback
from buz.kafka import (
    KafkaConnectionConfig,
    ConsumerInitialOffsetPosition,
)
from buz.kafka.domain.models.auto_create_topic_configuration import AutoCreateTopicConfiguration
from buz.kafka.domain.models.kafka_poll_record import KafkaPollRecord
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient
from buz.kafka.infrastructure.aiokafka.aiokafka_multi_threaded_consumer import AIOKafkaMultiThreadedConsumer
from buz.kafka.infrastructure.aiokafka.factories.kafka_python_multi_threaded_consumer_factory import (
    KafkaPythonMultiThreadedConsumerFactory,
)
from buz.kafka.infrastructure.deserializers.bytes_to_message_deserializer import BytesToMessageDeserializer
from buz.kafka.infrastructure.deserializers.implementations.json_bytes_to_message_deserializer import (
    JSONBytesToMessageDeserializer,
)
from buz.kafka.infrastructure.serializers.kafka_header_serializer import KafkaHeaderSerializer

T = TypeVar("T", bound=Event)

ConsumingTask = tuple[KafkaPollRecord, AIOKafkaMultiThreadedConsumer]


class BuzAIOKafkaMultiThreadedConsumer(AsyncConsumer):
    __MAX_NUMBER_OF_CONCURRENT_POLLING_TASKS = 20
    __SECONDS_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE = 1
    __SECONDS_BETWEEN_COMMITS_POLLING = 1

    __commit_task_future: Optional[Future] = None
    __execution_exception: Optional[Exception] = None

    def __init__(
        self,
        *,
        connection_config: KafkaConnectionConfig,
        kafka_admin_client: Optional[KafkaAdminClient],
        consume_strategy: KafkaConsumeStrategy,
        on_fail_strategy: KafkaOnFailStrategy,
        max_queue_size: int,
        max_records_retrieved_per_poll: int,
        queue_repository: QueueRepository[ConsumingTask],
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        subscribers: Sequence[Subscriber],
        logger: Logger,
        consumer_initial_offset_position: ConsumerInitialOffsetPosition,
        deserializers_per_subscriber: dict[Subscriber, BytesToMessageDeserializer[T]],
        consume_middlewares: Optional[list[ConsumeMiddleware]] = None,
        consume_retrier: Optional[ConsumeRetrier] = None,
        reject_callback: Optional[RejectCallback] = None,
        auto_create_topic_configuration: Optional[AutoCreateTopicConfiguration] = None,
    ):
        self.__connection_config = connection_config
        self.__consume_strategy = consume_strategy
        self.__on_fail_strategy = on_fail_strategy
        self.__queue_repository = queue_repository
        self.__commit_repository: QueueRepository[ConsumingTask] = InMemoryQueueRepository(queue=Queue())
        self.__kafka_partition_assignors = kafka_partition_assignors
        self.__subscribers = subscribers
        self.__logger = logger
        self.__consumer_initial_offset_position = consumer_initial_offset_position
        self.__deserializers_per_subscriber = deserializers_per_subscriber
        self.__max_records_retrieved_per_poll = 1
        self.__subscriber_per_consumer_mapper: dict[AIOKafkaMultiThreadedConsumer, Subscriber] = {}
        self.__executor_per_consumer_mapper: dict[AIOKafkaMultiThreadedConsumer, KafkaEventSubscriberExecutor] = {}
        self.__max_records_retrieved_per_poll = max_records_retrieved_per_poll
        self.__max_queue_size = max_queue_size
        self.__should_stop = AsyncIOEvent()
        self.__stop_commit_task = AsyncIOEvent()
        self.__stop_consumption_thread = AsyncIOEvent()
        self.__start_kafka_consumers_elapsed_time: Optional[timedelta] = None
        self.__initial_coroutines_created_elapsed_time: Optional[timedelta] = None
        self.__events_processed: int = 0
        self.__events_processed_elapsed_time: timedelta = timedelta()
        self.__polling_tasks_semaphore = Semaphore(self.__MAX_NUMBER_OF_CONCURRENT_POLLING_TASKS)
        self.__consumption_thread = Thread(target=lambda: asyncio.run(self.__consume_events_thread()))
        self.__consume_middlewares = consume_middlewares
        self.__consume_retrier = consume_retrier
        self.__reject_callback = reject_callback
        self.__kafka_admin_client = kafka_admin_client
        self.__auto_create_topic_configuration = auto_create_topic_configuration

    async def run(self) -> None:
        start_time = datetime.now()
        await self.__generate_kafka_consumers()
        self.__initial_coroutines_created_elapsed_time = datetime.now() - start_time

        start_consumption_time = datetime.now()

        self.__consumption_thread.start()
        self.__commit_task_future = create_task(self.__commit_task())
        await self.__polling_task()

        self.__events_processed_elapsed_time = datetime.now() - start_consumption_time

        await self.__perform_graceful_stop()

    async def __generate_kafka_consumers(self):
        start_time = datetime.now()
        tasks = [self.__create_kafka_consumer_for_subscriber(subscriber) for subscriber in self.__subscribers]
        await gather(*tasks)
        self.__start_kafka_consumers_elapsed_time = datetime.now() - start_time

    async def __create_kafka_consumer_for_subscriber(self, subscriber: Subscriber) -> None:
        kafka_python_consumer_factory = KafkaPythonMultiThreadedConsumerFactory(
            consumer_group=self.__consume_strategy.get_subscription_group(subscriber),
            topics=self.__consume_strategy.get_topics(subscriber),
            kafka_connection_config=self.__connection_config,
            initial_offset_position=self.__consumer_initial_offset_position,
            kafka_partition_assignors=self.__kafka_partition_assignors,
            logger=self.__logger,
            kafka_admin_client=self.__kafka_admin_client,
            auto_create_topic_configuration=self.__auto_create_topic_configuration,
        )
        kafka_consumer = kafka_python_consumer_factory.build()
        self.__subscriber_per_consumer_mapper[kafka_consumer] = subscriber

        byte_deserializer = self.__deserializers_per_subscriber.get(subscriber) or JSONBytesToMessageDeserializer(
            event_class=subscriber.handles()  # type: ignore[arg-type]
        )

        self.__executor_per_consumer_mapper[kafka_consumer] = KafkaEventSubscriberExecutor(
            logger=self.__logger,
            byte_deserializer=byte_deserializer,
            header_deserializer=KafkaHeaderSerializer(),
            on_fail_strategy=self.__on_fail_strategy,
            subscriber=subscriber,
            consume_middlewares=self.__consume_middlewares,
            consume_retrier=self.__consume_retrier,
            reject_callback=self.__reject_callback,
        )

        await kafka_consumer.init()

    async def __polling_task(self) -> None:
        try:
            while not self.__should_stop.is_set():
                if self.__queue_repository.get_size() >= self.__max_queue_size:
                    await sleep(self.__SECONDS_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)
                    continue

                raw_consuming_tasks = await gather(
                    *[
                        self.__polling_consuming_tasks(kafka_consumer=consumer)
                        for consumer, subscriber in self.__subscriber_per_consumer_mapper.items()
                    ]
                )
                poll_results = [
                    consuming_task for consuming_tasks in raw_consuming_tasks for consuming_task in consuming_tasks
                ]
                if len(poll_results) == 0:
                    await sleep(self.__SECONDS_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)

                for poll_result in poll_results:
                    self.__queue_repository.push(poll_result)

        except Exception:
            self.__logger.error(f"Polling task failed with exception: {traceback.format_exc()}")
            self.__should_stop.set()

        return

    async def __commit_task(self) -> None:
        while not self.__stop_commit_task.is_set():
            await sleep(self.__SECONDS_BETWEEN_COMMITS_POLLING)
            await self.__commit_pending_tasks()

    async def __commit_pending_tasks(self) -> None:
        while self.__commit_repository.is_empty() is False:
            commit_record, consumer = self.__commit_repository.pop()
            await consumer.commit_poll_record(commit_record)

    async def __polling_consuming_tasks(self, kafka_consumer: AIOKafkaMultiThreadedConsumer) -> list[ConsumingTask]:
        async with self.__polling_tasks_semaphore:
            results = await kafka_consumer.poll(
                number_of_messages_to_poll=self.__max_records_retrieved_per_poll,
            )
        return [(result, kafka_consumer) for result in results]

    async def __consume_events_thread(self) -> None:
        while not self.__stop_consumption_thread.is_set():
            if self.__queue_repository.is_empty():
                await sleep(self.__SECONDS_BETWEEN_POLLS_IF_THERE_ARE_TASKS_IN_THE_QUEUE)
                continue

            kafka_poll_record, consumer = self.__queue_repository.pop()
            executor = self.__executor_per_consumer_mapper[consumer]

            try:
                await executor.consume(kafka_poll_record=kafka_poll_record)
                self.__commit_repository.push((kafka_poll_record, consumer))
                self.__events_processed += 1
            except Exception as ex:
                self.__should_stop.set()
                self.__execution_exception = ex
                return

    def request_stop(self) -> None:
        self.__should_stop.set()
        self.__logger.info("Worker stop requested. Waiting for finalize the current task")

    async def __perform_graceful_stop(self) -> None:
        self.__logger.info("Stopping consuming thread....")
        await self.__manage_consumption_thread_stopping()

        self.__logger.info("Commiting pending tasks")
        await self.__manage_commiting_task_stopping()

        self.__logger.info("Stopping kafka consumers...")
        await self.__manage_kafka_consumers_stopping()

        self.__logger.info("All kafka consumers stopped")
        self.__print_statistics()

        if self.__execution_exception is not None:
            self.__logger.info("The consumer was stopped due to an error")
            raise self.__execution_exception

    async def __manage_consumption_thread_stopping(self) -> None:
        self.__stop_consumption_thread.set()
        await asyncio.to_thread(self.__consumption_thread.join)

    async def __manage_commiting_task_stopping(self) -> None:
        if self.__commit_task_future:
            self.__stop_commit_task.set()
            await self.__commit_task_future
        await self.__commit_pending_tasks()

    async def __manage_kafka_consumers_stopping(self) -> None:
        for kafka_consumer in self.__subscriber_per_consumer_mapper.keys():
            await kafka_consumer.stop()

    def __print_statistics(self) -> None:
        self.__logger.info("Number of subscribers: %d", len(self.__subscribers))
        self.__logger.info(f"Start kafka consumers elapsed time: {self.__start_kafka_consumers_elapsed_time}")
        self.__logger.info(f"Initial coroutines created elapsed time: {self.__initial_coroutines_created_elapsed_time}")
        self.__logger.info(f"Events processed: {self.__events_processed}")
        self.__logger.info(f"Events processed elapsed time: {self.__events_processed_elapsed_time}")
