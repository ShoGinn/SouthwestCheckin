"""SouthwestCheckin openflights util API test."""

from swcheckin.utils.openflights import timezone_for_airport

from ..my_vcr_test import custom_vcr

MY_VCR = custom_vcr()


@MY_VCR.use_cassette()
def test_openflights_api() -> None:
    """Test the openflights api."""
    assert timezone_for_airport('LAX').zone == 'America/Los_Angeles'
