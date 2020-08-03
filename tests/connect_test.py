import pytest

from kafkaconnect.connect import Connect, HTTPMethod
from kafkaconnect.influxdb_sink.config import InfluxConfig


def test_expected_exception_get() -> None:
    with pytest.raises(ValueError):
        connect = Connect(connect_url="http://some-url")
        connect._request(
            HTTPMethod.GET, uri="http://some-url", data='{"foo": "bar"}'
        )


def test_expected_exception_delete() -> None:
    with pytest.raises(ValueError):
        connect = Connect(connect_url="http://some-url")
        connect._request(
            HTTPMethod.DELETE, uri="http://some-url", data='{"foo": "bar"}'
        )


@pytest.mark.vcr
def test_list() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.list()
    assert "influxdb-sink" in result


@pytest.mark.vcr
def test_info() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.info("influxdb-sink")
    assert '"name": "influxdb-sink"' in result


@pytest.mark.vcr
def test_status() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.status("influxdb-sink")
    assert "RUNNING" in result


@pytest.mark.vcr
def test_config() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.config("influxdb-sink")
    assert '"name": "influxdb-sink"' in result


@pytest.mark.vcr
def test_tasks() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.tasks("influxdb-sink")
    assert '"task": 0' in result


@pytest.mark.vcr
def test_topics() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.topics("influxdb-sink")
    # Kafka Connect 5.3.1
    assert "connectors/influxdb-sink/topics not found." in result


@pytest.mark.vcr
def test_plugins() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.plugins()
    assert "InfluxSinkConnector" in result


@pytest.mark.vcr
def test_remove() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.remove("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_create_or_update() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    connect_config = InfluxConfig()
    connect_config.update_topics(["t1", "t2", "t3"])
    result = connect.create_or_update(
        name="influxdb-sink", connect_config=connect_config.asjson()
    )
    assert "influxdb-sink" in result


@pytest.mark.vcr
def test_validate() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    connect_config = InfluxConfig()
    connect_config.update_topics(["t1", "t2", "t3"])
    result = connect.validate(
        name="InfluxSinkConnector", connect_config=connect_config.asjson()
    )
    assert "error_count" in result


@pytest.mark.vcr
def test_restart() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.restart("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_pause() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.pause("influxdb-sink")
    assert result == ""


@pytest.mark.vcr
def test_resume() -> None:
    connect = Connect(connect_url="http://localhost:8083")
    result = connect.resume("influxdb-sink")
    assert result == ""
