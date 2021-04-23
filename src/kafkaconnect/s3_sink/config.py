"""S3 Sink connector configuration.

See https://docs.confluent.io/current/connect/kafka-connect-s3.
"""

from dataclasses import dataclass
from typing import List

from kafkaconnect.config import ConnectorConfig


@dataclass
class S3Config(ConnectorConfig):
    """S3 Sink connector configuration."""

    name: str
    """Name of the connector. Configurable."""

    s3_bucket_name: str
    """The S3 Bucket."""

    s3_region: str
    """The AWS region to be used the connector."""

    aws_access_key_id: str
    """The AWS access key ID used to authenticate personal AWS credentials."""

    aws_secret_access_key: str
    """The secret access key used to authenticate personal AWS credentials."""

    topics_dir: str
    """Top level directory to store the data ingested from Kafka."""

    s3_schema_compatibility: str
    """The S3 schema compatibility mode."""

    flush_size: int
    """Number of records written to store before invoking file commits."""

    rotate_interval_ms: int
    """The time interval in milliseconds to invoke file commits."""

    partition_duration_ms: int
    """The duration of a partition in ms, used by the TimeBasedPartitioner."""

    path_format: str
    """Pattern used to format the path in the S3 object name."""

    tasks_max: int
    """Number of Kafka Connect tasks."""

    locale: str
    """The locale to use when partitioning with TimeBasedPartitioner."""

    timezone: str
    """The timezone to use when partitioning with TimeBasedPartitioner."""

    timestamp_extractor: str
    """The extractor determines how to obtain a timestamp from each record."""

    timestamp_field: str
    """The record field to be used as timestamp by the timestamp extractor."""

    # Attributes with defaults are not configured via click
    topics: str = ""
    """Comma separated list of Kafka topics to read from."""

    connector_class: str = "io.confluent.connect.s3.S3SinkConnector"
    """S3 Sink connector class"""

    format_class: str = "io.confluent.connect.s3.format.parquet.ParquetFormat"
    """The format class to use when writing data to the store."""

    parquet_codec: str = "snappy"
    """The Parquet compression codec to be used for output files."""

    storage_class: str = "io.confluent.connect.s3.storage.S3Storage"
    """The underlying storage layer."""

    partitioner_class: str = (
        "io.confluent.connect.storage.partitioner.TimeBasedPartitioner"
    )
    """The partitioner to use when writing data to the store."""

    def update_topics(self, topics: List[str]) -> None:
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
        self.topics = ",".join(topics)
