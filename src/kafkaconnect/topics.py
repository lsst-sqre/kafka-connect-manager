"""Select Kafka topics."""

__all__ = ["Topic"]

import logging
import re
from typing import Optional, Set

from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

logger = logging.getLogger("kafkaconnect")


class Topic:
    """Select kafka topics.

    Parameters
    ----------
    broker_url : `str`
        The Kafka Broker URL.
    topic_regex : `str`
        Regex to select topics from Kafka.
    excluded_topics : `str`
        List of 'problematic' topics to exclude from selection.
    """

    def __init__(
        self, broker_url: str, topic_regex: str, excluded_topics: str
    ) -> None:
        self._names: Set[str] = set()
        self._broker_url = broker_url
        self._topic_regex = topic_regex
        self._excluded_topics = set(
            excluded_topics.replace(" ", "").split(",")
        )

    @property
    def names(self) -> Optional[Set[str]]:
        """Return a set of topic names from Kafka.

        Use config.topic_regex to and config.exlcuded_topics to
        filter topic names.
        """
        try:
            conf = {"bootstrap.servers": self._broker_url}
            metadata = AdminClient(conf).list_topics(timeout=10)
            self._names = set(metadata.topics.keys())
        except KafkaException:
            message = (
                f"Failed to establish connection with broker "
                f"{self._broker_url}."
            )
            logger.error(message)
            return None

        if self._topic_regex:
            pattern = re.compile(self._topic_regex)
            self._names = {name for name in self._names if pattern.match(name)}

        if self._excluded_topics:
            self._names = self._names - self._excluded_topics

        return self._names
