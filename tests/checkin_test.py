"""pytest script."""

import pytest
from swcheckin.southwest import Reservation

from .my_vcr_test import custom_vcr

MY_VCR = custom_vcr()
RESERVATION = Reservation('XXXXXX', 'John', 'Smith')


@MY_VCR.use_cassette()
def test_generate_headers() -> None:
    """Test generating headers."""
    headers = Reservation.generate_headers()
    assert headers['Content-Type'] == 'application/json'
    assert headers['X-API-Key'] == 'l7xx0a43088fe6254712b10787646d1b298e'

# pylint: disable=broad-except
@MY_VCR.use_cassette()
def test_reservation_lookup() -> None:
    """Test reservation lookup."""
    try:
        RESERVATION.lookup_existing_reservation()
    except Exception:
        pytest.fail('Error looking up reservation')


@MY_VCR.use_cassette()
def test_checkin() -> None:
    """Test checking in."""
    try:
        RESERVATION.checkin()
    except Exception:
        pytest.fail('Error checking in')


@MY_VCR.use_cassette()
def test_checkin_without_passes() -> None:
    """Test checking in without passes."""
    try:
        RESERVATION.checkin()
    except Exception:
        pytest.fail('Error checking in')
