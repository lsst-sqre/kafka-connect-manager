"""InfluxDB Sink connector configuration.

See https://docs.lenses.io/connectors/sink/influx.html.
"""

from dataclasses import dataclass
from typing import List

from kafkaconnect.config import ConnectorConfig


@dataclass
class InfluxConfig(ConnectorConfig):
    """InfluxDB connector configuration."""

    name: str
    """Name of the connector."""

    connect_influx_url: str
    """InfluxDB connection URL."""

    connect_influx_db: str
    """InfluxDB database name."""

    tasks_max: int
    """Number of Kafka Connect tasks."""

    connect_influx_username: str
    """InfluxDB username."""

    connect_influx_password: str
    """InfluxDB password."""

    connect_influx_error_policy: str
    """Connector error policy configuration."""

    connect_influx_max_retries: str
    """Connector error policy configuration."""

    connect_influx_retry_interval: str
    """Connector error policy configuration."""

    connect_progress_enabled: bool
    """Enables the output for how many records have been processed."""

    # Attributes with defaults are not configurable via click
    topics: str = ""
    """Comma separated list of Kafka topics to read from."""

    connect_influx_kcql: str = ""
    """KCQL queries to extract fields from topics. Computed.

    We assume that a topic has a flat structure so that `SELECT * FROM` will
    retrieve all topic fields. This is configuration is derived from the list
    of topics and from the timestamp to use as the InfluxDB time.
    """

    connector_class: str = (
        "com.datamountaineer.streamreactor.connect.influx.InfluxSinkConnector"
    )
    """Stream reactor InfluxDB Sink connector class."""

    def update_topics(self, topics: List[str], timestamp: str = "") -> None:
        """Update the list of Kafka topics and Influx KCQL queries.

        Parameters
        ----------
        topics : `list`
            List of kafka topics.

        timestamp : `str`
            Timestamp used as influxDB time.
        """
        # Ensure uniqueness and sort topic names
        topics = list(set(topics))
        topics.sort()
        queries = [
            f"INSERT INTO {t} SELECT * FROM {t} WITHTIMESTAMP {timestamp}"
            for t in topics
        ]
        self.topics = ",".join(topics)
        self.connect_influx_kcql = ";".join(queries)
