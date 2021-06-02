"""kafkaconnect integration tests."""

import time
from typing import Any

import pytest
import requests
from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from requests.exceptions import ConnectionError, HTTPError

from kafkaconnect.connect import Connect
from kafkaconnect.influxdb_sink.config import InfluxConfig
from kafkaconnect.topics import Topic

Fixture = Any

BROKER_URL = "localhost:9092"
CONNECT_URL = "http://localhost:8083"


def is_broker_responsive() -> bool:
    """Check if broker is ready."""
    try:
        admin_client = AdminClient({"bootstrap.servers": BROKER_URL})
        admin_client.list_topics(timeout=10)
    except KafkaException:
        return False
    return True


def is_connect_responsive() -> bool:
    """Check if the kafka connet API is ready."""
    try:
        response = requests.get(f"{CONNECT_URL}/connectors")
        response.raise_for_status()
    except ConnectionError:
        return False
    except HTTPError:
        return False
    return True


@pytest.fixture(scope="session")
def ensure_broker_service(docker_services: Fixture) -> bool:
    """Ensure that broker service is up and responsive."""
    docker_services.wait_until_responsive(
        timeout=300, pause=30, check=lambda: is_broker_responsive()
    )
    return True


@pytest.fixture(scope="session")
def ensure_connect_service(docker_services: Fixture) -> bool:
    """Ensure that connect service is up and responsive."""
    docker_services.wait_until_responsive(
        timeout=300, pause=30, check=lambda: is_connect_responsive()
    )
    return True


@pytest.mark.docker
def test_integration_broker_connect(
    ensure_broker_service: Fixture, ensure_connect_service: Fixture
) -> None:
    """Test kafkaconnect with a Kafka broker and Kafka Connect.

    pytest-docker uses the docker-compose.yaml in the test directory.
    """
    admin_client = AdminClient({"bootstrap.servers": BROKER_URL})
    t1 = NewTopic(topic="test.t1", num_partitions=1)
    t2 = NewTopic(topic="test.t2", num_partitions=1)
    t3 = NewTopic(topic="test.t3", num_partitions=1)
    # Create test topics in Kafka
    try:
        admin_client.create_topics([t1, t2, t3])
        time.sleep(5)
    except KafkaException:
        return None
    # Test topic discovery
    topic = Topic(
        broker_url=BROKER_URL,
        topic_regex="test.*",
        excluded_topic_regex="test.t1",
    )
    assert "test.t1" not in topic.names
    assert "test.t2" in topic.names
    assert "test.t3" in topic.names
    # Configure the connector
    connect = Connect(connect_url=CONNECT_URL)
    connect_config = InfluxConfig(
        name="influxdb-sink",
        connect_influx_url="http://localhost:8086",
        connect_influx_db="mydb",
        tasks_max=1,
        connect_influx_username="foo",
        connect_influx_password="bar",
        connect_influx_error_policy="foo",
        connect_influx_max_retries="1",
        connect_influx_retry_interval="1",
        connect_progress_enabled=True,
    )
    connect_config.update_topics(topic.names)
    # Create the connector using the Kafka Connect API
    connect.create_or_update(
        name="influxdb-sink", connect_config=connect_config.asjson()
    )
    # List connectors from the Kafka Connect API
    list = connect.list()
    assert "influxdb-sink" in list
