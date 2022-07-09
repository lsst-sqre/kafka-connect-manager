"""Tests for the Topic class."""

from typing import Any, List

import pytest

from kafkaconnect.topic_names_set import TopicNamesSet

Fixture = Any


@pytest.fixture()
def topic_names_list() -> List:
    """Return a list of topic names to use in the tests."""
    return ["test.t1", "test.t2", "test.t3"]


def test_select_regex(topic_names_list: Fixture) -> None:
    """Test topic selection using a regex."""
    t = TopicNamesSet(topic_names_list, select_regex="test.*")

    assert "test.t1" in t.topic_names_set
    assert "test.t2" in t.topic_names_set
    assert "test.t3" in t.topic_names_set


def test_select_regex_topic_name(topic_names_list: Fixture) -> None:
    """Test topic selection using a topic name."""
    t = TopicNamesSet(topic_names_list, select_regex="test.t1")

    assert "test.t1" in t.topic_names_set
    assert "test.t2" not in t.topic_names_set
    assert "test.t3" not in t.topic_names_set


def test_exclude_regex(topic_names_list: Fixture) -> None:
    """Test topic exlusion using a regex."""
    t = TopicNamesSet(
        topic_names_list, select_regex="test.*", exclude_regex="test.t[1-2]"
    )

    assert "test.t1" not in t.topic_names_set
    assert "test.t2" not in t.topic_names_set
    assert "test.t3" in t.topic_names_set


def test_exclude_regex_topic_name(topic_names_list: Fixture) -> None:
    """Test topic exclusion using a single topic name."""
    t = TopicNamesSet(
        topic_names_list, select_regex="test.*", exclude_regex="test.t2"
    )

    assert "test.t1" in t.topic_names_set
    assert "test.t2" not in t.topic_names_set
    assert "test.t3" in t.topic_names_set


def test_exclude_all(topic_names_list: Fixture) -> None:
    """Test selecting and excluding all topics."""
    t = TopicNamesSet(
        topic_names_list, select_regex="test.*", exclude_regex="test.*"
    )

    assert t.topic_names_set == set()
