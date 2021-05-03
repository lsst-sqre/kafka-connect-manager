"""Kafkaconnect Command Line Interface."""

__all__ = (
    "main",
    "list",
    "info",
    "status",
    "config",
    "tasks",
    "topics",
    "plugins",
    "pause",
    "resume",
    "delete",
    "help",
    "create",
)

import json
from typing import Any, Optional

import click

from kafkaconnect.config import Config
from kafkaconnect.connect import Connect
from kafkaconnect.influxdb_sink.cli import create_influxdb_sink
from kafkaconnect.jdbc_sink.cli import create_jdbc_sink
from kafkaconnect.mirrormaker2.cli import create_mirrormaker2
from kafkaconnect.s3_sink.cli import create_s3_sink

# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-b",
    "--broker",
    "broker_url",
    envvar="KAFKA_BROKER_URL",
    default="localhost:9092",
    show_default=True,
    help="Kafka Broker URL. Alternatively set via $KAFKA_BROKER_URL env var.",
)
@click.option(
    "-c",
    "--connect",
    "connect_url",
    envvar="KAFKA_CONNECT_URL",
    default="http://localhost:8083",
    show_default=True,
    help=(
        "Kafka Connect URL. Alternatively set via $KAFKA_CONNECT_URL env var."
    ),
)
@click.version_option(message="%(version)s")
@click.pass_context
def main(ctx: click.Context, broker_url: str, connect_url: str) -> None:
    """Command-line interface for kafkaconnect.

    kafkaconnect is a Connect API client that helps to configure and
    manage Kafka connectors.
    """
    config = Config(broker_url=broker_url, connect_url=connect_url)
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


@main.command("list")
@click.pass_context
def list(ctx: click.Context) -> None:
    """Get a list of active connectors."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.list())


@main.command("info")
@click.argument("name")
@click.pass_context
def info(ctx: click.Context, name: str) -> None:
    """Get information about the connector."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.info(name))


@main.command("status")
@click.argument("name")
@click.pass_context
def status(ctx: click.Context, name: str) -> None:
    """Get the connector status."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.status(name))


@main.command("config")
@click.argument("name")
@click.pass_context
def config(ctx: click.Context, name: str) -> None:
    """Get the connector configuration."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.config(name))


@main.command("tasks")
@click.argument("name")
@click.pass_context
def tasks(ctx: click.Context, name: str) -> None:
    """Get a list of tasks currently running for the connector."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.tasks(name))


@main.command("topics")
@click.argument("name")
@click.pass_context
def topics(ctx: click.Context, name: str) -> None:
    """Get the list of topic names used by the connector."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.topics(name))


@main.command("plugins")
@click.pass_context
def plugins(ctx: click.Context) -> None:
    """Get a list of connector plugins available in the Connect cluster."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.plugins())


@main.command("restart")
@click.argument("name")
@click.pass_context
def restart(ctx: click.Context, name: str) -> None:
    """Restart a connector and its tasks."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.restart(name))


@main.command("pause")
@click.argument("name")
@click.pass_context
def pause(ctx: click.Context, name: str) -> None:
    """Pause the connector and its tasks."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.pause(name))


@main.command("resume")
@click.argument("name")
@click.pass_context
def resume(ctx: click.Context, name: str) -> None:
    """Resume a paused connector."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.resume(name))


@main.command("delete")
@click.argument("name")
@click.pass_context
def delete(ctx: click.Context, name: str) -> None:
    """Delete a connector.

    Halt tasks and remove the connector configuration.
    """
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)
    click.echo(connect.remove(name))


@main.command("upload")
@click.argument("configfile")
@click.option(
    "-n",
    "--name",
    "name",
    required=True,
    help=(
        "Name of the connector. Alternatively set via the "
        "$KAFKA_CONNECT_NAME env var."
    ),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=("Validate the connector configuration without uploading."),
)
@click.pass_context
def upload(
    ctx: click.Context, configfile: str, name: str, dry_run: bool,
) -> int:
    """Upload the connector configuration from a file."""
    config = ctx.obj["config"]
    connect = Connect(config.connect_url)

    with open(configfile) as f:
        connect_config = json.load(f)

    # Ensure connector name is consistent
    connect_config["name"] = name

    # Validate the connector configuration only.
    if dry_run:
        validation = connect.validate(
            name=connect_config["connector.class"],
            connect_config=json.dumps(connect_config),
        )
        click.echo(validation)
        return 0

    click.echo(f"Uploading {name} connector configuration...")
    click.echo(connect.validate_and_create(name, json.dumps(connect_config)))
    return 0


@main.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx: click.Context, topic: Optional[str], **kw: Any) -> None:
    """Show help for any command."""
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic:
        if topic in main.commands:
            ctx.info_name = topic
            click.echo(main.commands[topic].get_help(ctx))
        else:
            raise click.UsageError(f"Unknown help topic {topic}", ctx)
    else:
        assert ctx.parent
        click.echo(ctx.parent.get_help())


@main.group()
@click.pass_context
def create(ctx: click.Context) -> None:
    """Create a new connector.

    Each subcommand creates a different connector.
    """


# Add subcommands from other modules
create.add_command(create_influxdb_sink)
create.add_command(create_s3_sink)
create.add_command(create_mirrormaker2)
create.add_command(create_jdbc_sink)
