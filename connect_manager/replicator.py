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

"""Manage the Confluent Replicator connector.
https://docs.confluent.io/current/connect/kafka-connect-replicator/index.html
"""

__all__ = ('create_replicator', 'make_replicator_config',)

import click
import json
import time

from .utils import (get_kafka_connect_url, update_connector,
                    get_connector_status)


@click.command('replicator')
@click.argument('topics', nargs=-1, required=False)
@click.option(
    '--name', 'name', required=False, default='replicator',
    show_default=True,
    help='Name of the connector to create.'
)
@click.option(
    '--src-kafka', required=True,
    nargs=1,
    help=('A list of host and port pairs to use for establishing the initial '
          'connection to the source Kafka cluster. This list must be in the '
          'form `host1:port1,host2:port2,...`.')
)
@click.option(
    '--dest-kafka', required=True, nargs=1,
    help=('A list of host and port pairs to use for establishing the initial '
          'connection to the destination Kafka cluster. This list must be in '
          'the form `host1:port1,host2:port2,...`.')
)
@click.option(
    '--topic-rename-format', default="${topic}",
    nargs=1, required=False, show_default=True,
    help='A format string for the topic name in the destination cluster, '
         'which may contain ${topic} as a placeholder for the originating '
         'topic name, e.g. `summit_${topic}`.'
)
@click.option(
    '--tasks', '-t', default=1,
    help='Number of Kafka Connect tasks.', show_default=True,
)
@click.option(
    '--schema-registry-topic', default='_schemas', show_default=True,
    help=('The topic that acts as the durable log for the schema registry.')
)
@click.option(
    '--schema-registry-url', default=None, required=True,
    help=('Comma-separated list of URLs for schema registry instances that '
          'can be used to register or look up schemas. If the replicator is'
          ' configured in the destination cluster this should be the URL '
          ' for the destination schema registry which configured in IMPORT '
          ' mode.')
)
@click.option(
    '--group-id', default=None,
    help=('If the replicator needs to run on a separate Connect cluster, '
          'the `group.id` property specifies which workers to use.')
)
@click.option(
    '--filter', '-f', 'filter_regex', required=True,
    help='Regex of topics to replicate to the destination cluster.'
)
@click.option(
    '--dry-run', is_flag=True,
    help=('Show the InfluxDB Sink Connector configuration but does not create '
          'the connector.')
)
@click.option(
    '--blacklist', 'blacklist', multiple=True,
    help=('Topics to exclude from replication. Note that Kafka internal '
          'topics are not replicated by default.')
)
@click.option(
    '--check-interval', 'check_interval', default='120000', show_default=True,
    help=('How often to poll the source cluster for new topics matching '
          'the --filer regex, in milliseconds.')
)
@click.pass_context
def create_replicator(ctx, topics, name, src_kafka, dest_kafka,
                      topic_rename_format, tasks, schema_registry_topic,
                      schema_registry_url, group_id, filter_regex,
                      dry_run, blacklist, check_interval):
    """Create an instance of the Replicator Connector.

    The TOPICS argument specifies the list of topics to replicate. If
    provided, they are added to the whitelist. If not, only topics matching
    the --filter regex option will be replicated. Whitelisted topics do not
    have to match the regex.
    """
    topics = list(topics)
    blacklist = list(blacklist)
    config = make_replicator_config(topics, src_kafka, dest_kafka,
                                    topic_rename_format, tasks,
                                    schema_registry_topic, schema_registry_url,
                                    group_id, filter_regex, blacklist,
                                    check_interval)
    if dry_run:
        click.echo(json.dumps(config, indent=4, sort_keys=True))
        return 0

    kafka_connect_url = get_kafka_connect_url(ctx.parent.parent)

    click.echo("Updating the connector...")
    update_connector(kafka_connect_url, name, config)

    while True:
        time.sleep(int(check_interval) / 1000)
        try:
            status = get_connector_status(kafka_connect_url, name)
            click.echo(status)
        except KeyboardInterrupt:
            raise click.ClickException('Interruped.')


def make_replicator_config(topics, src_kafka, dest_kafka,
                           topic_rename_format, tasks,
                           schema_registry_topic, schema_registry_url,
                           group_id, filter_regex, blacklist,
                           check_interval):
    """Make Replicator connector configuration.

    Parameters
    ----------
    topics : `list`
        List of topics to whitelist.
    src_kafka : `str`
        Source Kafka broker.
    dest_kafka : `str`
        Destination kafka broker.
    topic_rename_format : `str`
        Format string for destination topics, e.g. `summit_$(topic)`.
    tasks : `int`
        Number of Kafka connect tasks.
    schema_registry_url : `str`
        Schema registry URL for the destination cluster.
    group_id : `str`
        Kafka Connect group.id
    filter_regex : `str`
        Regex of topics to replicate to the destination cluster.
    blacklist : `str`
        Topics to exclude from replication.
    check_interval : `int`
        How often to poll the source cluster for new topics.
    """
    DEFAULT_CONVERTER = 'io.confluent.connect.replicator.util.'\
        'ByteArrayConverter'
    config = {}
    config['connector.class'] = 'io.confluent.connect.replicator.'\
        'ReplicatorSourceConnector'
    config['task.max'] = tasks
    config['key.converter'] = DEFAULT_CONVERTER
    config['value.converter'] = DEFAULT_CONVERTER
    config['header.coverter'] = DEFAULT_CONVERTER
    config['schema.registry.topic'] = schema_registry_topic
    config['topic.regex'] = filter_regex

    # Ensure uniqueness and sort topic names
    topics = list(set(topics))
    topics.sort()

    # The schema registry topic must be whitelisted explicitly
    topics.append(schema_registry_topic)
    config['topic.whitelist'] = ",".join(topics)

    if blacklist:
        config['topic.blacklist'] = ",".join(blacklist)

    config['topic.rename.format'] = topic_rename_format
    config['topic.poll.interval.ms'] = check_interval
    config['src.kafka.bootstrap.servers'] = src_kafka
    config['dest.kafka.bootstrap.servers'] = dest_kafka

    config['schema.subject.translator.class'] = 'io.confluent.connect.'\
        'replicator.schemas.DefaultSubjectTranslator'

    config['schema.registry.url'] = schema_registry_url

    if group_id:
        config['src.consumer.group.id'] = group_id

    return config
