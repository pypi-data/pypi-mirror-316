from __future__ import annotations

from logging import Logger, getLogger
from typing import Optional, Type

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor

from buz.kafka.domain.models.auto_create_topic_configuration import AutoCreateTopicConfiguration
from buz.kafka.domain.models.consumer_initial_offset_position import ConsumerInitialOffsetPosition
from buz.kafka.domain.models.kafka_connection_config import KafkaConnectionConfig
from buz.kafka.domain.services.kafka_admin_client import KafkaAdminClient
from buz.kafka.infrastructure.aiokafka.aiokafka_multi_threaded_consumer import AIOKafkaMultiThreadedConsumer


class KafkaPythonMultiThreadedConsumerFactory:
    __FALLBACK_PARTITION_ASSIGNORS = (RoundRobinPartitionAssignor,)

    def __init__(
        self,
        consumer_group: str,
        topics: list[str],
        kafka_connection_config: KafkaConnectionConfig,
        kafka_admin_client: Optional[KafkaAdminClient],
        initial_offset_position: ConsumerInitialOffsetPosition = ConsumerInitialOffsetPosition.BEGINNING,
        kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...] = (),
        auto_create_topic_configuration: Optional[AutoCreateTopicConfiguration] = None,
        logger: Logger = getLogger(),
    ) -> None:
        self.__consumer_group = consumer_group
        self.__topics = topics
        self.__kafka_connection_config = kafka_connection_config
        self.__kafka_admin_client = kafka_admin_client
        self.__initial_offset_position = initial_offset_position
        self.__kafka_partition_assignors = self.__get_partition_assignors_ordered_by_priority(kafka_partition_assignors)
        self.__auto_create_topic_configuration = auto_create_topic_configuration
        self.__logger = logger

    def __get_partition_assignors_ordered_by_priority(
        self, kafka_partition_assignors: tuple[Type[AbstractPartitionAssignor], ...]
    ) -> tuple[Type[AbstractPartitionAssignor], ...]:
        # A tuple is used to support rolling-updates.
        return tuple(kafka_partition_assignors + self.__FALLBACK_PARTITION_ASSIGNORS)

    def build(self) -> AIOKafkaMultiThreadedConsumer:
        return AIOKafkaMultiThreadedConsumer(
            consumer_group=self.__consumer_group,
            topics=self.__topics,
            connection_config=self.__kafka_connection_config,
            initial_offset_position=self.__initial_offset_position,
            partition_assignors=self.__kafka_partition_assignors,
            logger=self.__logger,
            kafka_admin_client=self.__kafka_admin_client,
            auto_create_topic_configuration=self.__auto_create_topic_configuration,
        )
