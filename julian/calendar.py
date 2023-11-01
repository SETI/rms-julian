##########################################################################################
# julian/calendar.py
##########################################################################################
# Calendar conversions
#   Algorithms from http://alcor.concordia.ca/~gpkatch/gdate-algorithm.html
#
# day     = number of days elapsed since January 1, 2000
# month   = number of months elapsed since January 2000
# (y,m,d) = year, month (1-12), day (1-31)
# (y,d)   = year and day-of-year (1-366)
# (y,m)   = year and month number (1-12)
#
# All function operate on either scalars or arrays. If given scalars, they return scalars;
# if given anything array-like, they return arrays.
##########################################################################################

import numbers

import numpy as np
from julian.utils   import _int, _int64, _is_float, _number
from julian.warning import _warn


def day_from_ymd(y, m, d, *, validate=False, proleptic=False, use_julian=None):
    """Number of elapsed days after January 1, 2000, given a year, month, and day.

    Inputs:
        y           year as a scalar, array, or array-like. Values are truncated to
                    integers if necessary. Note that 1 BCE corresponds to year 0, 2 BCE to
                    -1, etc.
        m           month number, 1-12, as a scalar, array, or array-like. Values are
                    truncated to integers if necessary.
        d           day number, 1-31, as a scalar, array, or array-like. Values can be
                    integers or floats; if the latter, floating-point values are returned.
        validate    True to raise ValueError for year, month, and day numbers out of
                    range; default is False.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    global FEB29_1BCE_GREGORIAN, FEB29_1BCE_JULIAN, GREGORIAN_DAY1

    if use_julian is not None:
        _warn('use_julian is deprecated; use "proleptic=not use_julian"')
        proleptic = not use_julian

    (y, m, d) = np.broadcast_arrays(y, m, d)
    if y.shape:
        y = _int(y)
        m = _int(m)
    else:
        y = int(y[()])
        m = int(m[()])
        d = d[()]

    is_float = _is_float(d)
    if is_float:
        frac = d % 1
        d = _int(d)
    else:
        frac = 0

    if validate:
        if np.any(d < 1):
            raise ValueError('days must be between 1 and 31')

        month = month_from_ym(y, m, validate=True)
        if np.any(d > days_in_month(month, proleptic=proleptic)):
            raise ValueError('day number cannot exceed days in month')

    mm = (m + 9) % 12   # This makes March the first month and February the last
    yy = y - mm//10     # This subtracts one from the year if the month is January or
                        # February.

    # Random notes:
    #
    # 306 is the number of days in March-December
    #
    # The formula (mm*306 + 5)//10 yields the number of days from the end of February to
    # the end of the given the month, using mm==1 for March, 2 for April, ... 10 for
    # December, 11 for January.
    #
    # The formula 365*yy + yy//4 - yy//100 + yy//400 is the number of elapsed days from
    # the end of February in 1 BCE to the end of February in year yy. (Note that 1 BCE is
    # yy==0.)

    day = ((365*yy + yy//4 - yy//100 + yy//400) + (mm * 306 + 5) // 10 + d
           + FEB29_1BCE_GREGORIAN)

    if proleptic:
        return day + frac

    # Handle the Julian-Gregorian calendar transition if necessary
    if np.isscalar(day):
        if day >= GREGORIAN_DAY1:
            return day + frac
        else:
            alt_day = ((365 * yy + yy//4) + (mm * 306 + 5) // 10 + d
                       + FEB29_1BCE_JULIAN)
            if validate:
                alt_ymd = ymd_from_day(alt_day, proleptic=False)
                if alt_ymd != (y,m,d):
                    isodate = '%04d-%02d-%02d' % (y, m, d)
                    raise ValueError(isodate + ' falls between the Julian and Gregorian '
                                               'calendars')
            return alt_day + frac

    mask = (day < GREGORIAN_DAY1)
    if np.any(mask):
        alt_day = ((365 * yy + yy//4) + (mm * 306 + 5) // 10 + d
                   + FEB29_1BCE_JULIAN)
        day[mask] = alt_day[mask]

        if validate:
            alt_d = ymd_from_day(alt_day[mask], proleptic=False)[2]
            dd = np.broadcast_to(d, day.shape)
            if np.any(alt_d != dd[mask]):
                raise ValueError('one or more dates fall between the Julian and '
                                 'Gregorian calendars')

    if is_float:
        return day + frac

    return day

########################################

def ymd_from_day(day, *, proleptic=False, use_julian=None):
    """Year, month and day from day number.

    Inputs:
        day         number of elapsed days after January 1, 2000 as a scalar, array, or
                    or array-like. Values can be integers or floats; if the latter,
                    returned day values are also floats.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    day = _number(day)
    is_float = _is_float(day)
    if is_float:
        frac = day % 1
    else:
        frac = 0
    day = _int64(day)

    # Execute the magic algorithm for the proleptic Gregorian calendar
    g = day + 730425                    # Elapsed days after March 1, 1 BCE, Gregorian
    y = (10000*g + 14780)//3652425      # Year, assumed starting on March 1
    doy = g - (365*y + y//4 - y//100 + y//400)
                                        # Day number since March 1 of given year

    # Correct the year if date is March 1 of
    if np.any(doy < 0):
        if np.shape(day):
            y[doy < 0] -= 1
        elif doy < 0:
            y -= 1
        doy = g - (365*y + y//4 - y//100 + y//400)

    if not proleptic:
        # https://www.quora.com/What-were-the-leap-years-from-45-BC-to-0-BC
        # https://scienceworld.wolfram.com/astronomy/LeapYear.html
        # https://www.wwu.edu/astro101/a101_leapyear.shtml

        # Prior to year 1, we extrapolate the Julian calendar backward. In reality, there
        # were no leap days prior to 46 BCE, and there is no clear consensus on which
        # years were leap years in Rome prior to 8 CE.

        mask = (day < GREGORIAN_DAY1)
        if np.any(mask):
            alt_g = day + 730427
            alt_y = (100 * alt_g + 75) // 36525
            alt_doy = alt_g - (365 * alt_y + alt_y//4)

            if np.isscalar(day):
                y = alt_y
                doy = alt_doy
            else:
                y[mask] = alt_y[mask]
                doy[mask] = alt_doy[mask]

    m0 = (100 * doy + 52)//3060         # mm = month, with m0==0 for March
    m = (m0 + 2) % 12 + 1
    y += (m0 + 2) // 12
    d = doy - (m0 * 306 + 5)//10 + 1

    if is_float:
        return (y, m, d + frac)
    return (y, m, d)

########################################

def yd_from_day(day, *, proleptic=False, use_julian=None):
    """Year and day-of-year from day number.

    Inputs:
        day         number of elapsed days after January 1, 2000 as a scalar, array, or
                    array-like. Values can be integers or floats; if the latter, returned
                    day values are also floats.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    (y,m,d) = ymd_from_day(day, proleptic=proleptic)
    return (y, _number(day) - day_from_ymd(y, 1, 1, proleptic=proleptic) + 1)

########################################

def day_from_yd(y, d, *, validate=False, proleptic=False, use_julian=None):
    """Day number from year and day-of-year.

    Inputs:
        y           year as a scalar, array, or array-like. Values are truncated to
                    integers if necessary. Note that 1 BCE corresponds to year 0, 2 BCE to
                    -1, etc.
        d           day of year, 1-366, as a scalar, array, or array-like. Values can be
                    integers or floats; if the latter, floating-point values are returned.
        validate    True to raise ValueError for year, month, and day numbers out of
                    range; default is False.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    if validate:
        if np.any(_int(d) < 1) or np.any(_int(d) > days_in_year(y, proleptic=proleptic)):
            raise ValueError('day number cannot exceed the number of days in the year')

    return day_from_ymd(y, 1, 1, proleptic=proleptic) + _number(d) - 1

########################################

def month_from_ym(y, m, *, validate=False):
    """Number of elapsed months since January 2000.

    Inputs:
        y           year as a scalar, array, or array-like. Values are truncated to
                    integers if necessary. Note that 1 BCE corresponds to year 0, 2 BCE to
                    -1, etc.
        m           month number, 1-12, as a scalar, array, or array-like. Values are
                    truncated to integers if necessary.
        validate    True to raise ValueError for year, month, and day numbers out of
                    range; default is False.
    """

    if validate:
        if np.any(_int(m) < 1) or np.any(_int(m) > 12):
            raise ValueError('month number must be between 1 and 12')

    return 12*(y - 2000) + (_int(m) - 1)

########################################

def ym_from_month(month):
    """Year and month from the number of elapsed months since January 2000.

    Inputs:
        month       month number, as the number of elapsed months since the beginning of
                    January 2000. Can be a scalar, array, or array-like. Values are
                    truncated to integers if necessary.
    """

    month = _int(month)

    y = _int(month // 12)
    m = month - 12 * y
    y += 2000
    m += 1

    return (y, m)

########################################

def days_in_month(month, *, proleptic=False, use_julian=None):
    """Number of days in month, given the number of elapsed months since January 2000.

    Inputs:
        month       month number, as the number of elapsed months since the beginning of
                    January 2000. Can be a scalar, array, or array-like. Values are
                    truncated to integers if necessary.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    month = _int(month)

    (y, m) = ym_from_month(month)
    day0 = day_from_ymd(y, m, 1, proleptic=proleptic)

    (y, m) = ym_from_month(month + 1)
    day1 = day_from_ymd(y, m, 1, proleptic=proleptic)

    return day1 - day0

########################################

def days_in_ym(y, m, *, validate=False, proleptic=False, use_julian=None):
    """Number of days in month.

    Inputs:
        y           year as a scalar, array, or array-like. Values are truncated to
                    integers if necessary. Note that 1 BCE corresponds to year 0, 2 BCE to
                    -1, etc.
        m           month number, 1-12, as a scalar, array, or array-like. Values are
                    truncated to integers if necessary.
        validate    True to raise ValueError for year and month numbers out of range;
                    default is False.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    month = month_from_ym(y, m, validate=validate)
    return days_in_month(month, proleptic=proleptic)

########################################

def days_in_year(year, *, proleptic=False, use_julian=None):
    """Number of days in year.

    Inputs:
        y           year as a scalar, array, or array-like. Values are truncated to
                    integers if necessary. Note that 1 BCE corresponds to year 0, 2 BCE to
                    -1, etc.
        proleptic   True to interpret all dates according to the modern Gregorian
                    calendar, even those that occurred prior to the transition from the
                    Julian calendar. False to use the Julian calendar for earlier dates.
                    Regardless of the calendar, all dates BCE are proleptic.
        use_julian  DEPRECATED input option equivalent to (not proleptic).
    """

    if use_julian is not None:
        _warn('use_julian option is deprecated; use proleptic=(negated value)')
        proleptic = not use_julian

    return (day_from_ymd(year+1, 1, 1, proleptic=proleptic) -
            day_from_ymd(year,   1, 1, proleptic=proleptic))

########################################

def set_gregorian_start(y=1582, m=10, d=15):
    """Set the first day of the Gregorian calendar as a year, month, and day.

    Note that is a global setting for the entire Julian library.

    Use set_gregorian_start(None) to ignore the Julian calendar, using the modern
    Gregorian calendar exclusively, even where proleptic=False.
    """

    global GREGORIAN_DAY1, GREGORIAN_DAY1_YMD, GREGORIAN_DAY0_YMD

    if y is None:       # prevents any Julian calendar date from being used
        GREGORIAN_DAY1 = -1.e30
        return

    GREGORIAN_DAY1 = day_from_ymd(y, m, d, proleptic=True)
    GREGORIAN_DAY1_YMD = (y, m, d)
    GREGORIAN_DAY0_YMD = ymd_from_day(GREGORIAN_DAY1-1, proleptic=False)

# Fill in some constants used by day_from_ymd

# Day number of February 29 1 BCE (year 0) in the Gregorian and Julian
# calendars, relative to January 1, 2000 in the Gregorian calendar.
# Should be...
# FEB29_1BCE_GREGORIAN = -730426
# FEB29_1BCE_JULIAN    = -730428

# Day number of the first day of the Gregorian calendar, October 15, 1582.
# Should be...
# GREGORIAN_DAY1 = -152384
# GREGORIAN_DAY1_YMD = (1582, 10, 15)
# GREGORIAN_DAY0_YMD = (1582, 10,  4)

# Deriving from first principles...
FEB29_1BCE_GREGORIAN = 0
FEB29_1BCE_GREGORIAN = (day_from_ymd(0, 2, 29, proleptic=True) -
                        day_from_ymd(2000, 1, 1, proleptic=True))

GREGORIAN_DAY1_YMD = (1582, 10, 15)
GREGORIAN_DAY1 = day_from_ymd(*GREGORIAN_DAY1_YMD, proleptic=True)

FEB29_1BCE_JULIAN = 0
FEB29_1BCE_JULIAN = (day_from_ymd(0, 2, 29, proleptic=False)
                     - day_from_ymd(1582, 10, 5, proleptic=False)
                     + GREGORIAN_DAY1)

GREGORIAN_DAY0_YMD = ymd_from_day(GREGORIAN_DAY1-1, proleptic=False)

##########################################################################################
