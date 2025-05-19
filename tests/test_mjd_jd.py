##########################################################################################
# julian/test_mjd_jd.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian.utc_tai_tdb_tt import set_tai_origin

from julian.mjd_jd import (
    day_from_mjd,
    day_sec_from_jd,
    day_sec_from_mjd,
    jd_from_day_sec,
    jd_from_tai,
    jd_from_time,
    mjd_from_day,
    mjd_from_day_sec,
    mjd_from_tai,
    mjd_from_time,
    tai_from_jd,
    tai_from_mjd,
    time_from_jd,
    time_from_mjd,
    _MJD_OF_JAN_1_2000,
    _JD_OF_JAN_1_2000,
)

from julian._DEPRECATED import (
    jed_from_tai,
    jed_from_tdb,
    mjed_from_tai,
    mjed_from_tdb,
    tai_from_jed,
    tai_from_mjed,
    tdb_from_jed,
    tdb_from_mjed,
)

class Test_mjd_jd(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # Test integer conversions...
        self.assertEqual(mjd_from_day(0), 51544)
        self.assertTrue(isinstance(mjd_from_day(0), numbers.Integral))
        self.assertFalse(isinstance(mjd_from_day(0.), numbers.Integral))

        self.assertTrue(np.all(mjd_from_day([0,1] == [51544, 51545])))
        self.assertEqual(mjd_from_day([0,1]).dtype.kind, 'i')
        self.assertEqual(mjd_from_day([0,1.]).dtype.kind, 'f')

        self.assertEqual(day_from_mjd(51545), 1)
        self.assertTrue(isinstance(day_from_mjd(51545), numbers.Integral))
        self.assertFalse(isinstance(day_from_mjd(51545.), numbers.Integral))

        self.assertEqual(day_from_mjd([0,1]).dtype.kind, 'i')
        self.assertEqual(day_from_mjd([0,1.]).dtype.kind, 'f')

        self.assertTrue(np.all(mjd_from_day(np.arange(10)) == np.arange(10) + 51544))
        self.assertTrue(np.all(day_from_mjd(np.arange(10)) == np.arange(10) - 51544))

        # Test integer conversions...
        self.assertEqual(mjd_from_day_sec(0), mjd_from_day(0))
        self.assertTrue(np.all(mjd_from_day_sec([0,1],[0,43200]) == mjd_from_day([0,1.5])))

        self.assertEqual(day_from_mjd(51545), 1)
        self.assertTrue(isinstance(day_from_mjd(51545), numbers.Integral))
        self.assertFalse(isinstance(day_from_mjd(51545.), numbers.Integral))

        self.assertEqual(day_from_mjd([0,1]).dtype.kind, 'i')
        self.assertEqual(day_from_mjd([0,1.]).dtype.kind, 'f')

        self.assertTrue(np.all(mjd_from_day(np.arange(10)) == np.arange(10) + 51544))
        self.assertTrue(np.all(day_from_mjd(np.arange(10)) == np.arange(10) - 51544))

        # Test MJD floating-point conversions spanning 1000 years
        span = 1000. * 365.25
        mjdlist = np.arange(-span, span, 5*np.pi) + _MJD_OF_JAN_1_2000

        for origin in ('MIDNIGHT', 'NOON'):
            set_tai_origin(origin)
            for mjdsys in ('UTC', 'TAI', 'TDB', 'TDT'):
                for timesys in ('UTC', 'TAI', 'TDB', 'TDT'):
                    time = time_from_mjd(mjdlist, mjdsys=mjdsys, timesys=timesys)
                    test = mjd_from_time(time, timesys=timesys, mjdsys=mjdsys)
                    self.assertLess(np.abs(test - mjdlist).max(), span * 1.e-15)

            for mjd in mjdlist[:100]:
                time = time_from_mjd(mjd, mjdsys=mjdsys, timesys=timesys)
                test = mjd_from_time(time, timesys=timesys, mjdsys=mjdsys)
                self.assertLess(abs(test - mjd), span * 1.e-15)

        (day, sec) = day_sec_from_mjd(mjdlist)
        test = mjd_from_day_sec(day, sec)
        self.assertLess(np.abs(test - mjdlist).max(), span * 1.e-15)

        for mjd in mjdlist[:100]:
            (day, sec) = day_sec_from_mjd(mjd)
            test = mjd_from_day_sec(day, sec)
            self.assertLess(abs(test - mjd), span * 1.e-15)

        # Test JD floating-point conversions spanning 100 years
        span = 100. * 365.25
        jdlist = np.arange(-span, span, np.pi) + _JD_OF_JAN_1_2000

        for origin in ('MIDNIGHT', 'NOON'):
            set_tai_origin(origin)
            for jdsys in ('UTC', 'TAI', 'TDB', 'TDT'):
                for timesys in ('UTC', 'TAI', 'TDB', 'TDT'):
                    time = time_from_jd(jdlist, jdsys=jdsys, timesys=timesys)
                    test = jd_from_time(time, timesys=timesys, jdsys=jdsys)
                    self.assertLess(np.abs(test - jdlist).max(), span * 1.e-15)

            for jd in jdlist[:100]:
                time = time_from_jd(jd, jdsys=jdsys, timesys=timesys)
                test = jd_from_time(time, timesys=timesys, jdsys=jdsys)
                self.assertLess(abs(test - jd), span * 1.e-15)

        (day, sec) = day_sec_from_jd(jdlist)
        test = jd_from_day_sec(day, sec)
        self.assertLess(np.abs(test - jdlist).max(), span * 1.e-15)

        for jd in jdlist[:100]:
            (day, sec) = day_sec_from_jd(jd)
            test = jd_from_day_sec(day, sec)
            self.assertLess(abs(test - jd), span * 1.e-15)

        MJD_TIME_CASES = [
            ('TAI', 'UTC', mjd_from_tai , mjd_from_time),
            ('TAI', 'TDB', mjed_from_tai, mjd_from_time),
            ('TDB', 'TDB', mjed_from_tdb, mjd_from_time),
            ('TAI', 'UTC', tai_from_mjd , time_from_mjd),
            ('TAI', 'TDB', tai_from_mjed, time_from_mjd),
            ('TDB', 'TDB', tdb_from_mjed, time_from_mjd),
        ]

        for (timesys, mjdsys, oldfunc, newfunc) in MJD_TIME_CASES:
            self.assertEqual(oldfunc(100), newfunc(100, timesys=timesys, mjdsys=mjdsys))

        JD_TIME_CASES = [
            ('TAI', 'UTC', jd_from_tai , jd_from_time),
            ('TAI', 'TDB', jed_from_tai, jd_from_time),
            ('TDB', 'TDB', jed_from_tdb, jd_from_time),
            ('TAI', 'UTC', tai_from_jd , time_from_jd),
            ('TAI', 'TDB', tai_from_jed, time_from_jd),
            ('TDB', 'TDB', tdb_from_jed, time_from_jd),
        ]

        for (timesys, jdsys, oldfunc, newfunc) in JD_TIME_CASES:
            self.assertEqual(oldfunc(100), newfunc(100, timesys=timesys, jdsys=jdsys))

        for origin in ('MIDNIGHT', 'NOON'):
            set_tai_origin(origin)
            self.assertEqual(mjd_from_time(0., timesys='TAI'),
                             51544.5 if origin == 'NOON' else 51544.0)
            self.assertEqual(mjd_from_time(0., timesys='UTC'),
                             51544.5 if origin == 'NOON' else 51544.0)
            self.assertEqual(mjd_from_day_sec(0, 0), 51544.0)

            self.assertEqual(time_from_mjd(51544.5 if origin == 'NOON' else 51544.0,
                             timesys='TAI'), 0.)
            self.assertEqual(time_from_mjd(51544.0, timesys='UTC'),
                             0. if origin == 'MIDNIGHT' else -43200)
            self.assertEqual(day_sec_from_mjd(51544.0), (0,0))

##########################################################################################
