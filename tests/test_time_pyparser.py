##########################################################################################
# julian/test_time_pyparser.py
##########################################################################################

import pytest

from pyparsing import ParseException, StringEnd

from tests._helpers import confirm_failure, confirm_success

####################################################################
# hour
####################################################################

def test_hour():

    from julian.time_pyparser import hour, hour_strict, hour_float, \
                                     hour_float_strict, hour_am, hour_pm \

    ################################
    # hour_strict
    ################################

    p = hour_strict + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'HOUR'
    for h in range(24):
        assert p.parse_string('%02d' % h)[0][1] == h

    # Failure
    for h in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(h))
    for h in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(h))
    with pytest.raises(ParseException):
        p.parse_string('24')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # hour
    ################################

    p = hour + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'HOUR'
    for h in range(24):
        assert p.parse_string('%02d' % h)[0][1] == h
    for h in range(10):
        assert p.parse_string(str(h))[0][1] == h
    for h in range(10):
        assert p.parse_string(' ' + str(h))[0][1] == h

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('24')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # hour_float_strict
    ################################

    p = hour_float_strict + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'HOUR'
    for h in range(24):
        assert p.parse_string('%02d.5' % h)[0][1] == h + 0.5

    # Failure
    for h in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(h) + '.5')
    for h in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(h) + '.5')
    with pytest.raises(ParseException):
        p.parse_string('23')
    with pytest.raises(ParseException):
        p.parse_string('24.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0.')
    with pytest.raises(ParseException):
        p.parse_string('000.')

    ################################
    # hour_float
    ################################

    p = hour_float + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'HOUR'
    for h in range(24):
        assert p.parse_string('%02d.5' % h)[0][1] == h + 0.5
    for h in range(10):
        assert p.parse_string(str(h) + '.5')[0][1] == h + 0.5
    for h in range(10):
        assert p.parse_string(' ' + str(h) + '.5')[0][1] == h + 0.5

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('23')
    with pytest.raises(ParseException):
        p.parse_string('24.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000.')

    ################################
    # hour_am
    ################################

    p = hour_am + StringEnd()

    # Success
    assert p.parse_string('01')[0][0] == 'HOUR'
    for h in range(1,12):
        assert p.parse_string('%02d' % h)[0][1] == h
    assert p.parse_string('12')[0][1] == 0
    for h in range(1,10):
        assert p.parse_string(str(h))[0][1] == h
    for h in range(1,10):
        assert p.parse_string(' ' + str(h))[0][1] == h

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('00')
    with pytest.raises(ParseException):
        p.parse_string('13')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # hour_pm
    ################################

    p = hour_pm + StringEnd()

    # Success
    assert p.parse_string('01')[0][0] == 'HOUR'
    for h in range(1,12):
        assert p.parse_string('%02d' % h)[0][1] == h+12
    assert p.parse_string('12')[0][1] == 12
    for h in range(1,10):
        assert p.parse_string(str(h))[0][1] == h+12
    for h in range(1,10):
        assert p.parse_string(' ' + str(h))[0][1] == h+12

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('00')
    with pytest.raises(ParseException):
        p.parse_string('13')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

####################################################################
# minute
####################################################################

def test_minute():

    from julian.time_pyparser import minute, minute_strict, minute_float, \
                                     minute_float_strict, minute1439, \
                                     minute1439_float

    ################################
    # minute_strict
    ################################

    p = minute_strict + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'MINUTE'
    for m in range(60):
        assert p.parse_string('%02d' % m)[0][1] == m

    # Failure
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(m))
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(m))
    with pytest.raises(ParseException):
        p.parse_string('60')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # minute
    ################################

    p = minute + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'MINUTE'
    for m in range(60):
        assert p.parse_string('%02d' % m)[0][1] == m
    for m in range(10):
        assert p.parse_string(' ' + str(m))[0][1] == m

    # Failure
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(m))
    with pytest.raises(ParseException):
        p.parse_string('60')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # minute_float_strict
    ################################

    p = minute_float_strict + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'MINUTE'
    for m in range(60):
        assert p.parse_string('%02d.5' % m)[0][1] == m + 0.5

    # Failure
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(m))
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(m))
    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('60.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0.5')
    with pytest.raises(ParseException):
        p.parse_string('000.5')

    ################################
    # minute_float
    ################################

    p = minute_float + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'MINUTE'
    for m in range(60):
        assert p.parse_string('%02d.5' % m)[0][1] == m + 0.5
    for m in range(10):
        assert p.parse_string(' ' + str(m) + '.5')[0][1] == m + 0.5

    # Failure
    for m in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(m) + '.5')
    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('60.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0.5')
    with pytest.raises(ParseException):
        p.parse_string('000.5')

    ################################
    # minute1439
    ################################

    p = minute1439 + StringEnd()

    # Success
    assert p.parse_string('0')[0][0] == 'MINUTE'
    for m in range(1440):
        assert p.parse_string(str(m))[0][1] == m

    # Failure
    for m in range(100):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(m))
    for m in range(100):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(m))

    with pytest.raises(ParseException):
        p.parse_string('1440')
    with pytest.raises(ParseException):
        p.parse_string('1500')
    with pytest.raises(ParseException):
        p.parse_string('2000')
    with pytest.raises(ParseException):
        p.parse_string(' 1000')
    with pytest.raises(ParseException):
        p.parse_string(' 100')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # minute1439_float
    ################################

    p = minute1439_float + StringEnd()

    # Success
    assert p.parse_string('0.5')[0][0] == 'MINUTE'
    for m in range(1440):
        assert p.parse_string(str(m) + '.5')[0][1] == m + 0.5

    # Failure
    for m in range(100):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(m))
    for m in range(100):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(m))

    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('1440')
    with pytest.raises(ParseException):
        p.parse_string('1500')
    with pytest.raises(ParseException):
        p.parse_string('2000')
    with pytest.raises(ParseException):
        p.parse_string(' 1000')
    with pytest.raises(ParseException):
        p.parse_string(' 100')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

####################################################################
# second
####################################################################

def test_second():

    from julian.time_pyparser import second, second_strict, second_float, \
                                     second_float_strict, second86399, \
                                     second86399_float

    ################################
    # second_strict
    ################################

    p = second_strict + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'SECOND'
    for s in range(60):
        assert p.parse_string('%02d' % s)[0][1] == s

    # Failure
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(s))
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s))
    with pytest.raises(ParseException):
        p.parse_string('60')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # second
    ################################

    p = second + StringEnd()

    # Success
    assert p.parse_string('00')[0][0] == 'SECOND'
    for s in range(60):
        assert p.parse_string('%02d' % s)[0][1] == s
    for s in range(10):
        assert p.parse_string(' ' + str(s))[0][1] == s

    # Failure
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(s))
    with pytest.raises(ParseException):
        p.parse_string('60')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # second_float_strict
    ################################

    p = second_float_strict + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'SECOND'
    for s in range(60):
        assert p.parse_string('%02d.5' % s)[0][1] == s + 0.5

    # Failure
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(s))
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s))
    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('60.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000.5')

    ################################
    # second_float
    ################################

    p = second_float + StringEnd()

    # Success
    assert p.parse_string('00.')[0][0] == 'SECOND'
    for s in range(60):
        assert p.parse_string('%02d.5' % s)[0][1] == s + 0.5
    for s in range(10):
        assert p.parse_string(' ' + str(s) + '.5')[0][1] == s + 0.5

    # Failure
    for s in range(10):
        with pytest.raises(ParseException):
            p.parse_string(str(s) + '.5')
    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('60.')
    with pytest.raises(ParseException):
        p.parse_string(' 10.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0.5')
    with pytest.raises(ParseException):
        p.parse_string('000.5')

    ################################
    # second86399
    ################################

    p = second86399 + StringEnd()

    # Success
    assert p.parse_string('0')[0][0] == 'SECOND'
    for s in (1, 10, 100, 1000, 10000, 80000, 86000, 86300, 86399):
        assert p.parse_string(str(s))[0][1] == s

    # Failure
    for s in (100, 200, 400, 800, 999):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s))
    for s in (100, 200, 400, 800, 999):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(s))

    with pytest.raises(ParseException):
        p.parse_string('86400')
    with pytest.raises(ParseException):
        p.parse_string('87000')
    with pytest.raises(ParseException):
        p.parse_string('90000')
    with pytest.raises(ParseException):
        p.parse_string(' 10000')
    with pytest.raises(ParseException):
        p.parse_string(' 1000')
    with pytest.raises(ParseException):
        p.parse_string(' 100')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # second86399_float
    ################################

    p = second86399_float + StringEnd()

    # Success
    assert p.parse_string('0.5')[0][0] == 'SECOND'
    for s in range(1440):
        assert p.parse_string(str(s) + '.5')[0][1] == s + 0.5

    # Failure
    for s in range(100):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s))
    for s in range(100):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(s))

    with pytest.raises(ParseException):
        p.parse_string('10')
    with pytest.raises(ParseException):
        p.parse_string('1440')
    with pytest.raises(ParseException):
        p.parse_string('1500')
    with pytest.raises(ParseException):
        p.parse_string('2000')
    with pytest.raises(ParseException):
        p.parse_string(' 1000')
    with pytest.raises(ParseException):
        p.parse_string(' 100')
    with pytest.raises(ParseException):
        p.parse_string(' 10')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

####################################################################
# leapsec
####################################################################

def test_leapsec():

    from julian.time_pyparser import leapsec, leapsec_float, \
                                     leapsec86409, leapsec86409_float

    ################################
    # leapsec
    ################################

    p = leapsec + StringEnd()

    # Success
    assert p.parse_string('60')[0][0] == 'SECOND'
    for s in range(60,70):
        assert p.parse_string(str(s))[0][1] == s

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('70')
    with pytest.raises(ParseException):
        p.parse_string('90')
    with pytest.raises(ParseException):
        p.parse_string(' 60')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('0')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # leapsec_float
    ################################

    p = leapsec_float + StringEnd()

    # Success
    assert p.parse_string('60.')[0][0] == 'SECOND'
    for s in range(60,70):
        assert p.parse_string(str(s) + '.5')[0][1] == s + 0.5

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('60')
    with pytest.raises(ParseException):
        p.parse_string('70.')
    with pytest.raises(ParseException):
        p.parse_string(' 60.5')
    with pytest.raises(ParseException):
        p.parse_string('a.')
    with pytest.raises(ParseException):
        p.parse_string('0.5')
    with pytest.raises(ParseException):
        p.parse_string('060.5')

    ################################
    # leapsec86409
    ################################

    p = leapsec86409 + StringEnd()

    # Success
    assert p.parse_string('86400')[0][0] == 'SECOND'
    for s in range(86000, 86410):
        assert p.parse_string(str(s))[0][1] == s

    # Failure
    for s in range(86000, 86400):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s))
    for s in range(86000, 86400):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(s))

    with pytest.raises(ParseException):
        p.parse_string('86410')
    with pytest.raises(ParseException):
        p.parse_string('87000')
    with pytest.raises(ParseException):
        p.parse_string('90000')
    with pytest.raises(ParseException):
        p.parse_string(' 86400')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

    ################################
    # leapsec86409_float
    ################################

    p = leapsec86409_float + StringEnd()

    # Success
    assert p.parse_string('86400.')[0][0] == 'SECOND'
    for s in range(86000, 86410):
        assert p.parse_string(str(s) + '.5')[0][1] == s+ 0.5

    # Failure
    for s in range(86330, 86400):
        with pytest.raises(ParseException):
            p.parse_string(' ' + str(s) + '.')
    for s in range(86300, 86400):
        with pytest.raises(ParseException):
            p.parse_string('0' + str(s) + '.')

    with pytest.raises(ParseException):
        p.parse_string('86400')
    with pytest.raises(ParseException):
        p.parse_string('86410.')
    with pytest.raises(ParseException):
        p.parse_string('87000.')
    with pytest.raises(ParseException):
        p.parse_string('90000.')
    with pytest.raises(ParseException):
        p.parse_string(' 86400.5')
    with pytest.raises(ParseException):
        p.parse_string('a')
    with pytest.raises(ParseException):
        p.parse_string('000')

####################################################################
# timezone
####################################################################

def test_tz():

    from julian.time_pyparser import hhmm_tz, named_tz, timezone

    ################################
    # hhmm_tz
    ################################

    p = hhmm_tz + StringEnd()

    # Success
    assert p.parse_string('Z')[:2] == [('TZ', 'Z'), ('TZMIN', 0)]
    assert p.parse_string('+00')[:2] == [('TZ', '+00'), ('TZMIN', 0)]
    for s in ('-', '+'):
        for h in range(0,15):
            test = s + '%02d' % h
            assert p.parse_string(test)[0][1] == test
            assert p.parse_string(test)[1][1] == 60 * int(s+'1') * h
            for m in (0, 15, 30, 45):
                test1 = test + ':%02d' % m
                assert p.parse_string(test1)[0][1] == test1
                assert p.parse_string(test1)[1][1] == int(s+'1') * (60*h + m)

                test2 = test + '%02d' % m
                assert p.parse_string(test2)[0][1] == test2
                assert p.parse_string(test2)[1][1] == int(s+'1') * (60*h + m)

    assert p.parse_string(' Z')[0] == ('TZ', 'Z')
    assert p.parse_string(' z')[0] == ('TZ', 'Z')

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('+0')
    with pytest.raises(ParseException):
        p.parse_string('+ 0')
    with pytest.raises(ParseException):
        p.parse_string(' +0')
    with pytest.raises(ParseException):
        p.parse_string('+00:14')

    ################################
    # named_tz
    ################################

    p = named_tz + StringEnd()

    # Success
    assert p.parse_string('PST')[:2] == [('TZ', 'PST'), ('TZMIN', -8 * 60)]
    for name, h in [('GMT',0), ('  gmT',0), ('  z',0), ('Z',0),
                    ('EST',-5), (' pdt',-7)]:
        for space in ('', ' '):
            assert p.parse_string(space + name)[0][1] == name.lstrip().upper()
            assert p.parse_string(space + name)[1][1] == 60 * h

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('ABC')

    ################################
    # timezone
    ################################

    p = timezone + StringEnd()

    # Success
    assert p.parse_string('PsT')[:2] == [('TZ', 'PST'), ('TZMIN', -8 * 60)]
    assert p.parse_string('  z')[:2] == [('TZ', 'Z'), ('TZMIN', 0)]
    assert p.parse_string('+00')[:2] == [('TZ', '+00'), ('TZMIN', 0)]
    for s in ('-', '+'):
        for h in range(0,15):
            test = s + '%02d' % h
            sign = -1 if s == '-' else +1
            assert p.parse_string(test)[0][1] == test
            assert p.parse_string(test)[1][1] == 60 * sign * h
            for m in (0, 15, 30, 45):
                test1 = test + ':%02d' % m
                assert p.parse_string(test1)[0][1] == test1
                assert p.parse_string(test1)[1][1] == sign * (60*h + m)

                test2 = test + '%02d' % m
                assert p.parse_string(test2)[0][1] == test2
                assert p.parse_string(test2)[1][1] == sign * (60*h + m)

    for name, h in [('GMT',0), ('EST',-5), ('PDT',-7)]:
        for space in ('', ' '):
            assert p.parse_string(space + name)[0][1] == name
            assert p.parse_string(space + name)[1][1] == 60 * h

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('+0')
    with pytest.raises(ParseException):
        p.parse_string('+ 0')
    with pytest.raises(ParseException):
        p.parse_string(' +0')
    with pytest.raises(ParseException):
        p.parse_string('+00:14')
    with pytest.raises(ParseException):
        p.parse_string('ABC')

####################################################################
# timesys
####################################################################

def test_timesys():

    from julian.time_pyparser import timesys

    p = timesys + StringEnd()

    # Success
    for space in ('', ' '):
        assert p.parse_string(space + 'UTC')[0][1] == 'UTC'
        assert p.parse_string(space + 'utc')[0][1] == 'UTC'
        assert p.parse_string(space + 'UT') [0][1] == 'UTC'
        assert p.parse_string(space + 'UT1')[0][1] == 'UTC'
        assert p.parse_string(space + 'TAI')[0][1] == 'TAI'
        assert p.parse_string(space + 'tai')[0][1] == 'TAI'
        assert p.parse_string(space + 'TDB')[0][1] == 'TDB'
        assert p.parse_string(space + 'ET') [0][1] == 'TDB'
        assert p.parse_string(space + 'TDT')[0][1] == 'TT'
        assert p.parse_string(space + 'TT') [0][1] == 'TT'
        assert p.parse_string(space + 'tt') [0][1] == 'TT'
        assert p.parse_string(space + 'Z')  [0][1] == 'UTC'

    # Failure
    with pytest.raises(ParseException):
        p.parse_string('PST')

####################################################################
# time_pyparser
####################################################################

def time_tester(parser, *, leapsecs=False, ampm=False, timezones=False,
                floating=False, timesys=False, iso_only=False,
                padding=False, embedded=False, failure=False):

    HOURS = []
    for h in [0, 1, 9, 23, 24]:
        HOURS.append((9 if h >= 24 else 0, '%02d' % h, h))
        if h < 10:
            HOURS.append((9 if iso_only else 1, str(h), h))

    MINUTES = []
    for m in [0, 1, 14, 59, 60]:
        MINUTES.append((9 if m >= 60 else 0, '%02d' % m, m))
        if m < 10:
            MINUTES.append((9 if iso_only else 1, '%2d' % m, m))

    SECONDS = []
    for s in [0, 1, 9, 59, 70]:
        SECONDS.append((9 if s >= 70 else 0, '%02d' % s, s))
        if s < 10:
            SECONDS.append((9 if iso_only else 1, '%2d' % s, s))
    for s in [60, 69]:
        SECONDS.append((0 if leapsecs else 9, str(s), s))

    TIMEZONES = [(0, '', 0)]
    if timezones:
        TIMEZONES += [(0, 'Z', 0), (0, '-01:15', -75), (0, '+14', 14*60)]
        if not iso_only:
            TIMEZONES += [(0, ' GMT', 0), (0, 'PST', -8*60)]

    TIMESYS = []
    if timesys:
        TIMESYS = [(0, 'UT', 'UTC'), (0, ' TDT', 'TT'), (0, 'Z', 'UTC')]

    ALL_TIMESYS = ('TDB', 'TT', 'UTC', 'TAI')

    if iso_only:
        PUNCS = [':', '']
    else:
        PUNCS = [':']

    if padding:
        before = '  '
        after = '  '
    else:
        before = ''
        after = ''

    if embedded:
        after = ' xxx'

    if floating:
        SECONDS += [(stat, word + '.5', val + 0.5) for (stat, word, val) in SECONDS]

    msgfmt = ('**** TIME PYPARSER test %d expected %s: "%s"; '
              f'leapsecs={leapsecs}, ampm={ampm}, timezones={timezones}, '
              f'floating={floating}, timesys={timesys}, iso_only={iso_only}, '
              f'padding={padding}, embedded={embedded}')

    STATUS = {
        True : 'FAILURE',
        False: 'SUCCESS',
    }

    count = 0
    for hstat, hword, hval in HOURS:
      for mstat, mword, mval in MINUTES:
        for sstat, sword, sval in SECONDS:
          for zstat, zword, zval in TIMEZONES + TIMESYS:
            for punc in PUNCS:
                test = before + hword + punc + mword + punc + sword + zword + after
                status = hstat + mstat + sstat + zstat
                expect_failure = status > 3 or failure
                count += 1
                msg = msgfmt % (count, STATUS[expect_failure], test)

                if expect_failure:
                    confirm_failure(parser, test, msg=msg)
                else:
                    parse_dict = confirm_success(parser, test, msg=msg,
                                        values=[('HOUR', hval), ('MINUTE', mval),
                                                ('SECOND', sval)])
                    if zval in ALL_TIMESYS:
                        assert 'TIMESYS' in parse_dict, msg
                        assert parse_dict['TIMESYS'] == zval
                    elif zword:
                        assert 'TZ' in parse_dict, msg
                        assert 'TZMIN' in parse_dict, msg
                        assert parse_dict['TZ'] == zword.strip()
                        assert parse_dict['TZMIN'] == zval

    if floating:
        MINUTES += [(stat, word + '.5', val + 0.5) for (stat, word, val) in MINUTES]

    for hstat, hword, hval in HOURS:
      for mstat, mword, mval in MINUTES:
        for zstat, zword, zval in TIMEZONES + TIMESYS:
          for punc in PUNCS:
            test = before + hword + punc + mword + zword + after
            status = hstat + mstat + zstat
            expect_failure = status > 3 or failure
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)

            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('HOUR', hval), ('MINUTE', mval)])
                if zval in ALL_TIMESYS:
                    assert 'TIMESYS' in parse_dict, msg
                    assert parse_dict['TIMESYS'] == zval
                elif zword:
                    assert 'TZ' in parse_dict, msg
                    assert 'TZMIN' in parse_dict, msg
                    assert parse_dict['TZ'] == zword.strip()
                    assert parse_dict['TZMIN'] == zval

    if floating:
        SECONDS = []
        for s in [0, 1, 9, 10, 99, 100, 999, 1000, 9999, 10000, 80000,
                  86000, 86300, 86399, 86400, 86409, 86410, 87000, 9000]:
            if leapsecs:
                stat = 9 * int(s >= 86410)
            else:
                stat = 9 * int(s >= 86400)

            SECONDS.append((stat, str(s), s))
            SECONDS.append((stat, str(s) + '.5', s + 0.5))

        for sstat, sword, sval in SECONDS:
            test = before + sword + 's' + after
            expect_failure = sstat > 1 or failure or iso_only
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)

            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('SECOND', sval)])

        MINUTES = []
        for m in [0, 1, 9, 10, 99, 100, 999, 1000, 1400, 1430, 1439, 1440]:
            MINUTES.append((9 if m >= 1440 else 0, str(m), m))
            MINUTES.append((9 if m >= 1440 else 0, str(m) + '.5', m + 0.5))

        for mstat, mword, mval in MINUTES:
            test = before + mword + 'm' + after
            expect_failure = mstat > 1 or failure or iso_only
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)

            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('MINUTE', mval)])

        HOURS = []
        for h in [0, 1, 9, 10, 23, 24]:
            HOURS.append((9 if h >= 24 else 0, str(h), h))
            HOURS.append((9 if h >= 24 else 0, str(h) + '.5', h + 0.5))

        for hstat, hword, hval in HOURS:
            test = before + hword + ' h' + after
            expect_failure = hstat > 1 or failure or iso_only
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)
            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('HOUR', hval)])

    if not ampm:
        return

    HOURS = []
    for a in (0,1):
      for h in [0, 1, 9, 11, 12, 13]:
        hval = 12 * a + h - (12 if h == 12 else 0)
        stat = 9 if (h == 0 or h > 12) else 0
        suffix = 'am' if a == 0 else ' pm'
        HOURS.append((stat, '%02d' % h, suffix, hval))
        if h < 10:
            HOURS.append((stat, str(h), suffix, hval))

    MINUTES = []
    for m in [0, 1, 59, 60]:
        MINUTES.append((9 if m >= 60 else 0, '%02d' % m, m))
        if m < 10:
            MINUTES.append((9 if iso_only else 1, '%2d' % m, m))

    SECONDS = []
    for s in [0, 1, 59, 70]:
        SECONDS.append((9 if s >= 70 else 0, '%02d' % s, s))
        if s < 10:
            SECONDS.append((1, '%2d' % s, s))
    for s in [60, 61, 69]:
        SECONDS.append((0 if leapsecs else 9, str(s), s))

    for hstat, hword, suffix, hval in HOURS:
      for mstat, mword, mval in MINUTES:
        for sstat, sword, sval in SECONDS:
            test = before + hword + ':' + mword + ':' + sword + suffix + after
            status = hstat + mstat + sstat

            expect_failure = status > 3 or failure
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)

            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('HOUR', hval), ('MINUTE', mval),
                                            ('SECOND', sval)])

    for hstat, hword, suffix, hval in HOURS:
        for mstat, mword, mval in MINUTES:
            test = before + hword + ':' + mword + suffix + after
            status = hstat + mstat
            expect_failure = status > 3 or failure
            count += 1
            msg = msgfmt % (count, STATUS[expect_failure], test)

            if expect_failure:
                confirm_failure(parser, test, msg=msg)
            else:
                parse_dict = confirm_success(parser, test, msg=msg,
                                    values=[('HOUR', hval), ('MINUTE', mval)])

    for hstat, hword, suffix, hval in HOURS:
        test = before + hword + suffix + after
        status = hstat
        expect_failure = status > 3 or failure
        count += 1
        msg = msgfmt % (count, STATUS[expect_failure], test)

        if expect_failure:
            confirm_failure(parser, test, msg=msg)
        else:
            parse_dict = confirm_success(parser, test, msg=msg,
                                values=[('HOUR', hval)])


_MAIN_OPTIONS = [
    (False, False, False, False, False),
    (True,  True,  True,  True,  True),
    (True,  False, False, False, False),
    (False, True,  False, False, False),
    (False, False, True,  False, False),
    (False, False, False, True,  False),
    (False, False, False, False, True),
]

@pytest.mark.parametrize('leapsecs,floating,timezones,timesys,ampm', _MAIN_OPTIONS)
def test_time_pyparser(leapsecs, floating, timezones, timesys, ampm):
    from julian.time_pyparser import time_pyparser
    parser = time_pyparser(leapsecs=leapsecs, ampm=ampm,
                           timezones=timezones, floating=floating,
                           timesys=timesys, iso_only=False,
                           padding=True, embedded=True)
    time_tester(parser, leapsecs=leapsecs, ampm=ampm,
                timezones=timezones, floating=floating,
                timesys=timesys, iso_only=False,
                padding=True, embedded=True)


@pytest.mark.parametrize('leapsecs,floating', [
    (True, False), (True, True), (False, False), (False, True),
])
def test_time_pyparser_iso_only(leapsecs, floating):
    from julian.time_pyparser import time_pyparser
    parser = time_pyparser(leapsecs=leapsecs, ampm=False,
                           timezones=True, floating=floating,
                           timesys=False, iso_only=True,
                           padding=True, embedded=True)
    time_tester(parser, leapsecs=leapsecs, ampm=False,
                timezones=True, floating=floating,
                timesys=False, iso_only=True,
                padding=True, embedded=True)


@pytest.mark.parametrize('padding,embedded', [
    (True, False), (False, True), (False, False),
])
def test_time_pyparser_quick(padding, embedded):
    from julian.time_pyparser import time_pyparser
    parser = time_pyparser(leapsecs=False, ampm=False,
                           timezones=False, floating=False,
                           timesys=False, iso_only=False,
                           padding=padding, embedded=embedded)
    time_tester(parser, leapsecs=False, ampm=False,
                timezones=False, floating=False,
                timesys=False, iso_only=False,
                padding=padding, embedded=embedded)

##########################################################################################
