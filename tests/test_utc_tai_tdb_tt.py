##########################################################################################
# julian/test_utc_tai_tdb.py
##########################################################################################

import numbers
import numpy as np
import os
import pytest
import sys

from julian.utc_tai_tdb_tt import (
    day_sec_from_tai,
    day_sec_from_time,
    day_sec_from_utc,
    set_tai_origin,
    tai_from_day,
    tai_from_day_sec,
    tai_from_tdb,
    tai_from_tdt,
    tai_from_tt,
    tai_from_utc,
    tdb_from_tai,
    tdt_from_tai,
    time_from_day_sec,
    time_from_time,
    tt_from_tai,
    utc_from_day,
    utc_from_tai,
)

from julian._DEPRECATED import (
    day_sec_as_type_from_utc,
    utc_from_day_sec_as_type,
)

from julian              import leap_seconds
from julian.calendar     import day_from_ymd
from julian.formatters   import iso_from_tai
from julian.leap_seconds import set_ut_model


def test_utc_tai_tdb_tt():

    import warnings
    from julian._warnings import JulianDeprecationWarning
    warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

    ################################################################
    # Rigorously compare TDB to cspyce ET around all leap seconds
    ################################################################

    import cspyce

    julian_root_dir = os.path.split(sys.modules['julian'].__file__)[0]
    lsk_path = os.path.join(julian_root_dir, 'assets',
                            leap_seconds._LATEST_LSK_NAME)
    cspyce.furnsh(lsk_path)

    set_ut_model('SPICE')
    for origin in ('MIDNIGHT', 'NOON'):
        set_tai_origin(origin)
        for y in range(1970, 2030):
            for m in (1, 7):
                date = f'{y}-{m:02d}-00T00:00:00'
                et0 = cspyce.utc2et(date)
                et_array = np.arange(et0-100, et0+100)
                iso_array = iso_from_tai(tai_from_tdb(et_array), digits=6, ymd=True)
                for k, et in enumerate(et_array):
                    assert iso_array[k] == cspyce.et2utc(et, 'ISOC', 6)

    set_ut_model('LEAPS')

    ########################################
    # UTC-day conversions
    ########################################

    set_tai_origin('MIDNIGHT')

    # Check utc_from_day
    assert utc_from_day(0) == 0
    assert utc_from_day([0,1])[0] == 0
    assert utc_from_day([0,1])[1] == 86400

    assert isinstance(utc_from_day(0), numbers.Integral)
    assert not isinstance(utc_from_day(0.), numbers.Integral)

    # Check day_sec_from_utc
    assert day_sec_from_utc(0) == (0, 0)
    assert day_sec_from_utc([100, 86600])[0][0] == 0
    assert day_sec_from_utc([100, 86600])[0][1] == 1
    assert day_sec_from_utc([100, 86600])[1][0] == 100
    assert day_sec_from_utc([100, 86600])[1][1] == 200

    assert isinstance(day_sec_from_utc([100, 86600])[0][1], numbers.Integral)
    assert isinstance(day_sec_from_utc([100, 86600])[1][1], numbers.Integral)
    assert not isinstance(day_sec_from_utc([100., 86600.])[1][0], numbers.Integral)

    # A large number of dates, spanning > 200 years
    daylist = np.arange(-40000,40000,83)

    # Test as a loop
    for day in daylist:
        (test_day, test_sec) = day_sec_from_utc(utc_from_day(day))
        assert test_day == day
        assert test_sec == 0

    # Test as an array operation
    (test_day, test_sec) = day_sec_from_utc(utc_from_day(daylist))
    assert np.all(test_day == daylist)
    assert np.all(test_sec == 0)

    # Switch UTC origin to NOON

    set_tai_origin('NOON')

    # Check utc_from_day
    assert utc_from_day(0) == -43200
    assert utc_from_day([0,1])[0] == -43200
    assert utc_from_day([0,1])[1] ==  43200

    assert isinstance(utc_from_day(0), numbers.Integral)
    assert not isinstance(utc_from_day(0.), numbers.Integral)

    # Check day_sec_from_utc
    assert day_sec_from_utc(0) == (0, 43200)
    assert day_sec_from_utc([100, 86600])[0][0] == 0
    assert day_sec_from_utc([100, 86600])[0][1] == 1
    assert day_sec_from_utc([100, 86600])[1][0] == 43300
    assert day_sec_from_utc([100, 86600])[1][1] == 43400

    assert isinstance(day_sec_from_utc([100, 86600])[0][1], numbers.Integral)
    assert isinstance(day_sec_from_utc([100, 86600])[1][1], numbers.Integral)
    assert not isinstance(day_sec_from_utc([100., 86600.])[1][0], numbers.Integral)

    # A large number of dates, spanning > 200 years
    daylist = np.arange(-40000,40000,83)

    # Test as a loop
    for day in daylist:
        (test_day, test_sec) = day_sec_from_utc(utc_from_day(day))
        assert test_day == day
        assert test_sec == 0

    # Test as an array operation
    (test_day, test_sec) = day_sec_from_utc(utc_from_day(daylist))
    assert np.all(test_day == daylist)
    assert np.all(test_sec == 0)

    ########################################
    # UTC-TAI conversions
    ########################################

    set_ut_model('LEAPS')
    set_tai_origin('NOON')

    # Check tai_from_day
    assert tai_from_day(0) == 32 - 43200
    assert tai_from_day([0,1])[0] == 32 - 43200
    assert tai_from_day([0,1])[1] == 32 + 43200

    assert isinstance(tai_from_day(0), numbers.Integral)
    assert not isinstance(tai_from_day(0.), numbers.Integral)

    # Check day_sec_from_tai
    assert day_sec_from_tai(32.) == (0, 43200.)
    assert day_sec_from_tai([35.,86435.])[0][0] == 0
    assert day_sec_from_tai([35.,86435.])[0][1] == 1
    assert day_sec_from_tai([35.,86435.])[1][0] == 43203.
    assert day_sec_from_tai([35.,86435.])[1][1] == 43203.

    assert isinstance(day_sec_from_tai([35,86435])[0][1], numbers.Integral)
    assert isinstance(day_sec_from_tai([35,86435])[1][0], numbers.Integral)
    assert not isinstance(day_sec_from_tai([35.,86435.])[1][0], numbers.Integral)

    # utc_from_tai
    assert day_sec_from_utc(utc_from_tai(32)) == (0, 43200.)
    assert day_sec_from_utc(utc_from_tai([35,86435]))[0][0] == 0
    assert day_sec_from_utc(utc_from_tai([35,86435]))[0][1] == 1
    assert day_sec_from_utc(utc_from_tai([35,86435]))[1][0] == 43235-32
    assert day_sec_from_utc(utc_from_tai([35,86435]))[1][1] == 43235-32

    assert isinstance(utc_from_tai(32), numbers.Integral)
    assert isinstance(utc_from_tai([35,86435])[0], numbers.Integral)
    assert not isinstance(utc_from_tai(32.), numbers.Integral)
    assert not isinstance(utc_from_tai([35.,86435.])[0], numbers.Integral)

    # tai_from_utc
    assert day_sec_from_tai(tai_from_utc(0)) == (0, 43200)
    assert day_sec_from_tai(tai_from_utc([100,200]))[0][0] == 0
    assert day_sec_from_tai(tai_from_utc([100,200]))[0][1] == 0
    assert day_sec_from_tai(tai_from_utc([100,200]))[1][0] == 43300
    assert day_sec_from_tai(tai_from_utc([100,200]))[1][1] == 43400

    assert isinstance(tai_from_utc(43200), numbers.Integral)
    assert isinstance(tai_from_utc([100,200])[0], numbers.Integral)
    assert not isinstance(tai_from_utc(43200.), numbers.Integral)
    assert not isinstance(tai_from_utc([100.,200.])[0], numbers.Integral)

    # A large number of dates, spanning > 200 years
    daylist = np.arange(-40000,40000,83)

    # Test as a loop
    for day in daylist:
        (test_day, test_sec) = day_sec_from_tai(tai_from_day(day))
        assert test_day == day, 'Day mismatch at ' + str(day)
        assert test_sec == 0,   'Sec mismatch at ' + str(day)

    # Test as an array operation
    (test_day, test_sec) = day_sec_from_tai(tai_from_day(daylist))
    assert np.all(test_day == daylist)
    assert np.all(test_sec == 0)

    ########################################
    # TAI-TDB conversions
    ########################################

    # Check tdb_from_tai
    assert tdb_from_tai(tai_from_day(0) + 43200) == pytest.approx(64.183927284731055, abs=1e-15)

    # Check tai_from_tdb
    assert tai_from_tdb(64.183927284731055) == pytest.approx(32., abs=1e-15)

    # Test inversions around tdb = 0.
    # A list of two million small numbers spanning 2 sec
    secs = 2.
    tdbs = np.arange(-secs, secs, 1.e-6 * secs)
    errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
    assert np.all(errors <  1.e-11 * secs)
    assert np.all(errors > -1.e-11 * secs)

    # Now make sure we get the exact same results when we replace arrays by
    # scalars
    for i in range(0, tdbs.size, 1000):
        assert errors[i] == tdb_from_tai(tai_from_tdb(tdbs[i])) - tdbs[i]

    # A list of two million bigger numbers spanning ~ 20 days
    secs = 20. * 86400.
    tdbs = np.arange(-secs, secs, 1.e-6 * secs)
    errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
    assert np.all(errors <  1.e-15 * secs)
    assert np.all(errors > -1.e-15 * secs)

    # A list of two million still bigger numbers spanning ~ 2000 years
    secs = 2000. * 365. * 86400.
    tdbs = np.arange(-secs, secs, 1.e-6 * secs)
    errors = tdb_from_tai(tai_from_tdb(tdbs)) - tdbs
    assert np.all(errors <  1.e-15 * secs)
    assert np.all(errors > -1.e-15 * secs)

    ########################################
    # TAI-TT conversions
    ########################################

    assert tt_from_tai(10.) == pytest.approx(42.184, abs=1e-15)
    assert tdt_from_tai(10.) == pytest.approx(42.184, abs=1e-15)

    assert tai_from_tt(10.) == pytest.approx(-22.184, abs=1e-14)
    assert tai_from_tdt(10.) == pytest.approx(-22.184, abs=1e-14)

    set_tai_origin('MIDNIGHT')

    assert tt_from_tai(10. + 43200) == pytest.approx(42.184, abs=1e-11)
    assert tdt_from_tai(10. + 43200) == pytest.approx(42.184, abs=1e-11)

    assert tai_from_tt(32.184) == pytest.approx(43200, abs=1e-14)
    assert tai_from_tdt(32.184) == pytest.approx(43200, abs=1e-14)

    set_tai_origin('NOON')

    ########################################
    # Time System conversions
    ########################################

    offsets_1971_12_31 = {'LEAPS': 10, 'SPICE':9, 'CANON': 9.889649987220764,
                          'PRE-1972': 9.889649987220764}

    # For the batch test of every day 1971-2012. Conversions should be exact.
    daylist = np.arange(day_from_ymd(1971,1,1), day_from_ymd(2012,1,1))

    for model in ('SPICE', 'PRE-1972', 'CANON', 'LEAPS'):
      set_ut_model(model)

      for origin in ('MIDNIGHT', 'NOON'):
        set_tai_origin(origin)

        for value in [-10.e10, -5.e10, -1.e10, 0, 1.e10, 5.e10, 10.e10]:
            assert time_from_time(value, 'UTC', 'TAI') == tai_from_utc(value)
            assert time_from_time(value, 'TDB', 'TAI') == tai_from_tdb(value)
            assert time_from_time(value, 'TT' , 'TAI') == tai_from_tt( value)
            assert time_from_time(value, 'TAI', 'UTC') == utc_from_tai(value)
            assert time_from_time(value, 'TAI', 'TDB') == tdb_from_tai(value)
            assert time_from_time(value, 'TAI', 'TT' ) == tt_from_tai( value)

        t1 = [-10.e10, -5.e10, -1.e10, 0, 1.e10, 5.e10, 10.e10]
        for tsys1 in ('UTC', 'TAI', 'TT', 'TDB'):
          for tsys2 in ('UTC', 'TAI', 'TT', 'TDB'):
            t2 = time_from_time(t1, tsys1, tsys2)
            t3 = time_from_time(t2, tsys2, tsys1)
            assert np.abs(t3-t1).max() < 1.e-11

        assert time_from_day_sec(10, 43200, 'TAI') == \
                         tai_from_day_sec(10, 43200)
        assert time_from_day_sec(10, 43200, 'TDB') == \
                         tdb_from_tai(tai_from_day_sec(10, 43200))
        assert time_from_day_sec(10, 43200, 'TT') == \
                         tt_from_tai(tai_from_day_sec(10, 43200))

        assert day_sec_from_time(10000., 'TAI') == \
                         day_sec_from_tai(10000.)
        assert day_sec_from_time(10000., 'TDB') == \
                         day_sec_from_tai(tai_from_tdb(10000.))
        assert day_sec_from_time(10000., 'TT') == \
                         day_sec_from_tai(tai_from_tt(10000.))

        # "Dates" in other time systems
        tai = time_from_day_sec(365, 32, timesys='TAI', leapsecs=False)
        assert day_sec_from_time(tai, timesys='TAI') == (365, 0)

        tt = time_from_day_sec(365, 64.184, timesys='TT', leapsecs=False)
        assert day_sec_from_time(tt, timesys='TT')[0] == 365
        assert day_sec_from_time(tt, timesys='TT')[1] == pytest.approx(0., abs=1e-14)

        days = np.arange(365, 731)
        tdb = time_from_day_sec(days, 43200., timesys='TDB', leapsecs=False)
        tt  = time_from_day_sec(days, 43200., timesys='TT',  leapsecs=False)

        sec1 = day_sec_from_time(tdb, timesys='TDB')[1]
        sec2 = day_sec_from_time(tt,  timesys='TT')[1]
        diffs = sec1 - sec2
        assert np.abs(diffs).max() < 0.0017
        assert np.abs(diffs.mean()) < 2.e-7

        # TAI tests...

        # TAI offset was 31-32 seconds ahead of UTC in 1999,2000,2001
        (day, sec) = day_sec_as_type_from_utc((-366,0,366), 0., time_type='TAI')
        assert np.all(day == (-366,0,366))
        assert np.all(sec == (31.,32.,32.))

        tai = time_from_day_sec((-366, 0, 366), 0., 'TAI')
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        assert np.all(day == (-366,0,366))
        assert np.all(sec == (31.,32.,32.))

        # Inverse of the above
        (day, sec) = utc_from_day_sec_as_type((-366,0,366), 32., time_type='TAI')
        assert np.all(day == (-366,0,366))
        assert np.all(sec == (1.,0.,0.))

        tai = time_from_day_sec((-366, 0, 366), 32., 'TAI', leapsecs=False)
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=True)
        assert np.all(day == (-366,0,366))
        assert np.all(sec == (1.,0.,0.))

        # TAI offset depended on model before 1972
        (day, sec) = day_sec_as_type_from_utc(day_from_ymd(1972,1,1), 0, time_type='TAI')
        assert sec == 10

        tai = time_from_day_sec(day_from_ymd(1972,1,1), 0., 'TAI')
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        assert sec == 10

        (day, sec) = day_sec_as_type_from_utc(day_from_ymd(1971,12,31), 0, time_type='TAI')
        assert sec == pytest.approx(offsets_1971_12_31[model], abs=1e-14)

        tai = time_from_day_sec(day_from_ymd(1971,12,31), 0., 'TAI')
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        assert sec == pytest.approx(offsets_1971_12_31[model], abs=1e-14)

        # Inverses of the above
        (day, sec) = utc_from_day_sec_as_type(day_from_ymd(1972,1,1), 10, time_type='TAI')
        assert sec == 0

        tai = time_from_day_sec(day_from_ymd(1972,1,1), 10, 'TAI', leapsecs=False)
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=True)
        assert sec == 0

        (day, sec) = utc_from_day_sec_as_type(day_from_ymd(1971,12,31),
                                              offsets_1971_12_31[model]+1, time_type='TAI')
        assert sec == pytest.approx(1, abs=1e-14)

        tai = time_from_day_sec(day_from_ymd(1971,12,31), offsets_1971_12_31[model],
                                'TAI', leapsecs=False)
        (day, sec) = day_sec_from_time(tai+1, 'TAI', leapsecs=True)
        assert sec == pytest.approx(1, abs=1e-14)

        # Batch test 1971-2012. Conversions should be exact.
        (day, sec) = day_sec_as_type_from_utc(daylist, 43200., time_type='TAI')
        (dtest, stest) = utc_from_day_sec_as_type(day, sec, time_type='TAI')
        assert np.all(dtest == daylist)
        assert np.all(stest == 43200.)

        tai = time_from_day_sec(daylist, 43200., 'TAI')
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        tai2 = time_from_day_sec(day, sec, 'TAI', leapsecs=False)
        (dtest, stest) = day_sec_from_time(tai2, 'TAI', leapsecs=True)
        assert np.all(dtest == daylist)
        assert np.all(stest == 43200.)

        (day, sec) = day_sec_as_type_from_utc(daylist, 0., time_type='TAI')
        (dtest,stest) = utc_from_day_sec_as_type(day, sec, time_type='TAI')
        assert np.all(dtest == daylist)
        assert np.all(stest == 0.)

        tai = time_from_day_sec(daylist, 0., 'TAI')
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        tai2 = time_from_day_sec(day, sec, 'TAI', leapsecs=False)
        (dtest, stest) = day_sec_from_time(tai2, 'TAI', leapsecs=True)
        assert np.all(dtest == daylist)
        assert np.all(stest == 0.)

        (day, sec) = utc_from_day_sec_as_type(daylist, 0., time_type='TAI')
        (dtest,stest) = day_sec_as_type_from_utc(day, sec, time_type='TAI')
        assert np.all(dtest == daylist)
        assert np.all(stest == 0.)

        tai = time_from_day_sec(daylist, 0., 'TAI', leapsecs=False)
        (day, sec) = day_sec_from_time(tai, 'TAI', leapsecs=True)
        tai = time_from_day_sec(day, sec, 'TAI', leapsecs=True)
        (dtest, stest) = day_sec_from_time(tai, 'TAI', leapsecs=False)
        assert np.all(dtest == daylist)
        assert np.all(stest == 0.)

        # TDB tests...

        assert abs(day_sec_as_type_from_utc(0, 0, time_type='TDB')[1]
                        - 64.183927284731055) < 1.e15
        assert abs(utc_from_day_sec_as_type(0, 0, time_type='TDB')[1]
                        + 64.183927284731055) < 1.e15

        tdb = time_from_day_sec(0, 0., 'TDB')
        (day, sec) = day_sec_from_time(tdb, 'TDB', leapsecs=False)
        assert sec == pytest.approx(64.18391281194636, abs=1e-14)

        (day, sec) = day_sec_as_type_from_utc(daylist, 43200., time_type='TDB')
        (dtest, stest) = utc_from_day_sec_as_type(day, sec, time_type='TDB')
        assert np.all(dtest == daylist)
        assert np.abs(stest - 43200.).max() < 1.e-7

        (day, sec) = utc_from_day_sec_as_type(daylist, 43200., time_type='TDB')
        (dtest, stest) = day_sec_as_type_from_utc(day, sec, time_type='TDB')
        assert np.all(dtest == daylist)
        assert np.abs(stest - 43200.).max() < 2.e-7

        tdb = time_from_day_sec(daylist, 43200., 'TDB', leapsecs=True)
        tdb2 = tdb_from_tai(tai_from_day_sec(daylist, 43200.))
        assert np.all(tdb == tdb2)

        (day, sec) = day_sec_from_time(tdb, 'TDB', leapsecs=False)
        tdb2 = time_from_day_sec(day, sec, 'TDB', leapsecs=False)
        assert np.abs(tdb - tdb2).max() < 1.e-7

        (dtest, stest) = day_sec_from_time(tdb2, 'TDB', leapsecs=True)
        assert np.all(dtest == daylist)
        assert np.abs(stest - 43200.).max() < 1.e-7

        tdb = time_from_day_sec(daylist, 43200., 'TDB', leapsecs=False)
        (day, sec) = day_sec_from_time(tdb, 'TDB', leapsecs=True)
        tdb2 = time_from_day_sec(day, sec, 'TDB', leapsecs=True)
        (dtest, stest) = day_sec_from_time(tdb2, 'TDB', leapsecs=False)
        assert np.all(dtest == daylist)
        assert np.abs(stest - 43200.).max() < 2.e-7

##########################################################################################
