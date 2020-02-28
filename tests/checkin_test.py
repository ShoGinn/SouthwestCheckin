"""pytest script."""

import pytest
from click.testing import CliRunner, Result
from swcheckin.__main__ import main as command_line
from swcheckin.config import config
from swcheckin.openflights import timezone_for_airport
from swcheckin.southwest import Reservation

from .my_vcr_test import custom_vcr

MY_VCR = custom_vcr()
RESERVATION = Reservation('XXXXXX', 'John', 'Smith')


@MY_VCR.use_cassette()
def test_generate_headers():
    """Test generating headers."""
    headers = Reservation.generate_headers()
    assert headers['Content-Type'] == 'application/json'
    assert headers['X-API-Key'] == 'l7xx0a43088fe6254712b10787646d1b298e'

# pylint: disable=broad-except
@MY_VCR.use_cassette()
def test_reservation_lookup():
    """Test reservation lookup."""
    try:
        RESERVATION.lookup_existing_reservation()
    except Exception:
        pytest.fail('Error looking up reservation')


@MY_VCR.use_cassette()
def test_checkin():
    """Test checking in."""
    try:
        RESERVATION.checkin()
    except Exception:
        pytest.fail('Error checking in')


@MY_VCR.use_cassette()
def test_checkin_without_passes():
    """Test checking in without passes."""
    try:
        RESERVATION.checkin()
    except Exception:
        pytest.fail('Error checking in')


@MY_VCR.use_cassette()
def test_openflights_api():
    """Test the openflights api."""
    assert timezone_for_airport('LAX').zone == 'America/Los_Angeles'


def verify_invoke_from_clirunner(result: Result, expected_output: str) -> None:
    """Verify the Invoke from CliRunner."""
    assert result.exit_code == 0
    assert result.output == expected_output


@MY_VCR.use_cassette()
def test_cli():
    """Test the cli with default options."""
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'XXXXXX', '-f', 'John', '-l', 'Smith', '-v'],
    )
    assert result.exit_code == 0


def test_cli_no_args():
    """Test the cli with no arguments."""
    result: Result = CliRunner().invoke(
        command_line, [],
    )
    assert result.exit_code == 2


@MY_VCR.use_cassette()
def test_api_key_fail():
    """Test a failed api key."""
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'XXXXXX', '-f', 'John', '-l', 'Smith'],
    )
    assert result.exit_code == 1


@MY_VCR.use_cassette()
def test_bad_request():
    """Test a bad request."""
    config.max_attempts = 1
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'xxx', '-f', 'blah', '-l', 'blah'],
    )
    assert result.exit_code == 1


@MY_VCR.use_cassette('test_bad_request.yml')
def test_bad_request_verbose():
    """Test a bad request verbose."""
    config.max_attempts = 1
    result: Result = CliRunner().invoke(
        command_line, ['-c', 'xxx', '-f', 'blah', '-l', 'blah', '-v'],
    )
    assert result.exit_code == 1
