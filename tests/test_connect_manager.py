# This file is part of kafka-connect-manager.
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


"""Tests for `kafka-connect-manager` package.
"""

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
    create_result = runner.invoke(main.main, ['create'])
    assert create_result.exit_code == 0
    create_influxdb_sink_result = runner.invoke(main.main,
                                                ['create influxdb-sink'])
    assert create_influxdb_sink_result.exit_code == 2
    delete_result = runner.invoke(main.main, ['delete'])
    assert delete_result.exit_code == 2
    help_result = runner.invoke(main.main, ['help'])
    assert help_result.exit_code == 0
    info_result = runner.invoke(main.main, ['info'])
    assert info_result.exit_code == 2
    list_result = runner.invoke(main.main, ['list'])
    assert list_result.exit_code == 1
    pause_result = runner.invoke(main.main, ['pause'])
    assert pause_result.exit_code == 2
    restart_result = runner.invoke(main.main, ['restart'])
    assert restart_result.exit_code == 2
    resume_result = runner.invoke(main.main, ['resume'])
    assert resume_result.exit_code == 2
    status_result = runner.invoke(main.main, ['status'])
    assert status_result.exit_code == 2
