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

__all__ = ('create_influxdb_sink', 'update_influxdb_sink_config',
           'make_influxdb_sink_config',)

import click
import json
import time

from .utils import (get_broker_url, get_kafka_connect_url,
                    update_connector, get_topics,
                    get_connector_status)


@click.command('influxdb-sink')
@click.argument('topics', nargs=-1, required=False)
@click.option(
    '--name', 'name', required=False, default='influxdb-sink',
    show_default=True,
    help='Name of the connector to create.'
)
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
@click.option(
    '--timestamp', 'timestamp', default='sys_time()',
    help=('Timestamp to use when recording the message in InfluxDB.'),
    show_default=True
)
@click.option(
    '--error-policy', 'error_policy',
    type=click.Choice(['NOOP', 'THROW', 'RETRY']), default='THROW',
    help=('Specifies the action to be taken if an error occurs while '
          'inserting the data. There are three available options, NOOP, '
          'the error is swallowed, THROW, the error is allowed to propagate '
          'and RETRY. For RETRY the Kafka message is redelivered up to a '
          'maximum number of times specified by the --max-retries option. '
          'The retry interval is specified by the --retry-interval option.'),
    show_default=True
)
@click.option(
    '--max-retries', 'max_retries', default='10',
    help=('The maximum number of times a message is retried. Only valid when '
          'the --error-policy is set to RETRY.'),
    show_default=True
)
@click.option(
    '--retry-interval', 'retry_interval', default='60000',
    help=('The interval, in milliseconds between retries. Only valid when '
          'the --error-policy is set to RETRY.'),
    show_default=True
)
@click.pass_context
def create_influxdb_sink(ctx, topics, name, influxdb_url, database, tasks,
                         username, password, filter_regex, dry_run,
                         auto_update, check_interval, blacklist,
                         timestamp, error_policy, max_retries, retry_interval):
    """Create an instance of the Stream Reactor InfluxDB Sink Connector.

    The TOPICS argument specifies the list of topics to write to InfluxDB.
    If not provided, topics are discovered from Kafka. In this case, use the
    --filter option to regex the topics you want to write to InfluxDB.
    """
    broker_url = get_broker_url(ctx.parent.parent)
    topics = list(topics)
    if topics == []:
        click.echo("Discoverying Kafka topics...")
        topics = get_topics(broker_url, filter_regex, blacklist)

    click.echo("Found {} topics.".format(len(topics)))

    config = make_influxdb_sink_config(influxdb_url,
                                       database, tasks, username,
                                       password, error_policy,
                                       max_retries, retry_interval)
    if topics:
        config = update_influxdb_sink_config(config, topics, timestamp)

        if dry_run:
            click.echo(json.dumps(config, indent=4, sort_keys=True))
            return 0

        kafka_connect_url = get_kafka_connect_url(ctx.parent.parent)

        click.echo("Updating the connector...")
        update_connector(kafka_connect_url, name, config)
        status = get_connector_status(kafka_connect_url, name)
        click.echo(status)

    if auto_update:
        while True:
            time.sleep(check_interval)
            try:
                current_topics = get_topics(broker_url, filter_regex,
                                            blacklist)
                new_topics = list(set(current_topics) - set(topics))
                if new_topics:
                    click.echo('Found new topics, updating the connector...')
                    config = update_influxdb_sink_config(config,
                                                         current_topics,
                                                         timestamp)
                    update_connector(kafka_connect_url, name, config)
                    status = get_connector_status(kafka_connect_url, name)
                    click.echo(status)
                    topics = current_topics
            except KeyboardInterrupt:
                raise click.ClickException('Interruped.')
    return 0


def update_influxdb_sink_config(config, topics, timestamp=''):
    """Update the InfluxDB connector configuration, adding a list of
    topics and the corresponding InfluxDB KCQL queries.
    We assume that the topic structure is flat, i.e `SELECT * FROM` will
    retrieve the topic fields.

    Parameters
    ----------
    config : `dict`
        A configuration dictionary as retuned by `make_influxdb_sink_config()`
    topics : `list`
        List of kafka topics.
    timestamp : `str`
        Use timestamp as the the InfluxDB timestamp.
    """
    # Ensure uniqueness and sort topic names
    topics = list(set(topics))
    topics.sort()
    config['topics'] = ','.join(topics)
    queries = [f'INSERT INTO {t} SELECT * FROM {t} WITHTIMESTAMP {timestamp}'
               for t in topics]
    config['connect.influx.kcql'] = ";".join(queries)

    return config


def make_influxdb_sink_config(influxdb_url, database, tasks,
                              username, password, error_policy,
                              max_retries, retry_interval):
    """Make InfluxDB Sink connector configuration.

    Parameters
    ----------
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
    error_policy : `str`
        See connector error policy configuration.
    max_retries : `str`
        See connector error policy configuration.
    retry_interval : `str`
        See connector error policy configuration.

    """
    config = {}
    config['connector.class'] = 'com.datamountaineer.streamreactor.'\
                                'connect.influx.InfluxSinkConnector'
    config['task.max'] = tasks
    config['connect.influx.url'] = influxdb_url
    config['connect.influx.db'] = database
    config['connect.influx.username'] = username

    if password:
        config['connect.influx.password'] = password

    config['connect.influx.error.policy'] = error_policy
    config['connect.influx.max.retries'] = max_retries
    config['connect.influx.retry.interval'] = retry_interval

    return config
