"""CLI to create the S3 Sink connector.

See https://docs.confluent.io/current/connect/kafka-connect-s3
"""

__all__ = ["create_s3_sink"]

import json
import time

import click

from kafkaconnect.connect import Connect


@click.command("s3-sink")
@click.argument("configfile")
@click.option(
    "-n",
    "--name",
    "name",
    default=None,
    help=(
        "Name of the S3 Sink connector. "
        "If provided it overrrides the ``name`` property "
        "value in the configuration file."
    ),
)
@click.option(
    "--aws-access-key-id",
    "aws_access_key_id",
    envvar="AWS_ACCESS_KEY_ID",
    default=None,
    help=(
        "The AWS access key ID used to authenticate personal AWS credentials."
    ),
)
@click.option(
    "--aws-secret-access-key",
    "aws_secret_access_key",
    envvar="AWS_SECRET_ACCESS_KEY",
    default=None,
    help=(
        "The secret access key used to authenticate personal AWS credentials."
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
def create_s3_sink(
    ctx: click.Context,
    configfile: str,
    name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    dry_run: bool,
    show_status: bool,
    show_status_interval: int,
) -> int:
    """Create an instance of the S3 Sink connector.

    Use the --show-status option to output status.
    """
    # Get configuration from the parent command
    if ctx.parent:
        parent_config = ctx.parent.obj["config"]

    connect = Connect(parent_config.connect_url)

    with open(configfile) as f:
        config = json.load(f)

    if name:
        click.echo("Updating connector name.")
        config["name"] = name

    if None in (aws_access_key_id, aws_secret_access_key):
        click.echo(
            "Could not get the AWS credentials. "
            "Use the --access-key-id and --aws-secret-access-key options "
            "or set the AWS credentials using the AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY env variables."
        )
        return 1

    config["aws.access.key.id"] = aws_access_key_id
    config["aws.secret.access.key"] = aws_secret_access_key

    # Validate the configuration only.
    if dry_run:
        validation = connect.validate(
            name=config["connector.class"],
            connect_config=json.dumps(config),
        )
        click.echo(validation)
        return 0

    name = config["name"]
    click.echo(f"Creating the {name} connector...")
    click.echo(connect.validate_and_create(name, json.dumps(config)))
    if show_status:
        while True:
            time.sleep(int(show_status_interval) / 1000)
            try:
                click.echo(connect.status(name=name))
            except KeyboardInterrupt:
                raise click.ClickException("Interruped.")

    return 0
