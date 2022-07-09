"""A set of topics names used to configure the connector."""

__all__ = ["TopicNamesSet"]

import logging
import re
from typing import List, Optional, Set, Type, TypeVar

from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

from kafkaconnect.config import Config

T = TypeVar("T", bound="TopicNamesSet")


logger = logging.getLogger("kafkaconnect")

SECURITY_PROTOCOL = "SASL_PLAINTEXT"
SASL_MECHANISM = "SCRAM-SHA-512"


class TopicNamesSet:
    """A set of topics names used to configure the connector.

    Parameters
    ----------
    topic_names_list : `List`
        A list topic names
    select_regex : `str`
        A regex to add topic names to the set.
    exclude_regex : `str`
        A regex to exclude topic names from the set.


    Raises
    ------
    ValueError
        If an ``topic_names_list`` entry contains any invalid names
        or duplicates with prior information.

    """

    def __init__(
        self,
        topic_names_list: List,
        select_regex: str = ".*",
        exclude_regex: Optional[str] = None,
    ) -> None:

        self.topic_names_list = topic_names_list
        self.select_regex = select_regex
        self.exclude_regex = exclude_regex
        self.topic_names_set = self.filter_topics()

    def filter_topics(self) -> Set[str]:
        """Filter a list of topic names.

        Returns
        -------
        topic_names_set: `Set`
            A a set of topic names.
        """
        topic_names_set = set(self.topic_names_list)

        if self.select_regex:
            pattern = re.compile(self.select_regex)
            topic_names_set = {
                topic for topic in topic_names_set if pattern.match(topic)
            }

        if self.exclude_regex:
            pattern = re.compile(self.exclude_regex)
            excluded_topic_names = {
                topic for topic in topic_names_set if pattern.match(topic)
            }
            topic_names_set = topic_names_set - excluded_topic_names

        return topic_names_set

    @classmethod
    def from_kafka(
        cls: Type[T],
        config: Config,
        select_regex: str = ".*",
        exclude_regex: Optional[str] = None,
    ) -> T:
        """Create the topic name set from a list of topic names in Kafka."""
        if config.sasl_plain_username and config.sasl_plain_password:
            kafka_config = {
                "bootstrap.servers": config.broker_url,
                "security.protocol": SECURITY_PROTOCOL,
                "sasl.mechanisms": SASL_MECHANISM,
                "sasl.username": config.sasl_plain_username,
                "sasl.password": config.sasl_plain_password,
            }
        elif (
            config.sasl_plain_username is None
            and config.sasl_plain_password is None
        ):
            kafka_config = {"bootstrap.servers": config.broker_url}
        else:
            raise ValueError(
                "Both or neither of 'config.sasl_plain_username' "
                "and 'config.sasl_plain_password' must be set."
            )
        try:
            broker_client = AdminClient(kafka_config)
        except KafkaException:
            message = (
                f"Failed to establish connection with broker "
                f"{config.broker_url}."
            )
            logger.error(message)

        topic_names_list: List = broker_client.list_topics(
            timeout=10
        ).topics.keys()

        return cls(
            topic_names_list=topic_names_list,
            select_regex=select_regex,
            exclude_regex=exclude_regex,
        )
