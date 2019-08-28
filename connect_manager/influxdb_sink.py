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

"""Manage the InfluxDB Sink connector.
"""

__all__ = ('create_influxdb_sink',)

import click


@click.command('influxdb-sink')
@click.argument('topics', nargs=-1, required=True)
@click.option(
    '--influxdb', 'influxdb', envvar='INFLUXDB', required=False,
    nargs=1, default='https://localhost:8086',
    show_default=True,
    help='InfluxDB URL. Alternatively set via $INFLUXDB env var.'
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
    help='InfluxDB username. Alternatively set via $INFLUXDB_USER env var. Use'
         ' \'-\' for unauthenticated users.'
)
@click.option(
    '--password', '-p', envvar='INFLUXDB_PASSWORD', default=None,
    help='InfluxDB password. Alternatively set via $INFLUXDB_PASSWORD env var.'
)
@click.option(
    '--dry-run', is_flag=True,
    help='Show the InfluxDB Sink Connector configuration but does not create '
         'the connector.'
)
@click.option(
    '--daemon', is_flag=True,
    help='Run in daemon mode monitoring the connector status.'
)
@click.option(
    '--auto-update', is_flag=True,
    help='Check for new Kafka topics and updates the connector configuration.'
)
@click.pass_context
def create_influxdb_sink(ctx, topics, influxdb, database, tasks,
                         username, password, dry_run, daemon):
    """Landoop InfluxDB Sink connector.
    """
    return 0
