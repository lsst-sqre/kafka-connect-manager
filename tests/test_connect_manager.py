#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cp-kafka-connect-manager` package."""

import pytest

from click.testing import CliRunner
from connect_manager import main


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.main)
    assert result.exit_code == 0
    assert '' in result.output
    help_result = runner.invoke(main.main, ['--help'])
    assert help_result.exit_code == 0
    help_result = runner.invoke(main.main, ['-h'])
    assert help_result.exit_code == 0
    version_result = runner.invoke(main.main, ['--version'])
    assert version_result.exit_code == 0
