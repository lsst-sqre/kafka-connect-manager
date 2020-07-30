import os
from dataclasses import dataclass, field
from typing import List

from kafkaconnect.config import ConnectConfig


@dataclass
class InfluxConfig(ConnectConfig):
    """InfluxDB connector configuration"""

    name: str = os.getenv("KAFKA_CONNECT_NAME", "influxdb-sink")
    """Name of the connector.

    The connector name must be unique accross the cluster.
    """

    connect_influx_url: str = os.getenv(
        "KAFKA_CONNECT_INFLUXDB_URL", "http://localhost:8086"
    )
    """InfluxDB connection URL."""

    connect_influx_db: str = os.getenv("KAFKA_CONNECT_DATABASE", "mydb")
    """InfluxDB database name."""

    connector_class: str = (
        "com.datamountaineer.streamreactor.connect.influx.InfluxSinkConnector"
    )
    """Stream reactor InfluxDB Sink connector class"""

    connect_influx_kcql: List[str] = field(default_factory=list)
    """KCQL queries to extract fields from topics.

    We assume that a topic has a flat structure so that `SELECT * FROM` will
    retrieve all topic fields. This is configuration is derived from the list
    of topics and from the timestamp to use as the InfluxDB time.
    """

    connect_influx_username: str = os.getenv(
        "KAFKA_CONNECT_INFLUXDB_USERNAME", "-"
    )
    """InfluxDB username."""

    connect_influx_password: str = os.getenv(
        "KAFKA_CONNECT_INFLUXDB_PASSWORD", ""
    )
    """InfluxDB password."""

    connect_influx_error_policy: str = os.getenv(
        "KAFKA_CONNECT_ERROR_POLICY", "THROW"
    )
    """Connector error policy configuration.

    See https://docs.lenses.io/connectors/sink/influx.html
    """

    connect_influx_max_retries: str = os.getenv(
        "KAFKA_CONNECT_MAX_RETRIES", "10"
    )
    """Connector error policy configuration.

    See https://docs.lenses.io/connectors/sink/influx.html
    """

    connect_influx_retry_interval: str = os.getenv(
        "KAFKA_CONNECT_RETRY_INTERVAL", "60000"
    )
    """Connector error policy configuration.

    See https://docs.lenses.io/connectors/sink/influx.html
    """

    connect_progress_enabled: bool = os.getenv(
        "KAFKA_CONNECT_PROGRESS_ENABLED", "false"
    ) == "true"
    """Enables the output for how many records have been processed."""

    def update_influx_kcql(self, timestamp: str = "sys_time()") -> None:

        topics = self.topics.split(",")
        queries = [
            f"INSERT INTO {t} SELECT * FROM {t} WITHTIMESTAMP {timestamp}"
            for t in topics
        ]
        self.connect_influx_kcql = ";".join(queries)
