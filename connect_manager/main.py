# -*- coding: utf-8 -*-

"""Console script for cp-kafka-connect-manager."""

__all__ = ('main',)

import click


# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(message='%(version)s')
def main(args=None):
    """Console script for cp-kafka-connect-manager."""
    click.echo('main')
    return 0
