##########################################################################################
# julian/datetime_pyparser.py
##########################################################################################
"""
=============================
Date-Time pyparsing  Grammars
=============================
"""

from julian.mjd_pyparser  import mjd_pyparser
from julian.date_pyparser import date_pyparser
from julian.time_pyparser import time_pyparser, opt_timesys

from pyparsing import (
    FollowedBy,
    Literal,
    OneOrMore,
    ParserElement,
    StringEnd,
    Suppress,
    White,
    ZeroOrMore,
    alphanums,
    one_of,
)

# All whitespace is handled explicitly
ParserElement.set_default_whitespace_chars('')

# Useful definitions...
white     = Suppress(OneOrMore(White()))
opt_white = Suppress(ZeroOrMore(White()))

seps = ['-', ',', '//', '/', ':']
NORMAL_SEPS  = Suppress(opt_white + one_of(seps) + opt_white) | white
ISOLIKE_SEPS = Suppress(opt_white + one_of(seps + ['T']) + opt_white) | white
T = Suppress(Literal('T'))


def datetime_pyparser(order='YMD', *, treq=False, strict=False, doy=False, mjd=False,
                      weekdays=False, extended=False, leapsecs=False, ampm=False,
                      timezones=False, timesys=False, floating=False, iso_only=False,
                      padding=True, embedded=False):
    """A date-time pyparser.

    Parameters:
        order (str):
            One of "YMD", "MDY", or "DMY", defining the default order for day month, and
            year in situations where it might be ambiguous.
        treq (bool, optional):
            True if a time field is required; False to recognize date strings that do not
            include a time.
        strict (bool, optional):
            True for a stricter parser, which is less likely to match strings that might
            not actually represent dates.
        doy (bool, optional):
            True to recognize dates specified as year and day-of-year.
        mjd (bool, optional):
            True to recognize Modified Julian Dates.
        weekdays (bool, optional):
            True to allow dates including weekdays.
        extended (bool, optional):
            True to support extended year values: signed (with at least four digits) and
            those involving "CE", "BCE", "AD", "BC".
        leapsecs (bool, optional):
            True to recognize leap seconds.
        ampm (bool, optional):
            True to recognize "am" and "pm" suffixes.
        timezones (bool, optional):
            True to recognize and interpret time zones. If True, returned values are
            adjusted to UTC.
        timesys (bool, optional):
            True to recognize an embedded time system such as "UTC", "TAI", etc.
        floating (bool, optional):
            True to allow date-times specified using floating-point days, hours, or
            minutes.
        iso_only (bool, optional):
            Require an ISO 8601:1988-compatible date string; ignore `order`, `strict`,
            `mjd, `ampm`, and `timesys` options.
        padding (bool, optional):
            True to ignore leading or trailing white space.
        embedded (bool, optional):
            True to allow the time to be followed by additional text.

    Returns:
        pyparsing.ParserElement: A parser for the selected syntax. Calling the `as_list()`
        method on the returned ParseResult object returns a list containing some but not
        all of these tuples, depending on what appears in the parsed string:

        * ("YEAR", year): Year if specified; two-digit years are converted to 1970-2069.
          Alternatively, "MJD" or "JD" if the day number is to be interpreted as a Julian
          or Modified Julian date.
        * ("MONTH", month): Month if specified, 1-12.
        * ("DAY", day); Day number: 1-31 if a month was specified; 1-366 if a day of year
          was specified; otherwise, the MJD or JD day value.
        * ("WEEKDAY", abbrev): Day of the week if provided, as an abbreviated uppercase
          name: "MON", "TUE", etc.
        * ("HOUR", hour): Hour if specified, 0-23, an int or possibly a float. Hours am/pm
          are converted to the range 0-23 automatically.
        * ("MINUTE", minute): Minute if specified, integer or float.
        * ("SECOND", second): Second if specified, integer or float.
        * ("TZ", tz_name): Name of the time zone if specified.
        * ("TZMIN", tzmin): Ooffset of the time zone in minutes.
        * ("TIMESYS", name): "UTC" for an MJD or JD date; "TDB" for an MJED or JED date;
          "TT" for an MJTD or JTD date.
        * ("~", number): The last occurrence of this tuple in the list contains the number
          of characters matched.
    """

    # Always include the full ISO 8601:1988 format, including the "T" separator.
    # This is the only allowed use of "T" as a separator.
    iso_idate = date_pyparser(iso_only=True, doy=doy, extended=extended, floating=False,
                              padding=False, embedded=True)
    iso_time = time_pyparser(iso_only=True, leapsecs=leapsecs, timezones=timezones,
                             floating=floating, padding=False, embedded=True)

    if iso_only:
        pyparser = iso_idate + T + iso_time
        if floating:
            iso_fdate = date_pyparser(iso_only=True, doy=doy, extended=extended,
                                      floating=True, floating_only=treq,
                                      padding=False, embedded=True)
            pyparser |= iso_fdate

        elif not treq:
            pyparser |= iso_idate

    # Augment the parser for non-ISO date-times
    else:

        # Define the general parser for date + time or time + date
        # Note that MJD and floating-point dates cannot be combined with a time
        idate = date_pyparser(order=order, strict=strict, doy=doy, mjd=False,
                              weekdays=weekdays, extended=extended, floating=False,
                              padding=False, embedded=True)
        time = time_pyparser(leapsecs=leapsecs, ampm=ampm, timezones=timezones,
                             timesys=timesys, floating=floating,
                             padding=False, embedded=True)

        # Define the parser with or without a time requirement
        pyparser = idate + NORMAL_SEPS + time | time + NORMAL_SEPS + idate

        # Allow for a floating-point date and/or a time system without a date
        if floating:
            fdate = date_pyparser(order=order, strict=strict, doy=doy, mjd=False,
                                  weekdays=weekdays, extended=extended,
                                  floating=True, floating_only=treq,
                                  padding=False, embedded=True)
            if timesys:
                pyparser |= fdate + opt_timesys
            else:
                pyparser |= fdate

        elif not treq:
            if timesys:
                pyparser |= idate + opt_timesys
            else:
                pyparser |= idate

        # Allow for the MJD options
        if mjd:
            mjd_parser = mjd_pyparser(floating=True, timesys=timesys,
                                      padding=False, embedded=True)
            if timesys:
                wo_timesys = mjd_pyparser(floating=True, timesys=False,
                                          padding=False, embedded=True)
                pyparser |= mjd_parser | wo_timesys + opt_timesys
            else:
                pyparser |= mjd_parser

        # Place the standard ISO parser in front
        pyparser = iso_idate + T + iso_time | pyparser

    # Finalize and return
    pyparser = pyparser + ~FollowedBy(alphanums + '.+-')

    if padding:
        pyparser = opt_white + pyparser + opt_white

    if not embedded:
        pyparser = pyparser + StringEnd()

    return pyparser

##########################################################################################
