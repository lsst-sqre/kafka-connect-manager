"""Tets for the connect module."""

import pytest

from kafkaconnect.connect import Connect, HTTPMethod
from kafkaconnect.influxdb_sink.config import InfluxConfig


def test_expected_exception_get() -> None:
    """Test expected exception."""
    with pytest.raises(ValueError):
        connect = Connect(connect_url="http://some-url")
        connect._request(
            HTTPMethod.GET, uri="http://some-url", data='{"foo": "bar"}'
        )


def test_expected_exception_delete() -> None:
    """Test expected exception."""
    with pytest.raises(ValueError):
        connect = Connect(connect_url="http://some-url")
        connect._request(
            HTTPMethod.DELETE, uri="http://some-url", data='{"foo": "bar"}'
        )


@pytest.mark.vcr
def test_list() -> None:
    """Test list method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.list()
    assert "influxdb-sink" in result


@pytest.mark.vcr
def test_info() -> None:
    """Test info method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.info("influxdb-sink")
    assert '"name": "influxdb-sink"' in result


@pytest.mark.vcr
def test_status() -> None:
    """Test status method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.status("influxdb-sink")
    assert "RUNNING" in result


@pytest.mark.vcr
def test_config() -> None:
    """Test config method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.config("influxdb-sink")
    assert '"name": "influxdb-sink"' in result


@pytest.mark.vcr
def test_tasks() -> None:
    """Test tasks method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.tasks("influxdb-sink")
    assert '"task": 0' in result


@pytest.mark.vcr
def test_topics() -> None:
    """Test topics method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.topics("influxdb-sink")
    # Kafka Connect 5.3.1
    assert "connectors/influxdb-sink/topics not found." in result


@pytest.mark.vcr
def test_plugins() -> None:
    """Test plugins method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.plugins()
    assert "InfluxSinkConnector" in result


@pytest.mark.vcr
def test_remove() -> None:
    """Test remove method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.remove("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_create_or_update() -> None:
    """Test create_or_update method."""
    connect = Connect(connect_url="http://localhost:8083")
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
    connect_config.update_topics(["t1", "t2", "t3"])
    result = connect.create_or_update(
        name="influxdb-sink", connect_config=connect_config.asjson()
    )
    assert "influxdb-sink" in result


@pytest.mark.vcr
def test_validate() -> None:
    """Test validate method."""
    connect = Connect(connect_url="http://localhost:8083")
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
    connect_config.update_topics(["t1", "t2", "t3"])
    result = connect.validate(
        name="InfluxSinkConnector", connect_config=connect_config.asjson()
    )
    assert "error_count" in result


@pytest.mark.vcr
def test_restart() -> None:
    """Test restart method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.restart("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_pause() -> None:
    """Test pause method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.pause("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_resume() -> None:
    """Test resume method."""
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.resume("influxdb-sink")
    assert result == ""
