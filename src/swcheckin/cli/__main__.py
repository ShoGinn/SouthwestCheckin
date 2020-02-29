"""Main."""
import errno
import sys

import click

from swcheckin.checkin import auto_checkin


# Click decorators
@click.command(
    context_settings=dict(
        help_option_names=['-h', '--help', '--halp'],
        ignore_unknown_options=True,
    ),
)
@click.version_option(prog_name='Southwest Checkin')
@click.option(
    '--conf-num',
    '-c',
    required=True,
    help='Your SouthWest Confirmation Number',
)
@click.option(
    '-f',
    '--first',
    '--first-name',
    'firstname',
    required=True,
    help='The First name of the traveller',
)
@click.option(
    '-l',
    '--last',
    '--last-name',
    'lastname',
    required=True,
    help='The Last name of the traveller',
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    default=False,
    help='Shows debugging information',
)
def main(
        conf_num: str = 'REDACTED',
        firstname: str = 'REDACTED',
        lastname: str = 'REDACTED',
        verbose: bool = False,
) -> None:
    """Python SouthWest Airlines Automation.

    Checks your flight reservation with Southwest
    and then checks you in at exactly 24 hours
    before your flight. Queue up the script
    and it will sleep until the earliest possible check-in time.
    """
    try:
        auto_checkin(conf_num, firstname, lastname, verbose)
    except KeyboardInterrupt:  # pragma: no cover
        print('Ctrl+C detected, canceling checkin')
        sys.exit()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except IOError as exc:
        if exc.errno != errno.EPIPE:
            raise
    except RuntimeError as the_error:
        raise SystemExit(str(the_error))
