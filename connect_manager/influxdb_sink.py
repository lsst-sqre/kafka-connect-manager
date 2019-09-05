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

"""Manage the Landoop InfluxDB Sink connector.
https://docs.lenses.io/connectors/sink/influx.html
"""

__all__ = ('create_influxdb_sink', 'make_connector_queries',
           'make_influxdb_sink_config',)

import click
import json
import time
import re

from .utils import (get_broker_url, get_kafka_connect_url,
                    update_connector, get_existing_topics,
                    get_connector_status)

CONNECTOR = 'influxdb-sink'


@click.command(CONNECTOR)
@click.argument('topics', nargs=-1, required=False)
@click.option(
    '--influxdb_url', 'influxdb_url', envvar='INFLUXDB', required=False,
    nargs=1, default='https://localhost:8086',
    show_default=True,
    help='InfluxDB connection URL. Alternatively set via $INFLUXDB env var.'
)
@click.option(
    '--database', '-d', default=None, required=True,
    help='InfluxDB database name. The database must exist at InfluxDB.'
)
@click.option(
    '--tasks', '-t', default=1,
    help='Number of Kafka Connect tasks.', show_default=True,
)
@click.option(
    '--username', '-u', envvar='INFLUXDB_USER', default='-',
    help=('InfluxDB username. Alternatively set via $INFLUXDB_USER env var.'
          'Use \'-\' for unauthenticated users.')
)
@click.option(
    '--password', '-p', envvar='INFLUXDB_PASSWORD', default=None,
    help='InfluxDB password. Alternatively set via $INFLUXDB_PASSWORD env var.'
)
@click.option(
    '--filter', '-f', 'filter_regex',
    help='Regex for selecting topics.'
)
@click.option(
    '--dry-run', is_flag=True,
    help=('Show the InfluxDB Sink Connector configuration but does not create '
          'the connector.')
)
@click.option(
    '--auto-update', is_flag=True,
    help=('Check for new Kafka topics and updates the connector configuration.'
          '--auto-update does not take effect if --dry-run is used.')
)
@click.option(
    '--check-interval', 'check_interval', default=15,
    help=('Time interval in seconds to check for new topics and update the '
          'connector.')
)
@click.option(
    '--blacklist', 'blacklist', multiple=True,
    help=('Blacklist problematic topics.')
)
@click.pass_context
def create_influxdb_sink(ctx, topics, influxdb_url, database, tasks,
                         username, password, filter_regex, dry_run,
                         auto_update, check_interval, blacklist):
    """The `Landoop InfluxDB Sink connector
    <https://docs.lenses.io/connectors/sink/influx.html>`_.

    Create connector configuration from a list of TOPICS. If not
    provided, TOPICS are discovered from Kafka.
    """
    broker_url = get_broker_url(ctx.parent.parent)
    topics = list(topics)
    if topics == []:
        click.echo("Discoverying Kafka topics...")
        topics = get_existing_topics(broker_url)

    if filter_regex:
        pattern = re.compile(filter_regex)
        topics = [t for t in topics if pattern.match(t)]

    if blacklist:
        for blacklisted_topic in blacklist:
            topics.remove(blacklisted_topic)

    config = make_influxdb_sink_config(topics, influxdb_url, database,
                                       tasks, username, password)

    if dry_run:
        click.echo(json.dumps(config, indent=4, sort_keys=True))
        return 0

    kafka_connect_url = get_kafka_connect_url(ctx.parent.parent)

    click.echo("Creating the connector...")
    update_connector(kafka_connect_url, CONNECTOR, config)
    status = get_connector_status(kafka_connect_url, CONNECTOR)
    click.echo(status)
    if auto_update:
        while True:
            time.sleep(check_interval)
            try:
                current_topics = get_existing_topics(broker_url)
                # apply the same filter here
                if filter_regex:
                    pattern = re.compile(filter_regex)
                    current_topics = [t for t in current_topics
                                      if pattern.match(t)]

                if blacklist:
                    for blacklisted_topic in blacklist:
                        current_topics.remove(blacklisted_topic)

                # topics in current_topics but not in topics
                new_topics = list(set(current_topics) - set(topics))
                if new_topics:
                    click.echo('Found new topics, updating the connector...')
                    config = make_influxdb_sink_config(current_topics,
                                                       influxdb_url,
                                                       database,
                                                       tasks,
                                                       username,
                                                       password)
                    update_connector(kafka_connect_url, CONNECTOR,
                                     config)
                    status = get_connector_status(kafka_connect_url,
                                                  CONNECTOR)
                    click.echo(status)
                    topics = current_topics
            except KeyboardInterrupt:
                raise click.ClickException('Interruped.')
    return 0


def make_connector_queries(topics, time_field=None):
    """Make the kafka connector queries. It assumes that the topic structure
    is flat  (`SELECT * FROM`).

    Parameters
    ----------
    topics : `list`
        List of kafka topics.
    time_field : `str`
        Uses an existing field or the system time as the InfluxDB timestamp.
    """
    query_template = 'INSERT INTO {} SELECT * FROM {} WITHTIMESTAMP sys_time()'

    if time_field:
        query_template = ('INSERT INTO {} SELECT * FROM {} WITHTIMESTAMP '
                          '{timestamp_field}')

    queries = [query_template.format(topic, topic) for topic in topics]

    return ";".join(queries)


def make_influxdb_sink_config(topics, influxdb_url, database, tasks,
                              username, password):
    """Make InfluxDB Sink connector configuration.

    Parameters
    ----------
    topics : `list`
        List of Kafka topics to add to the connector.
    influxdb_url : `str`
        InfluxDB connection URL.
    database : `str`
        InfluxDB database name.
    tasks : `int`
        Number of Kafka connect tasks.
    username : `str`
        InfluxDB username.
    password : `str`
        InfluxDB password.
    """
    config = {}
    config['connector.class'] = 'com.datamountaineer.streamreactor.'\
                                'connect.influx.InfluxSinkConnector'
    config['task.max'] = tasks
    # Ensure uniqueness and sort
    topics = list(set(topics))
    topics.sort()
    config['topics'] = ','.join(topics)
    config['connect.influx.url'] = influxdb_url
    config['connect.influx.db'] = database

    queries = make_connector_queries(topics)
    config['connect.influx.kcql'] = queries
    config['connect.influx.username'] = username

    if password:
        config['connect.influx.password'] = password

    return config
