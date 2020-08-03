"""Select Kafka topics."""

__all__ = ["Topic"]

import logging
import re
from typing import List, Optional, Set

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
        self._admin_client = self._get_admin_client(broker_url)
        self._topic_regex = topic_regex
        self._excluded_topics = set(
            excluded_topics.replace(" ", "").split(",")
        )

    def _get_admin_client(self, broker_url: str) -> Optional[AdminClient]:
        """Get an instance of the Kafka admin client.

        Parameters
        ----------
        broker_url : `str`

        Returns
        -------
        admin_client : `AdminClient` or None
        """
        try:
            conf = {"bootstrap.servers": broker_url}
            admin_client = AdminClient(conf).list_topics(timeout=10)
        except KafkaException:
            message = (
                f"Failed to establish connection with broker " f"{broker_url}."
            )
            logger.error(message)
            admin_client = None

        return admin_client

    @property
    def names(self) -> List[str]:
        """Return a list of topic names from Kafka.

        Use config.topic_regex to and config.exlcuded_topics to
        filter topic names.

        Returns
        -------

        topics: list
            A list of topic names from Kafka. Return an empty list if no topics
            are found.

        """
        if self._admin_client:
            self._names = set(self._admin_client.topics.keys())

        if self._topic_regex:
            pattern = re.compile(self._topic_regex)
            self._names = {name for name in self._names if pattern.match(name)}

        if self._excluded_topics:
            self._names = self._names - self._excluded_topics

        return list(self._names)
