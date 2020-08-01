"""Kafkaconnect application and generic connector configuration."""

__all__ = ["Config", "ConnectConfig"]

import json
import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class Config:
    """Kafkaconnect application configuration."""

    broker_url: str = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
    """The Kafka Broker URL.
    """

    connect_url: str = os.getenv("KAFKA_CONNECT_URL", "http://localhost:8083")
    """The Kafka Connect URL.

    The Kafka Connect REST API is used to manage connectors.
    """

    topic_regex: str = os.getenv("KAFKA_CONNECT_TOPIC_REGEX", ".*")
    """Regex to select topics from Kafka."""

    excluded_topics: str = os.getenv("KAFKA_CONNECT_EXCLUDED_TOPICS", "")
    """Comma separated list of topics to exclude from selection."""

    check_interval: int = int(os.getenv("KAFKA_CONNECT_CHECK_INTERVAL", 15000))
    """The interval, in milliseconds, to update the connector.

    Check Kafka for new topics and update the connector configuration.
    """


@dataclass
class ConnectConfig:
    """Generic connector configuration."""

    name: str = ""
    """Name of the connector.

    The connector name must be unique accross the cluster.
    """

    connector_class: str = ""
    """Name of the connector class."""

    topics: str = ""
    """Comma separated list of Kafka topics to read from (sink connectors) or
    to write to (source connectors).
    """

    tasks_max: int = int(os.getenv("KAFKA_CONNECT_TASKS_MAX", "1"))
    """Number of connect tasks to scale out.

    Topics and partitions are distributed accross tasks.
    """

    def update_topics(self, topics: List[str]) -> None:
        """Update the list of Kafka topics.

        Parameters
        ----------
        topics : `list`
            List of kafka topics.
        """
        # Ensure uniqueness and sort topic names
        topics = list(set(topics))
        topics.sort()
        self.topics = ",".join(topics)

    @staticmethod
    def format_field_names(fields: List[Tuple[str, Any]]) -> Dict[str, str]:
        """Dictionary factory to use with the dataclasses.asdict() method.

        Rename the field name replacing '_' by '.' and return a dictionary
        mapping field names to field values.
        """
        result = []
        for f in fields:
            name, value = f
            name = name.replace("_", ".")
            result.append((name, value))
        return dict(result)

    def asjson(self) -> str:
        config = asdict(self, dict_factory=self.format_field_names)
        return json.dumps(config, indent=4, sort_keys=True)
