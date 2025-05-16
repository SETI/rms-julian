##########################################################################################
# julian/time_of_day.py
##########################################################################################
"""
=====================
Time of Day Functions
=====================
"""

import numbers
import numpy as np
from julian._exceptions import JulianValidateFailure
from julian._utils      import _float, _int, _is_float, _is_int, _number


def hms_from_sec(sec, *, validate=False, leapsecs=True):
    """Hour, minute and second from seconds into day.

    Parameters:
        sec (int, float, or array-like): Elapsed seconds into a day. Values must be
            between 0 and 86410, where numbers above 86400 are treated as leap seconds.
        validate (bool, optional):
            True to check that the input values all fall within their valid range.
        leapsecs (bool, optional):
            True to tolerate leap second values during validation.

    Returns:
        tuple (h, m, s):

        - **h** (*int or array*): Hours (0-23).
        - **m** (*int or array*): Minutes (0-59).
        - **s** (*int, float, or array*): Seconds. Values are integral if `sec` is
          integral.

    Raises:
        JulianValidateFailure:
            If `validate` is True and any value of `sec` is outside the valid range.
    """

    sec = _number(sec)

    # Test for valid range
    if validate:
        if np.any(sec < 0.):
            raise JulianValidateFailure('seconds < 0')
        if leapsecs:
            if np.any(sec >= 86410.):
                raise JulianValidateFailure('seconds >= 86410')
        else:
            if np.any(sec >= 86400.):
                raise JulianValidateFailure('seconds >= 86400')

    h = _int(np.minimum(_int(sec//3600), 23))
    t = sec - 3600 * h

    m = _int(np.minimum(_int(t//60), 59))
    t -= 60 * m

    return (h, m, t)


def hms_microsec_from_sec(sec, *, validate=False, leapsecs=True):
    """Hour, minute, second, and microsecond from seconds into day.

    This function is provided to simplify conversions to `datetime` objects, where
    fractional seconds are defined by an integer value of microseconds. All returned
    values are integral, with the number of microseconds rounded if necessary.

    Parameters:
        sec (int, float, or array-like): Elapsed seconds into a day. Values must be
            between 0 and 86410, where numbers above 86400 are treated as leap seconds.
        validate (bool, optional):
            True to check that the input values all fall within their valid range.
        leapsecs (bool, optional):
            True to tolerate leap second values during validation.

    Returns:
        tuple (h, m, s, microsec):

        - **h** (*int or array*): Hours (0-23).
        - **m** (*int or array*): Minutes (0-59).
        - **s** (*int or array*): Seconds (0-69).
        - **microsec** (*int or array*): Microseconds (0-999999).

    Raises:
        JulianValidateFailure:
            If `validate` is True and any value of `sec` is outside the valid range.

    Notes:
        To construct a `datetime.time`, use::

            datetime.time(*hms_microsec_from_sec(sec))

        To construct a `datetime.datetime` from a day number and seconds value, use::

            datetime.datetime(*ymd_from_day(day), *hms_microsec_from_sec(sec))
    """

    if isinstance(sec, numbers.Integral):
        return hms_from_sec(sec, validate=validate, leapsecs=leapsecs) + (0,)

    if _is_int(sec):
        microsec = np.zeros(sec.shape, dtype=np.int64)
        return hms_from_sec(sec, validate=validate, leapsecs=leapsecs) + (microsec,)

    # Shift upward by just under 0.5 so floor() rounds to nearest
    # This ensures that microsec <= 999999
    h, m, s = hms_from_sec(sec + 0.49999e-6, validate=validate, leapsecs=leapsecs)
    isec = _int(s)
    microsec = _int(1.e6 * (s - isec))
    return (h, m, isec, microsec)


def sec_from_hms(h, m, s, microsec=0, *, validate=False, leapsecs=True):
    """Seconds into day from hour, minute and second.

    Parameters:
        h (int, float, or array-like):
            Hour (0-23).
        m (int, float, or array-like):
            Minute (0-59).
        s (int, float, or array-like):
            Second (0-69), with values > 59 implying leap seconds (if `leapsecs` is True).
        microsec (int, float, or array-like, optional):
            Microseconds (0-999999), provided as an alternative to specifying fractional
            seconds and to simplify conversions from `datetime` objects.
        validate (bool, optional):
            True to check that the input values all fall within their valid range.
        leapsecs (bool, optional):
            True to tolerate leap second values during validation.

    Returns:
        int, float, or array:
            Elapsed seconds. Values are integral if `h`, `m`, and `s` are all integral.

    Raises:
        JulianValidateFailure:
            If `validate` is True and any input values are out of range.

    NotesL
    """

    h = _number(h)
    m = _number(m)
    s = _number(s)
    microsec = _number(microsec)

    if validate:
        if np.any(h >= 24):
            raise JulianValidateFailure('hour >= 24')
        if np.any(h < 0):
            raise JulianValidateFailure('hour < 0')
        if np.any(m >= 60):
            raise JulianValidateFailure('minute >= 60')
        if np.any(m < 0):
            raise JulianValidateFailure('minute < 0')
        if np.any(s < 0):
            raise JulianValidateFailure('seconds < 0')
        if np.any(microsec < 0):
            raise JulianValidateFailure('microseconds < 0')
        if np.any(microsec >= 1000000):
            raise JulianValidateFailure('microseconds >= 1000000')
        if leapsecs:
            if np.any((s >= 60) & (h != 23) & (m != 59)):
                raise JulianValidateFailure('seconds >= 60')
            if np.any(s >= 70):
                raise JulianValidateFailure('seconds >= 70')
        else:
            if np.any(s >= 60):
                raise JulianValidateFailure('seconds >= 60')

    if np.any(microsec):    # don't convert to float unless necessary
        return 3600 * h + 60 * m + s + microsec/1.e6

    if _is_float(microsec):
        return _float(3600 * h + 60 * m + s)

    return 3600 * h + 60 * m + s

##########################################################################################
