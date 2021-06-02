"""Tests for the Topic class."""

from typing import Any, List

import pytest

from kafkaconnect.topics import Topic

Fixture = Any


@pytest.fixture()
def get_topic_names() -> List:
    """Return list of topic names to use in the tests."""
    return ["test.t1", "test.t2", "test.t3"]


def test_topic_regex(get_topic_names: Fixture) -> None:
    """Test topic selection using a regex."""
    topic = Topic(topic_regex="test.*")
    topic._names = get_topic_names

    assert "test.t1" in topic.names
    assert "test.t2" in topic.names
    assert "test.t3" in topic.names


def test_topic_regex_single(get_topic_names: Fixture) -> None:
    """Test topic selection using a single topic name."""
    topic = Topic(topic_regex="test.t1")
    topic._names = get_topic_names

    assert "test.t1" in topic.names
    assert "test.t2" not in topic.names
    assert "test.t3" not in topic.names


def test_excluded_topic_regex(get_topic_names: Fixture) -> None:
    """Test topic exlusion using a regex."""
    topic = Topic(topic_regex="test.*", excluded_topic_regex="test.t[1-2]")
    topic._names = get_topic_names

    assert "test.t1" not in topic.names
    assert "test.t2" not in topic.names
    assert "test.t3" in topic.names


def test_excluded_topic_regex_single(get_topic_names: Fixture) -> None:
    """Test topic exclusion using a single topic name."""
    topic = Topic(topic_regex="test.*", excluded_topic_regex="test.t2")
    topic._names = get_topic_names

    assert "test.t1" in topic.names
    assert "test.t2" not in topic.names
    assert "test.t3" in topic.names


def test_exclude_all(get_topic_names: Fixture) -> None:
    """Test selecting and excluding all topics."""
    topic = Topic(topic_regex="test.*", excluded_topic_regex="test.*")
    topic._names = get_topic_names

    assert topic.names == []
