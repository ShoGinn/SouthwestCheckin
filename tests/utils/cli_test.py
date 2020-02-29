"""Pytest for the cli."""
from click.testing import CliRunner, Result
from swcheckin.cli.__main__ import main as command_line
from swcheckin.config import config

from ..my_vcr_test import custom_vcr

MY_VCR = custom_vcr()


def verify_invoke_from_clirunner(result: Result, expected_output: str) -> None:
    """Verify the Invoke from CliRunner."""
    assert result.exit_code == 0
    assert result.output == expected_output


@MY_VCR.use_cassette()
def test_cli() -> None:
    """Test the cli with default options."""
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'XXXXXX', '-f', 'John', '-l', 'Smith', '-v'],
    )
    assert result.exit_code == 0


def test_cli_no_args() -> None:
    """Test the cli with no arguments."""
    result: Result = CliRunner().invoke(
        command_line, [],
    )
    assert result.exit_code == 2


@MY_VCR.use_cassette()
def test_api_key_fail() -> None:
    """Test a failed api key."""
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'XXXXXX', '-f', 'John', '-l', 'Smith'],
    )
    assert result.exit_code == 1


@MY_VCR.use_cassette()
def test_bad_request() -> None:
    """Test a bad request."""
    config.max_attempts = 1
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'xxx', '-f', 'blah', '-l', 'blah'],
    )
    assert result.exit_code == 1


@MY_VCR.use_cassette('test_bad_request.yml')
def test_bad_request_verbose() -> None:
    """Test a bad request verbose."""
    config.max_attempts = 1
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'xxx', '-f', 'blah', '-l', 'blah', '-v'],
    )
    assert result.exit_code == 1
