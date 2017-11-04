import calendar
import sys
import time
from builtins import str
from datetime import datetime, timedelta

import locale
import re

# Required 3rd party libraries
from parsedatetime import parsedatetime

try:
    import attr
    from dateutil.tz import tzlocal
    from dateutil.parser import parse
except ImportError as e:
    print("ERROR: Missing module - %s" % e.args[0])
    sys.exit(1)

from . import colors


def string_to_unicode(string):
    return str(string)


def string_from_unicode(string):
    return string.encode(locale.getlocale()[1] or
                         locale.getpreferredencoding(False) or
                         "UTF-8", "replace")


def usage(expanded=False):
    sys.stdout.write(__doc__ % sys.argv[0])
    sys.exit(1)


def print_err_msg(msg):
    print_msg(colors.ClrBrred(), msg)


def print_msg(color, msg):
    if colors.CLR.use_color:
        sys.stdout.write(str(color))
        sys.stdout.write(str(msg))
        sys.stdout.write(str(colors.ClrNrm()))
    else:
        sys.stdout.write(msg)


def debug_print(msg):
    return
    print_msg(colors.ClrYlw(), msg)


def dprint(obj):
    try:
        from pprint import pprint
        pprint(obj)
    except ImportError:
        print(obj)


class DateTimeParser:
    def __init__(self):
        self.pdt_calendar = parsedatetime.Calendar()

    def from_string(self, e_when):
        default_date_time = datetime.now(tzlocal()).replace(hour=0,
                                                          minute=0,
                                                          second=0,
                                                          microsecond=0)

        try:
            e_time_start = parse(e_when, default=default_date_time)
        except BaseException:
            struct, result = self.pdt_calendar.parse(e_when)
            if not result:
                raise ValueError("Date and time is invalid")
            e_time_start = datetime.fromtimestamp(time.mktime(struct), tzlocal())

        return e_time_start


def days_since_epoch(dt):
    # Because I hate magic numbers
    __DAYS_IN_SECONDS__ = 24 * 60 * 60
    return calendar.timegm(dt.timetuple()) / __DAYS_IN_SECONDS__


def get_time_from_str(e_when, e_duration=0, allday=False):
    dtp = DateTimeParser()

    try:
        e_time_start = dtp.from_string(e_when)
    except BaseException:
        print_err_msg('Date and time is invalid!\n')
        sys.exit(1)

    if allday:
        try:
            e_time_stop = e_time_start + timedelta(days=float(e_duration))
        except BaseException:
            print_err_msg('Duration time (days) is invalid\n')
            sys.exit(1)

        s_time_start = e_time_start.date().isoformat()
        s_time_stop = e_time_stop.date().isoformat()

    else:
        try:
            e_time_stop = e_time_start + timedelta(minutes=float(e_duration))
        except BaseException:
            print_err_msg('Duration time (minutes) is invalid\n')
            sys.exit(1)

        s_time_start = e_time_start.isoformat()
        s_time_stop = e_time_stop.isoformat()

    return s_time_start, s_time_stop


def parse_reminder(rem):
    match_obj = re.match(r'^(\d+)([wdhm]?)(?:\s+(popup|email|sms))?$', rem)
    if not match_obj:
        print_err_msg('Invalid reminder: ' + rem + '\n')
        sys.exit(1)
    n = int(match_obj.group(1))
    t = match_obj.group(2)
    m = match_obj.group(3)
    if t == 'w':
        n = n * 7 * 24 * 60
    elif t == 'd':
        n = n * 24 * 60
    elif t == 'h':
        n = n * 60

    if not m:
        m = 'popup'

    return n, m


def sigint_handler(signum, frame):
    print_err_msg('Signal caught, bye!\n')
    sys.exit(1)