from __future__ import annotations

from logging import Logger
from ssl import SSLContext
from typing import Optional, cast

from aiokafka import AIOKafkaConsumer, TopicPartition, OffsetAndMetadata
from aiokafka.helpers import create_ssl_context
from buz.event.infrastructure.buz_kafka.exceptions.kafka_event_bus_config_not_valid_exception import (
    KafkaEventBusConfigNotValidException,
)

from buz.kafka.domain.models.auto_create_topic_configuration import AutoCreateTopicConfiguration
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.create_kafka_topic import CreateKafkaTopic
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.models.kafka_poll_record import KafkaPollRecord
from buz.kafka.domain.models.kafka_supported_security_protocols import KafkaSupportedSecurityProtocols
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient
from buz.kafka.infrastructure.aiokafka.rebalance.rebalance_ready import RebalanceReady
from buz.kafka.infrastructure.aiokafka.rebalance.simple_kafka_lock_rebalancer import SimpleKafkaLockRebalancer
from buz.kafka.infrastructure.aiokafka.translators.consumer_initial_offset_position_translator import (
    AIOKafkaConsumerInitialOffsetPositionTranslator,
)


class AIOKafkaMultiThreadedConsumer(RebalanceReady):
    __DEFAULT_POLL_TIMEOUT_MS = 0
    __DEFAULT_SESSION_TIMEOUT_MS = 1000 * 60
    __DEFAULT_HEARTBEAT_INTERVAL_MS = 1000 * 15
    __DEFAULT_MAX_POLL_INTERVAL = 2147483647

    def __init__(
        self,
        *,
        consumer_group: str,
        topics: list[str],
        connection_config: KafkaConnectionConfig,
        kafka_admin_client: Optional[KafkaAdminClient],
        initial_offset_position: ConsumerInitialOffsetPosition,
        partition_assignors: tuple,
        logger: Logger,
        session_timeout_ms: int = __DEFAULT_SESSION_TIMEOUT_MS,
        auto_create_topic_configuration: Optional[AutoCreateTopicConfiguration] = None,
    ) -> None:
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__initial_offset_position = initial_offset_position
        self.__connection_config = connection_config
        self.__kafka_admin_client = kafka_admin_client
        self.__partition_assignors = partition_assignors
        self.__logger = logger
        self.__session_timeout_ms = session_timeout_ms
        self.__pending_messages: int = 0
        self.__auto_create_topic_configuration = auto_create_topic_configuration
        self.__check_kafka_admin_client_is_needed()
        self.__consumer = self.__generate_consumer()

    def __check_kafka_admin_client_is_needed(self) -> None:
        if self.__kafka_admin_client is None and self.__auto_create_topic_configuration is not None:
            raise KafkaEventBusConfigNotValidException(
                "A KafkaAdminClient is needed to create topics when 'auto_create_topic_configuration' is set."
            )

    def __generate_consumer(self) -> AIOKafkaConsumer:
        sasl_mechanism: Optional[str] = None
        ssl_context: Optional[SSLContext] = None

        if self.__auto_create_topic_configuration is not None:
            self.__ensure_topics_are_created(self.__auto_create_topic_configuration)

        if self.__connection_config.credentials.sasl_mechanism is not None:
            sasl_mechanism = self.__connection_config.credentials.sasl_mechanism.value

        if self.__connection_config.credentials.security_protocol == KafkaSupportedSecurityProtocols.SASL_SSL:
            ssl_context = create_ssl_context()
        consumer = AIOKafkaConsumer(
            None,
            ssl_context=ssl_context,
            bootstrap_servers=self.__connection_config.bootstrap_servers,
            security_protocol=self.__connection_config.credentials.security_protocol.value,
            sasl_mechanism=sasl_mechanism,
            sasl_plain_username=self.__connection_config.credentials.user,
            sasl_plain_password=self.__connection_config.credentials.password,
            client_id=self.__connection_config.client_id,
            group_id=self.__consumer_group,
            enable_auto_commit=False,
            auto_offset_reset=AIOKafkaConsumerInitialOffsetPositionTranslator.to_kafka_supported_format(
                self.__initial_offset_position
            ),
            session_timeout_ms=self.__session_timeout_ms,
            heartbeat_interval_ms=self.__DEFAULT_HEARTBEAT_INTERVAL_MS,
            partition_assignment_strategy=list(self.__partition_assignors),
            max_poll_interval_ms=self.__DEFAULT_MAX_POLL_INTERVAL,
            rebalance_timeout_ms=self.__DEFAULT_MAX_POLL_INTERVAL,
        )

        consumer.subscribe(topics=self.__topics, listener=SimpleKafkaLockRebalancer(self))
        return consumer

    def __ensure_topics_are_created(self, auto_create_topic_configuration: AutoCreateTopicConfiguration) -> None:
        kafka_admin_client = self.__get_kafka_admin_client()
        non_created_topics = [topic for topic in self.__topics if not kafka_admin_client.is_topic_created(topic)]

        if len(non_created_topics) == 0:
            return None

        topics_to_create = [
            CreateKafkaTopic(
                name=topic,
                partitions=auto_create_topic_configuration.partitions,
                replication_factor=auto_create_topic_configuration.replication_factor,
                configs=auto_create_topic_configuration.configs,
            )
            for topic in non_created_topics
        ]
        self.__logger.info(f"Created missing topics: {non_created_topics}")
        kafka_admin_client.create_topics(topics=topics_to_create)

    def __get_kafka_admin_client(self) -> KafkaAdminClient:
        if self.__kafka_admin_client is None:
            raise KafkaEventBusConfigNotValidException("KafkaAdminClient is not set.")
        return self.__kafka_admin_client

    async def init(self) -> None:
        await self.__consumer.start()

    async def poll(
        self,
        *,
        timeout_ms: int = __DEFAULT_POLL_TIMEOUT_MS,
        number_of_messages_to_poll: Optional[int] = None,
    ) -> list[KafkaPollRecord]:
        poll_results = await self.__consumer.getmany(
            timeout_ms=timeout_ms,
            max_records=number_of_messages_to_poll,
        )

        results = [
            cast(KafkaPollRecord, consumer_record)
            for consumer_records in poll_results.values()
            for consumer_record in consumer_records
        ]

        self.__pending_messages += len(results)

        return results

    async def commit_poll_record(self, poll_record: KafkaPollRecord) -> None:
        offset = {
            TopicPartition(topic=poll_record.topic, partition=poll_record.partition): OffsetAndMetadata(
                poll_record.offset + 1, ""
            )
        }
        await self.__consumer.commit(offset)
        self.__pending_messages -= 1

    async def stop(self) -> None:
        self.__logger.info(f"Closing connection of consumer with group_id={self.__consumer_group}")
        self.__pending_messages = 0
        await self.__consumer.stop()

    def is_ready_for_rebalancing(self) -> bool:
        return self.__pending_messages == 0
