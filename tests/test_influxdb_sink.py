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
from connect_manager.influxdb_sink import make_influxdb_sink_config
from connect_manager.influxdb_sink import update_influxdb_sink_config
from connect_manager import main


@pytest.fixture
def config():
    """Fixture to return the influxdb-sink configuration given a set of
    input values.
    """
    influxdb_url = 'https://example.com'
    database = 'mydb'
    tasks = 1
    username = 'nobody'
    password = None
    error_policy = 'NOOP'
    max_retries = '1'
    retry_interval = '1000'
    config = make_influxdb_sink_config(influxdb_url,
                                       database, tasks, username,
                                       password, error_policy,
                                       max_retries, retry_interval)
    topics = ['topic1', 'topic2', 'topic3']
    timestamp = 'mytime'
    config = update_influxdb_sink_config(config, topics, timestamp)

    return config


def test_influxdb_sink_config(config):
    """ Test influxdb-sink config """

    assert config['connect.influx.db'] == 'mydb'
    assert config['connect.influx.error.policy'] == 'NOOP'
    assert config['connect.influx.kcql'] == 'INSERT INTO topic1 SELECT * FROM'\
        ' topic1 WITHTIMESTAMP mytime;INSERT INTO topic2 SELECT * FROM topic2'\
        ' WITHTIMESTAMP mytime;INSERT INTO topic3 SELECT * FROM topic3'\
        ' WITHTIMESTAMP mytime'
    assert config['connect.influx.max.retries'] == '1'
    assert config['connect.influx.retry.interval'] == '1000'
    assert config['connect.influx.url'] == 'https://example.com'
    assert config['connect.influx.username'] == 'nobody'
    assert config['connector.class'] == 'com.datamountaineer.streamreactor.'\
        'connect.influx.InfluxSinkConnector'
    assert config['task.max'] == 1
    assert config['topics'] == 'topic1,topic2,topic3'


def test_influxdb_sink_cli():
    """Test the CLI for the influxdb-sink subcommand."""
    runner = CliRunner()
    create_result = runner.invoke(main.main, ['create'])
    assert create_result.exit_code == 0
    assert 'influxdb-sink' in create_result.output
    create_influxdb_sink_result = runner.invoke(main.main,
                                                ['create influxdb-sink'])
    assert create_influxdb_sink_result.exit_code == 2
