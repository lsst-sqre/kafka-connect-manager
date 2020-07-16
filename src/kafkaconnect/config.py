"""Configuration definition."""

__all__ = ["Configuration"]

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Configuration:
    """Configuration for kafkaconnect."""

    broker_url: str = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
    """The Kafka Broker URL.
    """

    connect_url: str = os.getenv("KAFKA_CONNECT_URL", "http://localhost:8083")
    """The Kafka Connect URL.

    The Kafka Connect REST API is used to manage connectors.
    """

    topic_regex: str = os.getenv("TOPIC_REGEX", ".*")
    """Regex to select topics from Kafka."""

    excluded_topics: List[str] = field(default_factory=list)
    """List of topics excluded from Kafka."""

    def __post_init__(self) -> None:
        """Post config initialization steps."""
        # Set default value for excluded_topics
        self.excluded_topics = self._strtolist(
            os.getenv("EXCLUDED_TOPICS", "")
        )

    def _strtolist(self, s: str) -> List[str]:
        """Convert comma separated values to a list of strings.

        Parameters
        ----------
        s : `str`
            Comma separated values

        Returns
        -------
        slist : `list`
        """
        slist = s.replace(" ", "").split(",")
        return slist


config = Configuration()
