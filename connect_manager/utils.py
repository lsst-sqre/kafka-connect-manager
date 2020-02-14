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

"""Helpers for command-line tools.
"""

__all__ = ('get_broker_url', 'get_kafka_connect_url', 'get_existing_topics',
           'update_connector', 'get_connector_status')

import requests
import json

from click import ClickException
import confluent_kafka
from confluent_kafka.admin import AdminClient


def get_broker_url(ctx):
    """Get the broker connection string from the context, or print an error
    message otherwise.

    Parameters
    ==========
    ctx: `obj`
        Click context object.
    """
    try:
        broker_url = ctx.obj['broker_url']
    except KeyError:
        message = (
            'Broker is not configured. Pass a --broker option to kafkaefd '
            'or set the $BROKER environment variable. An example connection '
            'string is "localhost:9092".'
        )
        raise ClickException(message)
    return broker_url


def get_kafka_connect_url(ctx):
    """Get the Confluent Kafka Connect connection string from the context, or
    print an error message otherwise.

    Parameters
    ==========
    ctx : `obj`
        Click context object.
    """
    try:
        kafka_connect_url = ctx.obj['kafka_connect_url']
    except KeyError:
        message = (
            'kafka Connect is not configured. Pass a --kafka-connect option to'
            ' kafkaefd or set the $KAFKA_CONNECT environment variable. An '
            'example connection string is "https://localhost:8083".'
        )
        raise ClickException(message)
    return kafka_connect_url


def get_existing_topics(broker_url):
    """Get existing topics from Kafka.

    Parameters
    ==========
    broker_url : `str`
        Kafka broker URL.
    """

    broker_client = AdminClient({
        "bootstrap.servers": broker_url
    })
    existing_topics = []
    try:
        metadata = broker_client.list_topics(timeout=10)
        existing_topics = set(metadata.topics.keys())
    except confluent_kafka.KafkaException as err:
        message = err.args[0].str()
        raise ClickException(message)

    return existing_topics


def update_connector(kafka_connect_url, name, config):
    """Update a connector configuration.

    Parameters
    ==========
    kafka_connect_url : `str`
        Kafka connect URL.
    name : `str`
        Connector name.
    config : `json document`
        Connector configuration.
    """
    uri = f'{kafka_connect_url}/connectors/{name}/config'
    headers = {'Content-Type': 'application/json'}

    try:
        r = requests.put(uri, data=json.dumps(config), headers=headers)
        r.raise_for_status()
        print(json.dumps(r.json(), indent=4, sort_keys=True))
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


def get_connector_status(kafka_connect_url, name):
    """
    """
    uri = f'{kafka_connect_url}/connectors/{name}/status'
    try:
        r = requests.get(uri)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)

    status = json.dumps(r.json(), indent=4, sort_keys=True)
    return status
