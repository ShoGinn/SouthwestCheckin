"""Southwest Checkin."""
import json
import sys
import uuid

from time import sleep
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests

from .config import config


class Reservation():
    """The Reservation Class."""

    def __init__(self, number: str, first: str, last: str, verbose: bool = False):
        """Require confirmation number, first and last name."""
        self.number = number
        self.first = first
        self.last = last
        self.verbose = verbose

    @staticmethod
    def generate_headers():
        """Generate the headers necessary for request.

        Returns:
            dict -- The header
        """
        config_js = requests.get('https://mobile.southwest.com/js/config.js')
        if config_js.status_code == requests.codes.ok:  # pylint: disable=no-member
            modded = config_js.text[config_js.text.index('API_KEY'):]
            api_key = modded[
                modded.index(':') +
                1:modded.index(',')
            ].strip('"')
        else:
            print("Couldn't get API_KEY")
            sys.exit(1)

        user_experience_key = str(uuid.uuid1()).upper()
        # Pulled from proxying the Southwest iOS App
        return {
            'Host': 'mobile.southwest.com',
            'Content-Type': 'application/json',
            'X-API-Key': api_key,
            'X-User-Experience-Id': user_experience_key,
            'Accept': '*/*',
            'X-Channel-ID': 'MWEB',
        }

    # You might ask yourself, "Why the hell does this exist?"
    # Basically, there sometimes appears a "hiccup" in Southwest where things
    # aren't exactly available 24-hours before, so we try a few times
    def safe_request(self, url: str, body: Optional[str] = None):
        """Loops the request a set number of times [Default: 40].

        Arguments:
            url {str} -- southwests url for mobile

        Keyword Arguments:
            body {Optional[str]} -- extra info (default: {None})

        Returns:
            {dict} -- The json from southwest
        """
        try:
            headers = Reservation.generate_headers()
            for _ in range(0, config.max_attempts):
                if body is not None:
                    response = requests.post(url, headers=headers, json=body)
                else:
                    response = requests.get(url, headers=headers)
                data = response.json()
                if 'httpStatusCode' in data and data['httpStatusCode'] in [
                        'NOT_FOUND',
                        'BAD_REQUEST',
                        'FORBIDDEN',
                ]:
                    if not self.verbose:
                        print(data['message'])
                    else:
                        print(response.headers)
                        print(json.dumps(data, indent=2))
                    sleep(config.checkin_interval_seconds)
                    continue
                if self.verbose:
                    print(response.headers)
                    print(json.dumps(data, indent=2))
                return data
            sys.exit('Unable to get data, killing self')
        except ValueError:  # pragma: no cover
            # Ignore responses with no json data in body
            pass

    def load_json_page(self, url: str, body: Optional[str] = None):
        """Load the page with the info we need.

        Arguments:
            url {str} -- southwests url for mobile

        Keyword Arguments:
            body {Optional[str]} -- extra info (default: {None})

        Returns:
            [type] -- [description]
        """
        # pylint: disable=invalid-name
        data = self.safe_request(url, body)
        for k, v in list(data.items()):
            if k.endswith('Page'):
                return v
        return None  # pragma: no cover

    def with_suffix(self, uri):
        """Add the sw suffix to the url.

        Arguments:
            uri {str} -- The URL

        Returns:
            str -- The Url with the suffix added.
        """
        combined_url = urljoin(config.base_url, uri) + self.number + '?'
        suffix_dict = {'first-name': self.first, 'last-name': self.last}
        return combined_url + urlencode(suffix_dict)

    def lookup_existing_reservation(self):
        """Find our existing record."""
        return self.load_json_page(
            self.with_suffix(
                'mobile-air-booking/v1/mobile-air-booking/page/view-reservation/',
            ), )

    def get_checkin_data(self):
        """Get the Checkin Data."""
        return self.load_json_page(
            self.with_suffix(
                'mobile-air-operations/v1/mobile-air-operations/page/check-in/',
            ), )

    def checkin(self):
        """Check in function.

        Returns:
            [str] -- returns the confirmation
        """
        data = self.get_checkin_data()
        info_needed = data['_links']['checkIn']
        base_url = urljoin(config.base_url, 'mobile-air-operations')
        url = base_url + info_needed['href']
        print('Attempting check-in...')
        confirmation = self.load_json_page(url, info_needed['body'])
        return confirmation
