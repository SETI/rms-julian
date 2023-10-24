| PyPI Release | Test Status | Code Coverage |
| ------------ | ----------- | ------------- |
| [![PyPI version](https://badge.fury.io/py/julian.svg)](https://badge.fury.io/py/julian) | [![Build status](https://img.shields.io/github/actions/workflow/status/SETI/rms-julian/run-tests.yml?branch=master)](https://github.com/SETI/rms-julian/actions) | [![Code coverage](https://img.shields.io/codecov/c/github/SETI/rms-julian/main?logo=codecov)](https://codecov.io/gh/SETI/rms-julian) |

# rms-julian

PDS Ring-Moon Systems Node, SETI Institute

Supported versions: Python >= 3.7

This is a set of routines for handing date and time conversions. It handles
these time systems:

- UTC = Universal Coordinates Time, similar to Grenwich Mean Time, expressed
        by integer days since January 1, 2000 plus floating-point seconds
        since beginning of day. UTC can also be represented in various
        standard formats for a calendar date plus an optional time.
- TAI = International Atomic Time, which is number of actual elapsed seconds
        since December 31, 1999 at 23:59:28. This running tally accounts for
        all leap seconds.
- TDB = Terrestrial Barycentric Time, which is the number of elapsed seconds
        since noon (not midnight!) on January 1, 2000, and adjusted for
        relativistic effects that cause a clock on the Earth to vary in speed
        relative to one at the solar system barycenter. This quantity is
        equivalent to "ephemeris time" in the SPICE time system, although
        differences at the level of milliseconds can occur.
- TDT = Terrestrial Dynamical Time, which is the preferred time system for
        Earth-centered orbits. This is also defined in a manner consistent
        with that in the SPICE toolkit.
- JD  = Julian Date as a number of elapsed days since noon (not midnight!) on
        Monday, January 1, 4713 BCE. Each period from one noon to the next
        counts as one day, regardless of whether that day contains leap
        seconds. As a result, some days are longer than others. (Note that
        leap seconds always occur at midnight, and therefore at the middle of
        a Julian day.)
- MJD = Modified Julian Date, defined to be JD minus 2400000.5.
- JED = Julian Ephmeris Date, defined to be TDB/86400 + 2451545. It is
        compatible with SPICE ephemeris time but in units of days rather than
        seconds.
- MJED = Modified Julian Ephmeris Date, defined as JED minus 2400000.5.

Throughout the library, TAI is the intermediary time relative to which all
others are defined. Note: The term "TAI" is also used infrequently in the
SPICE Toolkit, but the SPICE value is smaller by exactly 43200 seconds. All
other terms used here are essentially identical in meaning to their SPICE
Toolkit equivalents.

If the environment variable SPICE_LSK_FILEPATH is defined, then this SPICE
leapseconds kernel is read at startup. Otherwise, leap seconds through 2020
are always included, as defined in NAIF00012.TLS.

The library also handles calendar conversions and both parses and formats
strings that express time in UTC.

This library duplicates much of the functionality of Python's built-in
datetime library, but is separate from them because the datetime library
cannot handle leap seconds.

This library duplicates some of the SPICE toolkit, but has the advantage of
supporting array-based time operations, which can be much faster when
processing large amounts of data. It is also pure Python, and so does not
need to be linked with C or FORTRAN libraries.

Aside from the I/O routines, every argument to every function can be either
a scalar or something array-like, i.e, a NumPy array, a tuple or a list.
Arguments other than scalars are converted to NumPy arrays, the arrays are
broadcasted to the same shape if necessary, and the complete array(s) of
results are returned.
