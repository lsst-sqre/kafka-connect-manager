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

"""Main commands for connect_manager.
   See also https://docs.confluent.io/current/connect/references/restapi.html
"""

__all__ = ('main', 'create', 'delete', 'restart', 'pause', 'resume', 'list',
           'status', 'info', 'help')

import click
from click import ClickException


import requests
import json

from .influxdb_sink import create_influxdb_sink
from .replicator import create_replicator
from .utils import get_kafka_connect_url, get_connector_status


# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--broker', 'broker_url', envvar='BROKER', required=False, nargs=1,
    default='confluent-kafka-cp-kafka-headless:9092',
    show_default=True,
    help='Kafka broker. Alternatively set via $BROKER env var.'
)
@click.option(
    '--kafka-connect', 'kafka_connect_url', envvar='KAFKA_CONNECT',
    required=False, nargs=1,
    default='http://confluent-kafka-cp-kafka-connect:8083',
    show_default=True,
    help='Kafka Connect URL. Alternatively set via $KAFKA_CONNECT env var.'
)
@click.version_option(message='%(version)s')
@click.pass_context
def main(ctx, broker_url, kafka_connect_url):
    """connect_manager is a CLI for the `Confluent Kafka Connect REST API
    <https://docs.confluent.io/current/connect/references/restapi.html>`_,
    it makes it easy to manage connectors.
    """
    # Subcommands should use the click.pass_obj decorator to get this
    # ctx object as the first argument.
    ctx.obj = {
        'broker_url': broker_url,
        'kafka_connect_url': kafka_connect_url,
    }
    return 0


@main.group()
@click.pass_context
def create(ctx):
    """Create a new connector. Each create subcommand manages a different
    connector.
    """


@main.command('delete')
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """Delete a connector.

    Halt all tasks and delete the connector configuration.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors/{name}'

    try:
        r = requests.delete(uri)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
        # returns 409 (Conflict) if rebalance is in process.
        elif err.response.status_code == 409:
            message = (f'Could not delete {name}. Rebalance is '
                       'in process.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


@main.command('restart')
@click.argument('name')
@click.pass_context
def restart(ctx, name):
    """Restart a connector and its tasks.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors/{name}/restart'

    try:
        r = requests.post(uri)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
        # returns 409 (Conflict) if rebalance is in process.
        elif err.response.status_code == 409:
            message = (f'Could not delete {name} connector. Rebalance is '
                       'in process.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


@main.command('pause')
@click.argument('name')
@click.pass_context
def pause(ctx, name):
    """Pause the connector and its tasks.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors/{name}/pause'

    try:
        r = requests.put(uri)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


@main.command('resume')
@click.argument('name')
@click.pass_context
def resume(ctx, name):
    """Resume a paused connector.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors/{name}/resume'

    try:
        r = requests.put(uri)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


@main.command('list')
@click.pass_context
def list(ctx):
    """Get a list of active connectors.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors'

    try:
        r = requests.get(uri)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)

    connectors = r.json()
    for name in connectors:
        click.echo(name)


@main.command('status')
@click.argument('name')
@click.pass_context
def status(ctx, name):
    """Get current status of the connector.

    Whether it is running, failed or paused, which worker it is assigned to,
    error information if it has failed, and the state of all its tasks.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    status = get_connector_status(kafka_connect_url, name)
    click.echo(status)


@main.command('info')
@click.argument('name')
@click.pass_context
def info(ctx, name):
    """Get information about the connector.
    """
    kafka_connect_url = get_kafka_connect_url(ctx.parent)
    uri = f'{kafka_connect_url}/connectors/{name}'
    r = requests.get(uri)

    try:
        r.raise_for_status()
        click.echo(json.dumps(r.json(), indent=4, sort_keys=True))
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:
            message = (f'Connector {name} not found.')
            raise ClickException(message)
    except requests.exceptions.ConnectionError:
        message = (f'Failed to establish connection with {kafka_connect_url}.')
        raise ClickException(message)


@main.command()
@click.argument('topic', default=None, required=False, nargs=1)
@click.pass_context
def help(ctx, topic, **kw):
    """Show help for any command.
    """
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic is None:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(main.commands[topic].get_help(ctx))


# Add subcommands from other modules
create.add_command(create_influxdb_sink)
create.add_command(create_replicator)
