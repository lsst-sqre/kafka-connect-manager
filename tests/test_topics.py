from typing import Any

import pytest
from confluent_kafka import KafkaException
from confluent_kafka.admin import AdminClient

from kafkaconnect.config import Config

Fixture = Any


def is_responsive() -> bool:
    try:
        conf = {"bootstrap.servers": Config.broker_url}
        _ = AdminClient(conf).list_topics(timeout=10)
    except KafkaException:
        return False
    return True


@pytest.fixture(scope="session")
def ensure_broker_service(docker_services: Fixture) -> bool:
    """Ensure that broker service is up and responsive."""

    docker_services.wait_until_responsive(
        timeout=300, pause=30, check=lambda: is_responsive()
    )
    return True


@pytest.mark.docker
def test_topic_names(ensure_broker_service: Fixture) -> None:
    pass
