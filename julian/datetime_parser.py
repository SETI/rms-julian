##########################################################################################
# julian/datetime_parser.py
##########################################################################################

import numbers
import pyparsing

from julian.date_parser  import _date_pattern_filter, _day_from_dict, _search_in_string
from julian.leap_seconds import seconds_on_day
from julian.mjd_jd       import day_from_mjd, JD_MINUS_MJD
from julian.time_parser  import _sec_from_dict, _time_pattern_filter
from julian.warning      import _warn

from julian.datetime_pyparser import datetime_pyparser

##########################################################################################
# General date/time parser
##########################################################################################

def day_sec_from_string(string, order='YMD', *, doy=True, mjd=False, proleptic=False,
                        treq=False, leapsecs=True, ampm=True, timezones=False,
                        timesys=False, floating=False):
    """Day and second values based on the parsing of a free-form string.

    Input:
        string      string to interpret.
        order       one of "YMD", "MDY", or "DMY"; this defines the default order for
                    date, month, and year in situations where it might be ambiguous.
        doy         True to recognize dates specified as year and day-of-year.
        mjd         True to recognize dates expressed as MJD, JD, MJED, JED, etc.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
        treq        True if a time field is required; False to recognize date strings that
                    do not include a time.
        leapsecs    True to recognize leap seconds.
        ampm        True to recognize "am" and "pm" suffixes.
        timezones   True to recognize and interpret time zones. If True, returned values
                    are adjusted to UTC.
        timesys     True to recognize an embedded time system such as "UTC", "TAI", etc.
        floating    True to recognize time specified using floating-point hours or
                    minutes.

    Return:         (day, sec) or (day, sec, tsys)
        day         integer day number, converted to UTC if a time zone was identified.
        sec         seconds into day, converted to UTC if a time zone was identified.
        tsys        name of the time system, included if the input value of timesys is
                    True.
    """

    parser = datetime_pyparser(order=order, treq=treq, strict=False, doy=doy, mjd=mjd,
                      weekdays=True, leapsecs=leapsecs, ampm=ampm, timezones=timezones,
                      floating=floating, timesys=timesys, iso_only=False, padding=True,
                      embedded=False)
    try:
        parse_list = parser.parse_string(string).as_list()
    except pyparsing.ParseException:
        raise ValueError(f'unrecognized date/time format: "{string}"')

    parse_dict = {key:value for key, value in parse_list}
    (day, sec, tsys) = _day_sec_timesys_from_dict(parse_dict, proleptic=proleptic,
                                                  leapsecs=leapsecs, validate=True)

    if timesys:
        return (day, sec, tsys)

    return (day, sec)

##########################################################################################
# Date/time scrapers
##########################################################################################

def day_sec_in_strings(strings, order='YMD', *, doy=False, mjd=False, proleptic=False,
                       treq=False, leapsecs=True, ampm=False, timezones=False,
                       timesys=False, floating=False, validate=True, substrings=False,
                       first=False):
    """List of day and second values representing date/time strings found by searching one
    or more strings for patterns that look like formatted dates and times.

    Input:
        strings     list/array/tuple of strings to interpret.
        order       one of "YMD", "MDY", or "DMY"; this defines the default order for
                    date, month, and year in situations where it might be ambiguous.
        doy         True to allow dates specified as year and day-of-year.
        mjd         True to allow dates expressed as MJD, JD, MJED, JED, etc.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
        treq        True if a time field is required; False to recognize date strings that
                    do not include a time.
        leapsecs    True to recognize leap seconds.
        ampm        True to recognize "am" and "pm" suffixes.
        timezones   True to recognize and interpret time zones. If True, returned values
                    are adjusted to UTC.
        timesys     True to allow a time system, e.g., "UTC", "TAI", "TDB", or "TT".
        floating    True to recognize time specified using floating-point hours or
                    minutes.
        validate    if True, patterns that resembled date/time strings but are not valid
                    for other reasons are ignored.
        substrings  True to also return the substring containing each identified date and
                    time.
        first       True to return when the first date and time is found, with None on
                    failure; False to return the full, ordered list of dates and times.

    Return:         a list of tuples (day, sec, optional tsys, optional substring).
        day         integer day number, onverted to UTC if a time zone was identified.
        sec         seconds into day, onverted to UTC if a time zone was identified.
        tsys        name of each associated time system, with "UTC" the default; included
                    if the input value of timesys is True.
        substring   the substring containing the text that was interpreted to represent
                    this date and time; included if the input value of substrings is True.

        Note: If the input value of first is True, then a single tuple is returned
        rather than a list of tuples. If no date was identified, None is returned.
    """

    if isinstance(strings, str):
        strings = [strings]

    parser = datetime_pyparser(order=order, treq=treq, strict=True, doy=doy, mjd=mjd,
                               weekdays=True, leapsecs=leapsecs, ampm=ampm,
                               timezones=timezones, timesys=timesys, floating=floating,
                               iso_only=False, padding=True, embedded=True)

    day_sec_list = []
    for string in strings:

        # Use fast check to skip over strings that are clearly time-less
        if not _date_pattern_filter(string, doy=doy, mjd=mjd):
            continue
        if treq and not mjd and not _time_pattern_filter(string):
            continue

        while True:
            parse_dict, substring, string = _search_in_string(string, parser)
            if not parse_dict:
                break

            try:
                (day, sec, tsys) = _day_sec_timesys_from_dict(parse_dict,
                                                              leapsecs=leapsecs,
                                                              proleptic=proleptic,
                                                              validate=validate)
            except ValueError:  # pragma: no cover
                continue

            result = [day, sec]
            if timesys:
                result.append(tsys)
            if substrings:
                result.append(substring)

            day_sec_list.append(tuple(result))

            if first:
                return day_sec_list[0]

    if first:
        return None

    return day_sec_list

##########################################################################################
# Utilities
##########################################################################################

def _day_sec_timesys_from_dict(parse_dict, leapsecs=True, proleptic=False, validate=True):
    """Day, second, and time system values based on the contents of a dictionary."""

    year = parse_dict['YEAR']
    day = parse_dict['DAY']
    timesys = parse_dict.get('TIMESYS', '')
    timesys_or_utc = timesys or 'UTC'

    if isinstance(year, numbers.Integral) and isinstance(day, numbers.Integral):
        day = _day_from_dict(parse_dict, proleptic=proleptic, validate=validate)
        sec, dday, tsys = _sec_from_dict(parse_dict, day, leapsecs=leapsecs,
                                         validate=validate)
        return (day + dday, sec, timesys_or_utc)

    if year == 'MJD' and isinstance(day, numbers.Integral):
        return (day_from_mjd(day), 0, timesys_or_utc)

    # The remaining cases all involve a conversion from fractional day to seconds.
    # The year could be a numeric year, "JD", or "MJD".

    # Convert to day number and fraction
    if year == 'JD':
        day = day - JD_MINUS_MJD
        year = 'MJD'

    frac = day % 1
    day = int(day)

    if year == 'MJD':
        day = day_from_mjd(day)
    else:
        day = _day_from_dict(parse_dict, proleptic=proleptic, validate=validate)

    # If a time system is specified, it overrides the leapsecs setting
    if timesys:
        leapsecs = (timesys == 'UTC')

    # Convert fraction of day to seconds
    sec = frac * seconds_on_day(day, leapsecs=leapsecs)

    return (day, sec, timesys_or_utc)

##########################################################################################
# DEPRECATED
##########################################################################################

def day_sec_type_from_string(string, order="YMD", validate=True, use_julian=True):
    """Day, second, and time system based on the parsing of the string.

    DEPRECATED. Use day_sec_from_string() with timesys=True.

    Input:
        string          String to interpret.
        order           One of 'YMD', 'MDY', or 'DMY'; this defines the default
                        order for date, month, and year in situations where it
                        might be ambiguous.
        validate        True to check the syntax and values more carefully. *IGNORED*
        use_julian      True to interpret dates prior to the adoption of the
                        Gregorian calendar as dates in the Julian calendar.
    """

    _warn('day_sec_type_from_string() is deprecated; '
          'use day_sec_from_string() with timesys=True')

    return day_sec_from_string(string, order=order, timesys=True, timezones=False,
                               mjd=True, floating=True, proleptic=(not use_julian))


def day_sec_type_in_string(string, order='YMD', *, remainder=False, use_julian=True):
    """Day, second, and time system based on the first occurrence of a date within a
    string.

    None if no date was found.

    DEPRECATED. Use day_sec_in_strings() with timesys=True.

    Input:
        string      string to interpret.
        order       One of "YMD", "MDY", or "DMY"; this defines the default order for
                    date, month, and year in situations where it might be ambiguous.
        remainder   If True and a date was found, return a 4-element tuple:
                        (day, sec, time system, remainder of string).
                    Otherwise, just return the 3-element tuple:
                        (day, sec, time system).
        use_julian  True to interpret dates prior to the adoption of the Gregorian
                    calendar as dates in the Julian calendar.
    """

    _warn('day_sec_type_in_string() is deprecated; '
          'use day_sec_in_strings() with timesys=True')

    result = day_sec_in_strings([string], order=order, doy=True, mjd=False,
                                proleptic=(not use_julian), treq=False, leapsecs=True,
                                ampm=True, timezones=False, timesys=True, floating=False,
                                validate=True, substrings=True, first=True)
    if result is None:
        return None

    day, sec, tsys, substring = result
    if remainder:
        return (day, sec, tsys, string.partition(substring)[2])
    else:
        return (day, sec, tsys)


def dates_in_string(string, order='YMD', *, use_julian=True):
    """List of the dates found in this string, represented by tuples (day, sec, time
    system).

    DEPRECATED. Use day_sec_in_strings().

    Input:
        string      string to interpret.
        order       One of "YMD", "MDY", or "DMY"; this defines the default order for
                    date, month, and year in situations where it might be ambiguous.
        use_julian  True to interpret dates prior to the adoption of the Gregorian
                    calendar as dates in the Julian calendar.
    """

    return day_sec_in_strings([string], order=order, doy=True, mjd=True,
                              proleptic=(not use_julian), treq=False, leapsecs=True,
                              ampm=True, timezones=False, floating=True, timesys=True,
                              validate=True, substrings=False, first=False)

##########################################################################################
