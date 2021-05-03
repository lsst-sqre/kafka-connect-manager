"""CLI to create the JDBC Sink connector.

https://docs.confluent.io/kafka-connect-jdbc/current/sink-connector/index.html
"""

__all__ = ["create_jdbc_sink"]

import json
import time

import click

from kafkaconnect.connect import Connect


@click.command("jdbc-sink")
@click.argument("configfile")
@click.option(
    "-n",
    "--name",
    "name",
    default=None,
    show_default=True,
    help=(
        "Name of the JDBC Sink connector. "
        "If provided it overrides the ``name`` property "
        "value in the configuration file."
    ),
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    help=("Validates the connector configuration without creating."),
)
@click.option(
    "--show-status",
    "show_status",
    is_flag=True,
    help=(
        "Show connector status in the output. See also the "
        "``--show-status-interval`` option."
    ),
)
@click.option(
    "--show-status-interval",
    "show_status_interval",
    default=15000,
    show_default=True,
    help=("The time interval in milliseconds to output the connector status."),
)
@click.pass_context
def create_jdbc_sink(
    ctx: click.Context,
    configfile: str,
    name: str,
    dry_run: bool,
    show_status: bool,
    show_status_interval: int,
) -> int:
    """Create an instance of the JDBC Sink connector.

    Use the --show-status option to output status.
    """
    # Get configuration from the main command
    if ctx.parent:
        config = ctx.parent.obj["config"]

    connect = Connect(config.connect_url)

    with open(configfile) as f:
        config = json.load(f)

    # Override connector name in the configuration
    if name:
        config["name"] = name

    # Validate the configuration only.
    if dry_run:
        validation = connect.validate(
            name=config["connector.class"], connect_config=json.dumps(config),
        )
        click.echo(validation)
        return 0

    _name = config["name"]
    click.echo(f"Creating the {_name} connector...")
    click.echo(connect.validate_and_create(_name, json.dumps(config)))
    if show_status:
        while True:
            time.sleep(int(show_status_interval) / 1000)
            try:
                click.echo(connect.status(name=_name))
            except KeyboardInterrupt:
                raise click.ClickException("Interruped.")

    return 0
