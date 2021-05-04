"""CLI to create the MirrorMaker 2 connectors.

https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0
"""

__all__ = ["create_mirrormaker2"]

import json
import time

import click

from kafkaconnect.connect import Connect


@click.command("mirrormaker2")
@click.option(
    "-n",
    "--name",
    "name",
    default=None,
    show_default=True,
    help=(
        "Name of the MirroMaker 2 instance. "
        "If provided it is used as a prefix to name the heartbeat, checkpoint "
        "and mirror-source connectors and it overrides the ``name`` property "
        "value in the configuration file."
    ),
)
@click.option(
    "-h",
    "--heartbeat",
    "heartbeat_configfile",
    required=True,
    help=("Hertbeat connector configuration file."),
)
@click.option(
    "-c",
    "--checkpoint",
    "checkpoint_configfile",
    required=True,
    help=("Checkpoint connector configuration file."),
)
@click.option(
    "-m",
    "--mirror-source",
    "mirror_source_configfile",
    required=True,
    help=("MirrorSource connector configuration file."),
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
def create_mirrormaker2(
    ctx: click.Context,
    name: str,
    heartbeat_configfile: str,
    checkpoint_configfile: str,
    mirror_source_configfile: str,
    dry_run: bool,
    show_status: bool,
    show_status_interval: int,
) -> int:
    """Create an instance of the MirrorMaker 2 connectors.

    Create the heartbeat, checkpoint and mirror-source
    connectors. Use the --show-status option to output status.
    """
    # Get configuration from the main command
    if ctx.parent:
        config = ctx.parent.obj["config"]

    connect = Connect(config.connect_url)

    with open(heartbeat_configfile) as f:
        heartbeat_config = json.load(f)

    with open(checkpoint_configfile) as f:
        checkpoint_config = json.load(f)

    with open(mirror_source_configfile) as f:
        mirror_source_config = json.load(f)

    # Override connector name in the configuration
    if name:
        heartbeat_config["name"] = f"{name}-heartbeat"
        checkpoint_config["name"] = f"{name}-checkpoint"
        mirror_source_config["name"] = f"{name}-mirror-source"

    # Validate the configuration only.
    if dry_run:
        heartbeat_validation = connect.validate(
            name=heartbeat_config["connector.class"],
            connect_config=json.dumps(heartbeat_config),
        )
        click.echo(heartbeat_validation)
        checkpoint_validation = connect.validate(
            name=checkpoint_config["connector.class"],
            connect_config=json.dumps(checkpoint_config),
        )
        click.echo(checkpoint_validation)
        mirror_source_validation = connect.validate(
            name=mirror_source_config["connector.class"],
            connect_config=json.dumps(mirror_source_config),
        )
        click.echo(mirror_source_validation)
        return 0

    heartbeat_name = heartbeat_config["name"]
    click.echo(f"Creating the {heartbeat_name} connector...")
    click.echo(
        connect.validate_and_create(
            heartbeat_name, json.dumps(heartbeat_config)
        )
    )
    checkpoint_name = checkpoint_config["name"]
    click.echo(f"Creating the {checkpoint_name} connector...")
    click.echo(
        connect.validate_and_create(
            checkpoint_name, json.dumps(checkpoint_config)
        )
    )
    mirror_source_name = mirror_source_config["name"]
    click.echo(f"Creating the {mirror_source_name} connector...")
    click.echo(
        connect.validate_and_create(
            mirror_source_name, json.dumps(mirror_source_config)
        )
    )

    if show_status:
        while True:
            time.sleep(int(show_status_interval) / 1000)
            try:
                click.echo(connect.status(name=heartbeat_name))
                click.echo(connect.status(name=checkpoint_name))
                click.echo(connect.status(name=mirror_source_name))
            except KeyboardInterrupt:
                raise click.ClickException("Interruped.")

    return 0
