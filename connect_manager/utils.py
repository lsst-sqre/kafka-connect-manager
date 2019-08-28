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
