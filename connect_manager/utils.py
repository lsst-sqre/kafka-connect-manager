# This file is part of cp-kafka-connect-manager.
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

__all__ = ('get_broker_url', 'get_connector_url')

from click import ClickException


def get_broker_url(ctx):
    """Get the broker connection string from the context, or print an error
    message otherwise.
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


def get_connector_url(ctx):
    """Get the Confluent Kafka Connect connection string from the context, or
    print an error message otherwise.
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
