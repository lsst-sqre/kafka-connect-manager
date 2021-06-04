"""CLI to create the InfluxDB Sink connector.

See https://docs.lenses.io/connectors/sink/influx.html.
"""

__all__ = ["create_influxdb_sink"]

import json
import time
from typing import List

import click

from kafkaconnect.connect import Connect
from kafkaconnect.influxdb_sink.config import InfluxConfig
from kafkaconnect.topics import Topic


@click.command("influxdb-sink")
@click.argument("topiclist", nargs=-1, required=False)
@click.option(
    "-n",
    "--name",
    "name",
    envvar="KAFKA_CONNECT_NAME",
    default="influxdb-sink",
    show_default=True,
    help=(
        "Name of the connector."
        "The connector name must be unique accross the cluster."
        "Alternatively set via the $KAFKA_CONNECT_NAME env var."
    ),
)
@click.option(
    "-i",
    "--influxdb_url",
    "connect_influx_url",
    envvar="KAFKA_CONNECT_INFLUXDB_URL",
    default="http://localhost:8086",
    show_default=True,
    help=(
        "InfluxDB connection URL. Alternatively set via the "
        "$KAFKA_CONNECT_INFLUXDB_URL env var."
    ),
)
@click.option(
    "-d",
    "--database",
    "connect_influx_db",
    envvar="KAFKA_CONNECT_DATABASE",
    default="mydb",
    show_default=True,
    help=(
        "InfluxDB database name. The database must exist at InfluxDB. "
        "Alternatively set via the $KAFKA_CONNECT_DATABASE env var."
    ),
)
@click.option(
    "-t",
    "--tasks-max",
    "tasks_max",
    envvar="KAFKA_CONNECT_TASKS_MAX",
    default="1",
    show_default=True,
    help=(
        "Number of Kafka Connect tasks. Alternatively set via the "
        "$KAFKA_CONNECT_TASKS_MAX env var."
    ),
)
@click.option(
    "-u",
    "--username",
    "connect_influx_username",
    envvar="KAFKA_CONNECT_INFLUXDB_USERNAME",
    default="-",
    show_default=True,
    help=(
        "InfluxDB username. Alternatively set via the "
        "$KAFKA_CONNECT_INFLUXDB_USERNAME env var. "
        "Use '-' for unauthenticated users."
    ),
)
@click.option(
    "-p",
    "--password",
    "connect_influx_password",
    envvar="KAFKA_CONNECT_INFLUXDB_PASSWORD",
    default="",
    show_default=True,
    help=(
        "InfluxDB password. Alternatively set via the "
        "$KAFKA_CONNECT_INFLUXDB_PASSWORD env var."
    ),
)
@click.option(
    "-r",
    "--topic-regex",
    "topic_regex",
    envvar="KAFKA_CONNECT_TOPIC_REGEX",
    default=".*",
    show_default=True,
    help=(
        "Regex for selecting topics. Alternatively set via the "
        "$KAFKA_CONNECT_TOPIC_REGEX env var."
    ),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "Show the InfluxDB Sink Connector configuration but do not create "
        "the connector."
    ),
)
@click.option(
    "--auto-update",
    is_flag=True,
    help=(
        "Check for new topics and update the connector. See also the "
        "--check-interval option."
    ),
)
@click.option(
    "-v",
    "--validate",
    is_flag=True,
    help="Validate the connector configuration before creating.",
)
@click.option(
    "-c",
    "--check-interval",
    "check_interval",
    envvar="KAFKA_CONNECT_CHECK_INTERVAL",
    default="15000",
    show_default=True,
    help=(
        "The interval, in milliseconds, to check for new topics and update"
        "the connector. Alternatively set via the "
        "$KAFKA_CONNECT_CHECK_INTERVAL env var."
    ),
)
@click.option(
    "-e",
    "--excluded_topic_regex",
    "excluded_topic_regex",
    envvar="KAFKA_CONNECT_EXCLUDED_TOPIC_REGEX",
    default="",
    show_default=True,
    help=(
        "Regex for excluding topics. Alternatively set via the "
        "$KAFKA_CONNECT_EXCLUDED_TOPIC_REGEX env var."
    ),
)
@click.option(
    "--error-policy",
    "connect_influx_error_policy",
    type=click.Choice(["NOOP", "THROW", "RETRY"]),
    envvar="KAFKA_CONNECT_ERROR_POLICY",
    default="THROW",
    show_default=True,
    help=(
        "Specifies the action to be taken if an error occurs while "
        "inserting the data. There are three available options, NOOP, "
        "the error is swallowed, THROW, the error is allowed to propagate "
        "and RETRY. For RETRY the Kafka message is redelivered up to a "
        "maximum number of times specified by the ``--max-retries`` option. "
        "The retry interval is specified by the ``--retry-interval`` option. "
        "Alternatively set via the $KAFKA_CONNECT_ERROR_POLICY env var."
    ),
)
@click.option(
    "--max-retries",
    "connect_influx_max_retries",
    envvar="KAFKA_CONNECT_MAX_RETRIES",
    default="10",
    show_default=True,
    help=(
        "The maximum number of times a message is retried. Only valid when "
        "the ``--error-policy`` is set to RETRY. Alternatively set via the "
        "$KAFKA_CONNECT_MAX_RETRIES env var."
    ),
)
@click.option(
    "--retry-interval",
    "connect_influx_retry_interval",
    envvar="KAFKA_CONNECT_RETRY_INTERVAL",
    default="60000",
    show_default=True,
    help=(
        "The interval, in milliseconds between retries. Only valid when "
        "the ``--error-policy`` is set to RETRY. Alternatively set via the "
        "$KAFKA_CONNECT_RETRY_INTERVAL env var."
    ),
)
@click.option(
    "--progress-enabled",
    "connect_progress_enabled",
    envvar="KAFKA_CONNECT_PROGRESS_ENABLED",
    default="false",
    show_default=True,
    help=(
        "Enables the output for how many records have been processed. "
        "Alternatively set via the $KAFKA_CONNECT_PROGRESS_ENABLED env var."
    ),
)
@click.option(
    "--timestamp",
    "timestamp",
    envvar="KAFKA_CONNECT_INFLUXDB_TIMESTAMP",
    default="sys_time()",
    show_default=True,
    help="Timestamp to use as the InfluxDB time.",
)
@click.pass_context
def create_influxdb_sink(
    ctx: click.Context,
    topiclist: tuple,
    name: str,
    connect_influx_url: str,
    connect_influx_db: str,
    tasks_max: str,
    connect_influx_username: str,
    connect_influx_password: str,
    topic_regex: str,
    dry_run: bool,
    auto_update: bool,
    validate: bool,
    check_interval: str,
    excluded_topic_regex: str,
    connect_influx_error_policy: str,
    connect_influx_max_retries: str,
    connect_influx_retry_interval: str,
    connect_progress_enabled: str,
    timestamp: str,
) -> int:
    """Create an instance of the InfluxDB Sink connector.

    A list of topics can be specified using the TOPICLIST argument.
    If not, topics are discovered from Kafka. Use the ``--topic-regex`` and
    ``--excluded_topics`` options to help in selecting the topics
    that you want to write to InfluxDB. To check for new topics and update
    the connector configuration use the
    ``--auto-update`` and ``--check-interval`` options.
    """
    # Get configuration from the main command
    if ctx.parent:
        config = ctx.parent.obj["config"]
    # Connector configuration
    influx_config = InfluxConfig(
        name=name,
        connect_influx_url=connect_influx_url,
        connect_influx_db=connect_influx_db,
        tasks_max=int(tasks_max),
        connect_influx_username=connect_influx_username,
        connect_influx_password=connect_influx_password,
        connect_influx_error_policy=connect_influx_error_policy,
        connect_influx_max_retries=connect_influx_max_retries,
        connect_influx_retry_interval=connect_influx_retry_interval,
        connect_progress_enabled=(connect_progress_enabled == "true"),
    )
    # The variadic argument is a tuple
    topics: List[str] = list(topiclist)
    if not topics:
        click.echo("Discoverying Kafka topics...")
        topics = Topic(
            config.broker_url, topic_regex, excluded_topic_regex
        ).names
        n = 0 if not topics else len(topics)
        click.echo(f"Found {n} topics.")
    connect = Connect(connect_url=config.connect_url)
    if topics:
        influx_config.update_topics(topics, timestamp)
        # --validate option
        if validate:
            click.echo(
                connect.validate(
                    name=influx_config.connector_class,
                    connect_config=influx_config.asjson(),
                )
            )
            return 0
        # --dry-run option returns the connector configuration
        if dry_run:
            click.echo(influx_config.asjson())
            return 0
        # Validate configuration before creating the connector
        validation = connect.validate(
            name=influx_config.connector_class,
            connect_config=influx_config.asjson(),
        )
        try:
            error_count = json.loads(validation)["error_count"]
            click.echo(f"Validation returned {error_count} error(s).")
            if error_count > 0:
                click.echo(
                    "Use the ``--validate`` option to return the validation "
                    "results."
                )
                return 1
        except Exception:
            click.echo(validation)
            return 1
        click.echo(f"Uploading {name} connector configuration...")
        connect.create_or_update(
            name=name, connect_config=influx_config.asjson()
        )
    if auto_update:
        while True:
            time.sleep(int(check_interval) / 1000)
            try:
                # Current list of topics from Kafka
                current_topics = Topic(
                    config.broker_url, topic_regex, excluded_topic_regex
                ).names
                new_topics = list(set(current_topics) - set(topics))
                if new_topics:
                    click.echo("Found new topics, updating the connector...")
                    influx_config.update_topics(current_topics, timestamp)
                    connect.create_or_update(
                        name=name, connect_config=influx_config.asjson()
                    )
                    topics = current_topics
            except KeyboardInterrupt:
                raise click.ClickException("Interruped.")
    return 0
