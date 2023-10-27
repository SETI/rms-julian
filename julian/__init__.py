##########################################################################################
# julian/__init__.py
##########################################################################################
"""PDS Ring-Moon Systems Node, SETI Institute
Julian Library, version 2.0

This is a large set of routines for handing date and time conversions. Compared to other
date/time libraries in Python, including CSPYCE, it has these features.

- It handles the time systems Coordinated Universal Time (UTC), International Atomic Time
  (TAI), Barycentric Dynamical Time (TDB), and Terrestrial Time (TT, previously called
  Terrestrial Dynamical Time or TDT), properly accounting for leap seconds.

- Any time can be expressed as a running count of elapsed seconds from a defined epoch, as
  a calendar date, using Julian Date (JD), or using Modified Julian Date (MJD).

- Nearly all functions can process arrays of dates and times all at once, not just as
  individual values. This can provide a substantial performance boost compared to using
  iteration, especially when parsing or formatting columns of dates for a table file.

- It provides options for how to interpret times before 1972, when the current version of
  the UTC time system was first implemented. Since 1972, leap seconds have been used to
  keep TAI in sync with UTC, ensuring that the UTC time never differs from UT1, the time
  system defined by the Earth's rotation, by more than ~ 1 second. Between 1958 and 1972,
  the UTC second was redefined as a "rubber second", which would stretch or shrink as
  necessary to ensure that every mean solar day contained exactly 86,400 UT seconds; see
        https://hpiers.obspm.fr/eop-pc/index.php?index=TAI-UTC_tab
  Before 1958, we use UT1 in place of UTC, employing a model for the long-term variations
  in Earth's rotation as documented for the "Five Millennium Canon of Solar Eclipses:
  -1999 to +3000; see
        https://eclipse.gsfc.nasa.gov/SEpubs/5MCSE.html
  The numerical details are here:
        https://eclipse.gsfc.nasa.gov/SEcat5/deltatpoly.html
  This model can also be applied to future dates.

- It supports both the modern (Gregorian) calendar and the older Julian calendar. The
  transition date can be defined by the user, or else the Julian calendar can be
  suppressed entirely.

- A general parser is able to interpret almost arbitrary date-time strings correctly. This
  parser can also be used to "scrape" occurrences of dates and times from arbitrary text.


CALENDAR OPERATIONS

Every date is represented by an integer "day" value, where day = 0 on January 1, 2000.
Various functions are provided to convert between day values and year, month, day, or day
of year:
    day_from_ymd(), day_from_yd(), ymd_from_day(), yd_from_day().

Years prior to 1 CE are specified using the "astronomical year", which includes a year
zero. As a result, 1 BCE is specified as year 0, 2 BCE as year -1, 4713 BCE as year -4712,
etc. Note that there is some historical uncertainty about which years were recognized as
leap years in Rome between the adoption of the Julian calendar in 46 BCE and about 8 CE.
For simplicity, we follow the convention that the Julian calendar extended backward
indefinitely, so all all years divisible by four, including 4 CE, 0 (1 BCE), -4 (5 BCE),
-8 (9 BCE), etc., were leap years.

Months are referred to by integers 1-12, 1 for January and 12 for December.

Day numbers within months are 1-31; day numbers within years are 1-366.

Functions are provided to determine the number of days in a specified month or year:
    days_in_month(), days_in_year(), days_in_ym().

Use the function set_gregorian_start() to specify the (Gregorian) year, month, and day for
the transition from the earlier Julian calendar to the modern Gregorian calendar. The
default start date of the Gregorian calendar is October 15, 1582, when this calendar was
first adopted in much of Europe. However, the user is free to modify this date; for
example, Britain adopted the Gregorian calendar on September 14, 1752.

Note that most calendar functions support an input parameter "proleptic", taking a value
of True or False. If True, all calendar dates are proleptic (extrapolated backward
assuming the modern calendar), regardless of which calendar was in effect at the time.


TIME SYSTEMS

All times are represented by numbers representing seconds past a specified epoch on
January 1, 2000. Internally, TAI times serve as the intermediary between the different
time systems (TAI, UTC, TDB, and TT). Conversions are straightforward, using:
    tai_from_utc(), utc_from_tai(), tai_from_tdb(), tdb_from_tai(), tai_from_tt(),
    tt_from_tai().
Alternatively, the more general function time_from_time() lets you specify the initial and
final time systems of the conversion.

You can also specify a time using an integer day plus the number of elapsed seconds on
that day, and then convert between these values and any time system:
    day_sec_from_utc(), day_sec_from_tai(), tai_from_day(), tai_from_day_sec(),
    utc_from_day(), utc_from_day_sec().
Alternatively, the more general functions day_sec_from_time() and time_from_day_sec()
let you specify the initial and final time systems.


JULIAN DATES

Similarly, Julian dates and Modified Julian Dates can be converted to times using any time
system:
    jd_from_time(), time_from_jd(), mjd_from_time(), time_from_mjd(),
    jd_from_day_sec(), day_sec_from_jd(), mjd_from_day_sec(), day_sec_from_mjd().

You can also convert directly between integer MJD and integer day numbers using:
    mjd_from_day(), day_from_mjd().


LEAP SECOND HANDLING

In 1972, the UTC time system began using leap seconds to keep TAI times in sync with mean
solar time to a precision of ~ 1 second. We provide several methods to allow the user to
keep the leap second list up to date.

If the environment variable SPICE_LSK_FILEPATH is defined, then this SPICE leapseconds
kernel is read at startup. Otherwise, leap seconds through 2020 are always included, as
defined in SPICE kernel file naif00012.tls. You can also call the function load_lsk()
directly.

Alternatively, use insert_leap_second() to augment the list with additional leap seconds
(positive or negative).

Use seconds_on_day() to determine the length in seconds of a given day; use
leapsecs_on_day() or leapsecs_from_ymd() to determine the cumulative number of leap
seconds on a given date.

Use set_ut_model() to define how to handle times before 1972 and into the future, outside
the duration of the current UTC leap second system.


FORMATTING

Several functions are provided to express dates or times as formatted character strings:
    format_day(), format_day_sec(), format_sec(), format_tai(), iso_from_tai().
Most variations of the ISO 8601:1988 format are supported.

Note that these functions can produce strings, bytestrings, or arbitrary arrays thereof.
The functions operate on the entire array all at once, and can therefore be much faster
than making individual calls over and over. For example, note that one could provide a
NumPy memmap as input to these functions and it would write content directly into a large
ASCII table, avoiding any conversion to/from Unicode.


PARSING

We provide functions for the very fast parsing of identically-formatted strings or
bytestrings that represent dates, times or both:
    day_from_iso(), day_sec_from_iso(), sec_from_iso(), tai_from_iso(), tdb_from_iso(),
    time_from_iso().
These functions recognize most variations of the ISO 8601:1988 format, and are ideal for
interpreting date and time columns from large ASCII tables.

More general parsers are provided for interpreting individual dates and times in almost
arbitrary formats:
    day_from_string(), day_sec_from_string(), sec_from_string()
These same parsers can also be invoked to "scrape" dates and times from almost arbitrary
text:
    day_in_string(), days_in_string(), time_in_string(), times_in_string(),
    dates_in_string().
Time zones are recognized, including most standard abbreviations.

For users familiar with the pyparsing module, we provide functions that generate parsers
for a wide variety of special requirements. See:
    date_pyparser(), datetime_pyparser(), time_pyparser().
"""

from julian.calendar import (
    day_from_yd,
    day_from_ymd,
    days_in_month,
    days_in_year,
    days_in_ym,
    month_from_ym,
    set_gregorian_start,
    yd_from_day,
    ym_from_month,
    ymd_from_day,
)

from julian.formatter import (
    format_day_sec,
    format_day,
    format_sec,
    format_tai,
    hms_format_from_sec,            # deprecated; use format_sec()
    iso_from_tai,
    yd_format_from_day,             # deprecated; use format_day()
    ydhms_format_from_day_sec,      # deprecated; use format_day_sec()
    ydhms_format_from_tai,          # deprecated; use format_tai()
    ymd_format_from_day,            # deprecated; use format_day()
    ymdhms_format_from_day_sec,     # deprecated; use format_day_sec()
    ymdhms_format_from_tai,         # deprecated; use format_tai()
)

from julian.iso_parser import (
    day_from_iso,
    day_sec_from_iso,
    sec_from_iso,
    tai_from_iso,
    tdb_from_iso,
    time_from_iso,
)

from julian.leap_seconds import (
    delta_t_from_day,
    delta_t_from_ymd,
    insert_leap_second,
    leapsecs_from_day,
    leapsecs_from_ym,
    leapsecs_from_ymd,
    leapsecs_on_day,
    load_lsk,
    seconds_on_day,
    set_ut_model,
)

from julian.mjd_jd import (
    day_from_mjd,
    day_sec_from_jd,
    day_sec_from_mjd,
    jd_from_day_sec,
    jd_from_tai,                    # deprecated; use jd_from_time()
    jd_from_time,
    jed_from_tai,                   # deprecated; use jd_from_time()
    jed_from_tdb,                   # deprecated; use jd_from_time()
    mjd_from_day,
    mjd_from_day_sec,
    mjd_from_tai,                   # deprecated; use mjd_from_time()
    mjd_from_time,
    mjed_from_tai,                  # deprecated; use mjd_from_time()
    mjed_from_tdb,                  # deprecated; use mjd_from_time()
    tai_from_jd,                    # deprecated; use time_from_jd()
    tai_from_jed,                   # deprecated; use time_from_jd()
    tai_from_mjd,                   # deprecated; use time_from_mjd()
    tai_from_mjed,                  # deprecated; use time_from_mjd()
    tdb_from_jed,                   # deprecated; use time_from_jd()
    tdb_from_mjed,                  # deprecated; use time_from_mjd()
    time_from_jd,
    time_from_mjd,
)

from julian.time_of_day import (
    hms_from_sec,
    sec_from_hms,
)

from julian.utc_tai_tdb import (
    day_sec_as_type_from_utc,       # deprecated; use day_sec_from_time()
    day_sec_from_tai,
    day_sec_from_time,
    day_sec_from_utc,
    set_tai_origin,
    tai_from_day_sec,
    tai_from_day,
    tai_from_tdb,
    tai_from_tdt,                   # deprecated; use tai_from_tt()
    tai_from_tt,
    tai_from_utc,
    tdb_from_tai,
    tdt_from_tai,                   # deprecated; use tt_from_tai()
    time_from_day_sec,
    time_from_time,
    tt_from_tai,
    utc_from_day_sec_as_type,       # deprecated; use day_sec_from_time()
    utc_from_day_sec,
    utc_from_day,
    utc_from_tai,
)

from julian.date_parser import (
    day_from_string,
    day_in_string,                  # deprecated; use days_in_strings()
    days_in_string,                 # deprecated; use days_in_strings()
    days_in_strings,
)

from julian.datetime_parser import (
    dates_in_string,                # deprecated; use day_sec_in_strings()
    day_sec_from_string,
    day_sec_in_strings,
    day_sec_type_from_string,       # deprecated; use day_sec_from_string()
    day_sec_type_in_string,         # deprecated; use day_sec_in_strings()
)

from julian.time_parser import (
    sec_from_string,
    sec_in_strings,
    time_in_string,                 # deprecated; use sec_in_strings()
    times_in_string,                # deprecated; use sec_in_strings()
)

from julian.warning import JulianDeprecationWarning

from julian.date_pyparser     import date_pyparser
from julian.datetime_pyparser import datetime_pyparser
from julian.time_pyparser     import time_pyparser

##########################################################################################
