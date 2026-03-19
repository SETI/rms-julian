##########################################################################################
# julian/test_time_parsers.py
##########################################################################################

import pytest

from julian.time_parsers import (
    sec_from_string,
    secs_in_strings,
)

from julian._DEPRECATED import (
    time_in_string,
    times_in_string,
)

from julian._exceptions import JulianParseException as JPE
from julian._exceptions import JulianValidateFailure as JVF


def test_time_parsers():

    import warnings
    from julian._warnings import JulianDeprecationWarning
    warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

    # Note: test_time_pyparser.py has more extensive unit tests

    # sec_from_string
    assert sec_from_string('00:00:00.000') == 0.0
    assert sec_from_string('00:00:00') == 0
    assert sec_from_string('00:00:59.000') == 59.0
    assert sec_from_string('00:00:59') == 59

    assert type(sec_from_string('00:00:00.000')) is float
    assert type(sec_from_string('00:00:00')) is int
    assert type(sec_from_string('00:00:59.000')) is float
    assert type(sec_from_string('00:00:59')) is int

    # sec_from_string, leapsecs
    assert sec_from_string('23:59:60.000') == 86400.0
    assert sec_from_string('23:59:69.000') == 86409.0
    with pytest.raises(JPE):
        sec_from_string('23:59:70.000')
    with pytest.raises(JPE):
        sec_from_string('23:59:60', leapsecs=False)

    # sec_from_string, am/pm
    assert sec_from_string('12:00:00 am', ampm=True) == 0
    assert sec_from_string(' 1:00:00 am', ampm=True) == 3600
    assert sec_from_string('11:59:59 am', ampm=True) == 43199
    assert sec_from_string('12:00:00PM ', ampm=True) == 43200
    assert sec_from_string(' 1:00:00 pm', ampm=True) == 43200 + 3600
    assert sec_from_string('11:59:59 pm', ampm=True) == 86399
    assert sec_from_string('11:59:60 pm', ampm=True, leapsecs=True) == 86400
    with pytest.raises(JPE):
        sec_from_string('11:59:60 pm', ampm=True, leapsecs=False)
    with pytest.raises(JPE):
        sec_from_string('23:00:00 am', ampm=True)

    # sec_from_string, floating
    assert sec_from_string('12h',    floating=True) == 43200
    assert sec_from_string('1.5 h',  floating=True) == 5400
    assert sec_from_string('86399s', floating=True) == 86399
    assert sec_from_string('86400s', floating=True, leapsecs=True) == 86400
    assert sec_from_string('1:10.5', floating=True) == 70.5 * 60
    assert sec_from_string('60 M',   floating=True) == 60 * 60

    with pytest.raises(JPE):
        sec_from_string('86400s', floating=True, leapsecs=False)

    # sec_from_string, timezones, am/pm, leapsecs
    assert sec_from_string('00:00 gmt',   timezones=True) == (0, 0)
    assert sec_from_string('0:01 Z',      timezones=True) == (60, 0)
    assert sec_from_string('16:00-08',    timezones=True) == (0, 1)
    assert sec_from_string('16:00 PST',   timezones=True) == (0, 1)
    assert sec_from_string('0:00 cet',    timezones=True) == (86400 - 3600, -1)
    assert sec_from_string('0:00 cest',   timezones=True) == (86400 - 7200, -1)
    assert sec_from_string('12:00am gmt', timezones=True) == (0, 0)
    assert sec_from_string('1:00 am bst', timezones=True) == (0, 0)
    assert sec_from_string('6:59:60 pm est', timezones=True, leapsecs=True) == (86400, 0)

    with pytest.raises(JPE):
        sec_from_string('10:59:59 pm', ampm=False)
    with pytest.raises(JPE):
        sec_from_string('7:59:59 pm est', ampm=True,
                        timezones=False)
    with pytest.raises(JPE):
        sec_from_string('6:59:60 pm est', ampm=True,
                        timezones=True, leapsecs=False)
    with pytest.raises(JVF):
        sec_from_string('7:59:60 pm est', ampm=True,
                        timezones=True, leapsecs=True)

    # secs_in_strings
    assert secs_in_strings('t=00:00:00.000', first=True) == 0.0
    assert secs_in_strings(['...', 't=00:00:00.000'], first=True) == 0.0
    assert secs_in_strings(['...', 't=00:00:00.000']) == [0.]
    assert secs_in_strings(['25:00', 't=00:00:00.000']) == [0.]
    assert secs_in_strings('after midnight, 1:00 am bst or later',
                                     timezones=True) == [(0, 0)]
    assert secs_in_strings('after midnight, 1:00 am bst or later',
                                     timezones=True, substrings=True) == [(0, 0, '1:00 am bst')]

    # DEPRECATED

    # Check time_in_string
    assert time_in_string('This is the time--00:00:00.000') == 0.0
    assert time_in_string('Is this the time? 00:00:00=now') == 0
    assert time_in_string('Time:00:00:59.000 is now') == 59.0
    assert time_in_string('Time (00:00:59)') == 59
    assert time_in_string('Time (00:00:60)') == 60
    assert time_in_string('Time (00:00:99)') is None
    assert time_in_string('whatever') is None

    # Check time_in_string with leap seconds
    assert time_in_string('End time[23:59:60.000]') == 86400.0
    assert time_in_string('End time is 23:59:69.000 and later') == 86409.0
    assert time_in_string('Error 23:5z:00.000:0') is None

    assert time_in_string('End time[23:59:60.000]', remainder=True)[1] == ']'
    assert time_in_string('End time is 23:59:69.000 and later',
                                    remainder=True)[1] == ' and later'

    # Check times_in_string with leap seconds
    assert times_in_string('End time[23:59:60.000]') == [86400.0]
    assert times_in_string('End time is 23:59:69.000 and later') == [86409.0]
    assert times_in_string('Error 23:5z:00.000:0') == []

##########################################################################################
