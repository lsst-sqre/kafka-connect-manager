# This file is part of kafka-connect-manager.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Tests for `kafka-connect-manager` package.
"""

import pytest

from click.testing import CliRunner
from connect_manager.replicator import make_replicator_config
from connect_manager import main


@pytest.fixture
def config():
    """Fixture to return the replicator configuration given a set of
    input values.
    """
    topics = ['t1', 'topic2', 'topic3']
    blacklist = ['topic2']
    src_kafka = 'localhost:80'
    dest_kafka = 'localhost:80'
    topic_rename_format = '${topic}'
    tasks = 4
    schema_registry_topic = '_schemas'
    schema_registry_url = 'http://example.com'
    group_id = None
    filter_regex = 'topic*'
    check_interval = '1000'

    config = make_replicator_config(topics, src_kafka, dest_kafka,
                                    topic_rename_format, tasks,
                                    schema_registry_topic,
                                    schema_registry_url, group_id,
                                    filter_regex, blacklist, check_interval)
    return config


def test_replicator_config(config):
    """ Test replicator config """

    DEFAULT_CONVERTER = 'io.confluent.connect.replicator.util.'\
                        'ByteArrayConverter'

    assert config['connector.class'] == 'io.confluent.connect.replicator.'\
        'ReplicatorSourceConnector'
    assert config['dest.kafka.bootstrap.servers'] == 'localhost:80'
    assert config['header.coverter'] == DEFAULT_CONVERTER
    assert config['key.converter'] == DEFAULT_CONVERTER
    assert config['schema.registry.topic'] == '_schemas'
    assert config['schema.registry.url'] == 'http://example.com'
    assert config['schema.subject.translator.class'] == 'io.confluent.connect'\
        '.replicator.schemas.DefaultSubjectTranslator'
    assert config['src.kafka.bootstrap.servers'] == 'localhost:80'
    assert config['tasks.max'] == 4
    assert config['topic.poll.interval.ms'] == '1000'
    assert config['topic.rename.format'] == '${topic}'
    assert config['topic.regex'] == 'topic*'
    # Make sure blacklisted 'topic2' is not whitelisted
    assert config['topic.blacklist'] == 'topic2'
    # Whitelisted topics do not have to match the regex
    assert config['topic.whitelist'] == 't1,topic3,_schemas'
    assert config['value.converter'] == DEFAULT_CONVERTER


def test_replicator_cli():
    """Test the CLI for the replicator subcommand."""
    runner = CliRunner()
    create_result = runner.invoke(main.main, ['create'])
    assert create_result.exit_code == 0
    assert 'replicator' in create_result.output
    create_replicator_result = runner.invoke(main.main,
                                             ['create replicator'])
    assert create_replicator_result.exit_code == 2
