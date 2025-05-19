##########################################################################################
# julian/datetime_parsers.py
##########################################################################################
"""
=================
Date-Time Parsers
=================
"""

import numbers
import pyparsing

from julian.date_parsers import _date_pattern_filter, _day_from_dict, _search_in_string
from julian.leap_seconds import seconds_on_day
from julian.mjd_jd       import day_from_mjd, _JD_MINUS_MJD
from julian.time_parsers import _sec_from_dict, _time_pattern_filter
from julian._exceptions  import JulianParseException

from julian.datetime_pyparser import datetime_pyparser

##########################################################################################
# General date/time parser
##########################################################################################

def day_sec_from_string(string, order='YMD', *, doy=True, mjd=True, weekdays=False,
                        extended=False, proleptic=False, treq=False, leapsecs=True,
                        ampm=True, timezones=False, timesys=False, floating=False):
    """Day and second values based on the parsing of a free-form string.

    Parameters:
        string (str):
            String to interpret.
        order (str):
            One of "YMD", "MDY", or "DMY", defining the default order for day month, and
            year in situations where it might be ambiguous.
        doy (bool, optional):
            True to recognize dates specified as year and day-of-year.
        mjd (bool, optional):
            True to recognize Modified Julian Dates.
        weekdays (bool, optional):
            True to allow dates including weekdays.
        extended (bool, optional):
            True to support extended year values: signed (with at least four digits) and
            those involving "CE", "BCE", "AD", "BC".
        proleptic (bool, optional):
            True to interpret all dates according to the modern Gregorian calendar, even
            those that occurred prior to the transition from the Julian calendar. False to
            use the Julian calendar for earlier dates.
        treq (bool, optional):
            True if a time field is required; False to recognize date strings that do not
            include a time.
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
            True to recognize time specified using floating-point hours or minutes.

    Returns:
        tuple (day, sec[, tsys]):

        - **day** (*int*): Integer day number, converted to UTC if a time zone was
          identified.
        - **sec** (*int or float*): Seconds into day, converted to UTC if a time zone was
          identified.
        - **tsys** (*str*): Name of the time system, included if `timesys` is True.

    Raises:
        JulianParseException:
            If `string` was not recognized as a valid date-time expression.
        JulianValidateFailure:
            If the date-time string contains invalid or contradictory information.
    """

    parser = datetime_pyparser(order=order, treq=treq, strict=False, doy=doy, mjd=mjd,
                               weekdays=weekdays, extended=extended, leapsecs=leapsecs,
                               ampm=ampm, timezones=timezones, floating=floating,
                               timesys=timesys, iso_only=False, padding=True,
                               embedded=False)
    try:
        parse_list = parser.parse_string(string).as_list()
    except pyparsing.ParseException:
        raise JulianParseException(f'unrecognized date/time format: "{string}"')

    parse_dict = {key:value for key, value in parse_list}
    (day, sec, tsys) = _day_sec_timesys_from_dict(parse_dict, proleptic=proleptic,
                                                  leapsecs=leapsecs, validate=True)

    if timesys:
        return (day, sec, tsys)

    return (day, sec)

##########################################################################################
# Date/time scrapers
##########################################################################################

def day_sec_in_strings(strings, order='YMD', *, doy=False, mjd=False, weekdays=False,
                       extended=False, proleptic=False, treq=False, leapsecs=True,
                       ampm=False, timezones=False, timesys=False, floating=False,
                       substrings=False, first=False):
    """List of day and second values representing date/time strings found by searching one
    or more strings for patterns that look like formatted dates and times.

    Parameters:
        strings (list, tuple, or array):
            Strings to interpret.
        order (str):
            One of "YMD", "MDY", or "DMY", defining the default order for day month, and
            year in situations where it might be ambiguous.
        doy (bool, optional):
            True to recognize dates specified as year and day-of-year.
        mjd (bool, optional):
            True to recognize Modified Julian Dates.
        weekdays (bool, optional):
            True to allow dates including weekdays.
        extended (bool, optional):
            True to support extended year values: signed (with at least four digits) and
            those involving "CE", "BCE", "AD", "BC".
        proleptic (bool, optional):
            True to interpret all dates according to the modern Gregorian calendar, even
            those that occurred prior to the transition from the Julian calendar. False to
            use the Julian calendar for earlier dates.
        treq (bool, optional):
            True if a time field is required; False to recognize date strings that do not
            include a time.
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
            True to recognize time specified using floating-point hours or minutes.
        substrings (bool, optional):
            True to also return the substring containing each identified date-time value.
        first (bool, optional):
            True to return the first date-time value found rather than a list of values.
            In this case, None is returned if no date-time is found rather than an empty
            list.

    Returns:
        tuple (day, sec[, tsys][, substring]), list[tuple], or None: If `first` is False,
        a list of tuples containing information about each date-time is returned;
        otherwise, a single tuple is returned or None if no date-time value was found.
        Within this tuple:

        - **day** (*int*): Day number, converted to UTC if a time zone was identified.
        - **sec** (*int or float*): Seconds into day, converted to UTC if a time zone was
          identified.
        - **tsys** (*str*): The name of each associated time system, with "UTC" the
          default; included if `timesys` is True.
        - **substring** (*str*): The substring containing the text that was interpreted to
          represent this date and time; included if `substrings` is True.

    Raises:
        JulianValidateFailure:
            If a matched date-time string contains invalid or contradictory information.
    """

    if isinstance(strings, str):
        strings = [strings]

    parser = datetime_pyparser(order=order, treq=treq, strict=True, doy=doy, mjd=mjd,
                               weekdays=weekdays, extended=extended, leapsecs=leapsecs,
                               ampm=ampm, timezones=timezones, timesys=timesys,
                               floating=floating, iso_only=False, padding=True,
                               embedded=True)

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

            (day, sec, tsys) = _day_sec_timesys_from_dict(parse_dict, leapsecs=leapsecs,
                                                          proleptic=proleptic,
                                                          validate=True)
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
        day = day - _JD_MINUS_MJD
        year = 'MJD'

    frac = day % 1
    day = int(day // 1.)

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
