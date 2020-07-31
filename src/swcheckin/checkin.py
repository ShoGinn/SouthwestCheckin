"""This is the command line script."""
import sys
import time
from datetime import datetime, timedelta
from threading import Thread

from humanfriendly import format_timespan
from pytz import utc
from swcheckin.southwest import Reservation
from swcheckin.utils.openflights import timezone_for_airport

CHECKIN_EARLY_SECONDS = 5


def schedule_checkin(flight_time, reservation) -> None:
    """Schedules the checkin.

    Arguments:
        flight_time {object} -- [description]
        reservation {object} -- [description]
    """
    checkin_time = flight_time - timedelta(days=1)
    current_time = datetime.utcnow().replace(tzinfo=utc)
    # check to see if we need to sleep until 24 hours before flight
    if checkin_time > current_time:
        # calculate duration to sleep
        delta = (
            checkin_time -
            current_time
        ).total_seconds() - CHECKIN_EARLY_SECONDS
        # pretty print our wait time
        print(f'Too early to check in.  Waiting {format_timespan(delta)}.')
        try:
            time.sleep(delta)
        except OverflowError:
            print(
                'System unable to sleep for that long, '
                'try checking in closer to your departure date', )
            sys.exit(1)
    data = reservation.checkin()
    for flight in data['flights']:
        for doc in flight['passengers']:
            print(
                f"{doc['name']} got {doc['boardingGroup']}{doc['boardingPosition']}!",
            )


def auto_checkin(
        reservation_number: str,
        first_name: str,
        last_name: str,
        verbose: bool = False,
) -> None:
    """Start the Auto Checkin Process.

    Arguments:
        reservation_number {[str]} -- Usually 6 characters
        first_name {[str]} -- First Name of Traveller
        last_name {[str]} -- Last name of Traveller

    Keyword Arguments:
        verbose {bool} -- Provides responses from SW (default: {False})
    """
    reservation = Reservation(
        reservation_number,
        first_name,
        last_name,
        verbose,
    )
    body = reservation.lookup_existing_reservation()

    # Get our utc time
    now = datetime.utcnow().replace(tzinfo=utc)

    threads = []

    # find all eligible legs for checkin
    for leg in body['bounds']:
        # calculate departure for this leg
        airport = '{}, {}'.format(
            leg['departureAirport']['name'],
            leg['departureAirport']['state'],
        )
        takeoff = '{} {}'.format(leg['departureDate'], leg['departureTime'])
        airport_tz = timezone_for_airport(leg['departureAirport']['code'])
        takeoff_date = airport_tz.localize(
            datetime.strptime(takeoff, '%Y-%m-%d %H:%M'), )
        if takeoff_date > now:
            # found a flight for checkin!
            print(
                f'Flight information found, departing {airport}'
                f" at {takeoff_date.strftime('%b %d %I:%M%p')}", )
            # Checkin with a thread
            checkin_thread = Thread(
                target=schedule_checkin,
                args=(takeoff_date, reservation),
            )
            checkin_thread.daemon = True
            checkin_thread.start()
            threads.append(checkin_thread)

    # cleanup threads while handling Ctrl+C
    while True:
        if len(threads) == 0:
            break
        for checkin_thread in threads:
            checkin_thread.join(5)
            if not checkin_thread.is_alive():
                threads.remove(checkin_thread)
                break
