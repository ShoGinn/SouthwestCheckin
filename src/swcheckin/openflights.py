"""OpenFlights API."""
import json

import pytz
import requests


def timezone_for_airport(airport_code: str):
    """Get the Timezone for the airport.

    Arguments:
        airport_code {str} -- the IATA airport code

    Returns:
        [str] -- timezone id (ex. US/Eastern)
    """
    tzrequest = {
        'iata': airport_code,
        'country': 'ALL',
        'db': 'airports',
        'iatafilter': 'true',
        'action': 'SEARCH',
        'offset': '0',
    }
    tzresult = requests.post(
        'https://openflights.org/php/apsearch.php',
        tzrequest,
    )
    airport_tz = pytz.timezone(
        json.loads(tzresult.text)['airports'][0]['tz_id'], )
    return airport_tz
