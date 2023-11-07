##########################################################################################
# julian/test_deltat.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian.calendar import day_from_ymd, ymd_from_day
from julian._deltat  import FuncDeltaT, LeapDeltaT, MergedDeltaT, SplineDeltaT, _MAX_YEAR

INFO = [(1972, 1, 10),
        (1972, 7, 11),
        (1973, 1, 12),
        (1974, 1, 13),
        (1975, 1, 14),
        (1976, 1, 15),
        (1977, 1, 16),
        (1978, 1, 17),
        (1979, 1, 18),
        (1980, 1, 19),
        (1981, 7, 20),
        (1982, 7, 21),
        (1983, 7, 22),
        (1985, 7, 23),
        (1988, 1, 24),
        (1990, 1, 25),
        (1991, 1, 26),
        (1992, 7, 27),
        (1993, 7, 28),
        (1994, 7, 29),
        (1996, 1, 30),
        (1997, 7, 31),
        (1999, 1, 32),
        (2006, 1, 33),
        (2009, 1, 34),
        (2012, 7, 35),
        (2015, 7, 36),
        (2017, 1, 37)]

def delta_t_long_term(y,m,d):
    u = (y - 1820.) / 100.      # m and d are ignored here
    return -20 + 32 * u**2


class Test_DeltaT(unittest.TestCase):

    def test_LeapDeltaT(self):

        dt = LeapDeltaT(INFO, before=9)
        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 9)
        self.assertFalse(dt.is_float)
        self.assertIsInstance(dt.before, numbers.Real)
        self.assertIsInstance(dt.before, numbers.Integral)
        self.assertEqual(dt.update_count, 1)

        self.assertEqual(dt.delta_t_from_ymd(1971, 12),  9)
        self.assertEqual(dt.delta_t_from_ymd(1972,  1), 10)
        self.assertEqual(dt.delta_t_from_ymd(2017,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(_MAX_YEAR, 1), dt.delta_t_from_ymd(2017, 1))

        self.assertIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Real)
        self.assertIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Real)
        self.assertIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Integral)

        self.assertEqual(dt.leapsecs_from_ymd(1971, 12),  9)
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 10)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), dt.leapsecs_from_ymd(2017, 1))

        years = [1971, 1972, 2017, 9999]
        answer = [9, 10, 37, 37]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, 1) == answer))

        self.assertEqual(dt.update_count, 1)

        # insert_leap_second()
        dt.insert_leap_second(2040, 2)
        dt.insert_leap_second(2041, 2, offset=-2)
        self.assertEqual(dt.update_count, 3)
        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 9)

        self.assertEqual(dt.delta_t_from_ymd(1971, 12),  9)
        self.assertEqual(dt.delta_t_from_ymd(1972,  1), 10)
        self.assertEqual(dt.delta_t_from_ymd(2017,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2040,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2040,  2), 38)
        self.assertEqual(dt.delta_t_from_ymd(2041,  1), 38)
        self.assertEqual(dt.delta_t_from_ymd(2041,  2), 36)
        self.assertEqual(dt.delta_t_from_ymd(2042,  1), 36)
        self.assertEqual(dt.delta_t_from_ymd(9999,  1), 36)
        self.assertEqual(dt.delta_t_from_ymd(_MAX_YEAR, 1), dt.delta_t_from_ymd(2041, 2))

        self.assertEqual(dt.leapsecs_from_ymd(1971, 12),  9)
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 10)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  2), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  1), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  2), 36)
        self.assertEqual(dt.leapsecs_from_ymd(2042,  1), 36)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 36)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), dt.leapsecs_from_ymd(2041, 2))

        years = [1971, 1972, 2017, 2040, 2041, 2042, 9999]
        answer = [9, 10, 37, 37, 38, 36, 36]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, 1) == answer))

        self.assertEqual(dt.update_count, 3)

        # before=None
        dt = LeapDeltaT(INFO, before=None)
        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 10)
        self.assertFalse(dt.is_float)

        years = [1971, 1972, 2017, 9999]
        answer = [10, 10, 37, 37]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, 1) == answer))

        # dates out of chronological order
        self.assertRaises(ValueError, LeapDeltaT, INFO + [(2016,1,37)])

        dt = LeapDeltaT(INFO)
        self.assertRaises(ValueError, dt.insert_leap_second, 2016, 1)

        # set_last_year()
        dt = LeapDeltaT(INFO, before=None)
        self.assertEqual(dt.update_count, 1)
        self.assertEqual(dt.last, _MAX_YEAR)

        dt.set_last_year(2040)
        self.assertEqual(dt.update_count, 2)
        self.assertEqual(dt.last, 2040)

        dt.set_last_year(np.inf)
        self.assertEqual(dt.update_count, 3)
        self.assertEqual(dt.last, _MAX_YEAR)


    def test_SplineDeltaT(self):

        dt = SplineDeltaT(INFO, before=9)
        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 9)
        self.assertTrue(dt.is_float)
        self.assertIsInstance(dt.before, numbers.Real)
        self.assertNotIsInstance(dt.before, numbers.Integral)

        self.assertEqual(dt.delta_t_from_ymd(1971, 12),  9)
        self.assertEqual(dt.delta_t_from_ymd(1972,  1), 10)
        self.assertEqual(dt.delta_t_from_ymd(2017,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2017,  2), 37)
        self.assertEqual(dt.delta_t_from_ymd(_MAX_YEAR, 1), dt.delta_t_from_ymd(2017, 1))

        self.assertEqual(dt.leapsecs_from_ymd(1971, 12), 0)
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 0)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 0)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  2), 0)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 0)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), 0)

        years = [1971, 1972, 2017, 9999]
        answer = [9, 10, 37, 37]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, 1) == 0))

        self.assertIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Real)
        self.assertNotIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Real)
        self.assertNotIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Integral)

        day_1976 = day_from_ymd(1976,1,1)
        day_1977 = day_from_ymd(1977,1,1)
        day = 0.5 * (day_1976 + day_1977)
        (y,m,d) = ymd_from_day(0.5 * (day_1976 + day_1977))
        d = d + day % 1
        dt_1976 = dt.delta_t_from_ymd(1976,1)
        dt_1977 = dt.delta_t_from_ymd(1977,1)
        self.assertEqual(dt.delta_t_from_ymd(y,m,d), 0.5 * (dt_1976 + dt_1977))

        fracs = np.arange(1025) / 1024.
        fracs = np.arange(17) / 16.
        day = (1. - fracs) * day_1976 + fracs * day_1977
        (y,m,d) = ymd_from_day(day)
        answer = (1 - fracs) * dt_1976 + fracs * dt_1977
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,m,d) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,m,d) == 0))


    def test_FuncDeltaT(self):

        dt = FuncDeltaT(delta_t_long_term, first=-np.inf, last=np.inf)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertNotEqual(dt.delta_t_from_ymd(2202,1,1), dt.delta_t_from_ymd(2201,1,1))

        dt = FuncDeltaT(delta_t_long_term, first=-np.inf, last=2200, after=100)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertEqual(dt.delta_t_from_ymd(2201,1,1), 100)

        dt = FuncDeltaT(delta_t_long_term, first=1000, last=2200, after=100)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertEqual(dt.delta_t_from_ymd(2201,1,1), 100)
        self.assertEqual(dt.delta_t_from_ymd( 999,1,1), dt.delta_t_from_ymd(1000,1,1))
        self.assertEqual(dt.delta_t_from_ymd(-999,1,1), dt.delta_t_from_ymd(1000,1,1))

        dt = FuncDeltaT(delta_t_long_term, first=1000, before=100)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertEqual(dt.delta_t_from_ymd( 999,1,1), 100)
        self.assertEqual(dt.delta_t_from_ymd(-999,1,1), 100)

        # date ranges...
        dt = FuncDeltaT(delta_t_long_term, first=-np.inf, last=np.inf)
        y = np.arange(-1000, 3000, 10)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))

        dt = FuncDeltaT(delta_t_long_term, first=-np.inf, last=2200, after=100)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertEqual(dt.delta_t_from_ymd(2201,1,1), 100)

        dt = FuncDeltaT(delta_t_long_term, first=-np.inf, last=2200)
        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 0)
        self.assertEqual(dt.delta_t_from_ymd(2202,1,1), dt.delta_t_from_ymd(2201,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt.delta_t_from_ymd(2201,1,1))

        y = np.arange(0, 3000)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        answer[y > 2201] = answer[2201]
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))

        dt = FuncDeltaT(delta_t_long_term, first=1000, last=np.inf)
        y = np.arange(0, 3000)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        answer[y < 1000] = answer[1000]
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))

        dt = FuncDeltaT(delta_t_long_term, first=1000, last=2200)
        y = np.arange(0, 3000)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        answer[y < 1000] = answer[1000]
        answer[y > 2201] = answer[2201]
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))

        dt = FuncDeltaT(delta_t_long_term, first=1000, last=2200, before=9999)
        y = np.arange(0, 3000)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        answer[y < 1000] = 9999
        answer[y > 2201] = answer[2201]
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))

        dt = FuncDeltaT(delta_t_long_term, first=1000, last=2200, before=9999, after=8888)
        y = np.arange(0, 3000)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        answer[y < 1000] = 9999
        answer[y >= 2201] = 8888
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == 0))


    def test_MergedDeltaT(self):

        # Splines through 1990, then leap seconds
        info1 = [rec for rec in INFO if rec[0] <= 1990]
        dt1 = SplineDeltaT(info1, before=7, last=1990)
        dt2 = LeapDeltaT(INFO, before=5)
        dt = MergedDeltaT(dt1, dt2)         # let splines 1972-1990 take precedence

        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 7)
        self.assertTrue(dt.is_float)
        self.assertIsInstance(dt.before, numbers.Real)
        self.assertNotIsInstance(dt.before, numbers.Integral)

        self.assertEqual(dt.delta_t_from_ymd(1971, 12),  7)
        self.assertEqual(dt.delta_t_from_ymd(1972,  1), 10)
        self.assertEqual(dt.delta_t_from_ymd(2017,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2017,  2), 37)
        self.assertEqual(dt.delta_t_from_ymd(9999,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(_MAX_YEAR, 1), dt.delta_t_from_ymd(2017, 1))

        self.assertEqual(dt.leapsecs_from_ymd(1971, 12),  5)    # defined by LeapDeltaT
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 10)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  2), 37)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), dt.leapsecs_from_ymd(2017, 1))

        years = [1971, 1972, 2017, 9999]
        answer = [7, 10, 37, 37]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))

        self.assertIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Real)
        self.assertNotIsInstance(dt.delta_t_from_ymd(1971, 12), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Real)
        self.assertIsInstance(dt.delta_t_from_ymd(9999, 1), numbers.Integral)

        day_1976 = day_from_ymd(1976,1,1)
        day_1977 = day_from_ymd(1977,1,1)
        day = 0.5 * (day_1976 + day_1977)
        (y,m,d) = ymd_from_day(0.5 * (day_1976 + day_1977))
        dt_1976 = dt.delta_t_from_ymd(1976,1)
        dt_1977 = dt.delta_t_from_ymd(1977,1)
        self.assertEqual(dt.delta_t_from_ymd(y,m,d), 0.5 * (dt_1976 + dt_1977))
        self.assertEqual(dt.leapsecs_from_ymd(y,m,d), 15)       # defined by LeapDeltaT

        fracs = np.arange(1025) / 1024.
        day = (1. - fracs) * day_1976 + fracs * day_1977
        (y,m,d) = ymd_from_day(day)
        answer = (1 - fracs) * dt_1976 + fracs * dt_1977
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,m,d) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,m,d) == dt2.leapsecs_from_ymd(y,m,d)))

        # insert_leap_second()
        dt2.insert_leap_second(2040, 2)
        self.assertEqual(dt.leapsecs_from_ymd(1971, 12),  5)
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 10)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  2), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  1), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  2), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2042,  1), 38)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 38)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), dt.leapsecs_from_ymd(2041, 2))

        dt2.insert_leap_second(2041, 2, offset=-2)
        self.assertEqual(dt.first, 1972)
        self.assertEqual(dt.last, _MAX_YEAR)
        self.assertEqual(dt.before, 7)

        self.assertEqual(dt.delta_t_from_ymd(1971, 12),  7)
        self.assertEqual(dt.delta_t_from_ymd(1972,  1), 10)
        self.assertEqual(dt.delta_t_from_ymd(2017,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2040,  1), 37)
        self.assertEqual(dt.delta_t_from_ymd(2040,  2), 38)
        self.assertEqual(dt.delta_t_from_ymd(2041,  1), 38)
        self.assertEqual(dt.delta_t_from_ymd(2041,  2), 36)
        self.assertEqual(dt.delta_t_from_ymd(2042,  1), 36)
        self.assertEqual(dt.delta_t_from_ymd(9999,  1), 36)
        self.assertEqual(dt.delta_t_from_ymd(_MAX_YEAR, 1), dt.delta_t_from_ymd(2041, 2))

        self.assertEqual(dt.leapsecs_from_ymd(1971, 12),  5)
        self.assertEqual(dt.leapsecs_from_ymd(1972,  1), 10)
        self.assertEqual(dt.leapsecs_from_ymd(2017,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(2040,  2), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  1), 38)
        self.assertEqual(dt.leapsecs_from_ymd(2041,  2), 36)
        self.assertEqual(dt.leapsecs_from_ymd(2042,  1), 36)
        self.assertEqual(dt.leapsecs_from_ymd(9999,  1), 36)
        self.assertEqual(dt.leapsecs_from_ymd(_MAX_YEAR, 1), dt.leapsecs_from_ymd(2041, 2))

        years = [1971, 1972, 2017, 2040, 2041, 2042, 9999]
        answer = [7, 10, 37, 37, 38, 36, 36]
        self.assertTrue(np.all(dt.delta_t_from_ymd(years, 1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, 1) == [5] + answer[1:]))

        # Mixed access to internal objects
        years = [1971, 1972, 1976, 2017, 2040, 2041, 2042, 9999]
        months = [1, 1, 7, 1, 1, 1, 1, 1]   # in a leap year, July 2 is the middle day 184
        days   = [1, 1, 2, 1, 1, 1, 1, 1]
        answer = [7, 10, 15.5, 37, 37, 38, 36, 36]
        test = dt.delta_t_from_ymd(years, months, days)
        self.assertTrue(np.all(test == answer))
        self.assertEqual(test.dtype.kind, 'f')

        test = dt.leapsecs_from_ymd(years, months, days)
        answer = [5, 10, 15, 37, 37, 38, 36, 36]
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years, months, days) == answer))
        self.assertEqual(test.dtype.kind, 'i')

        # All dates fall inside leap model
        years = list(range(1991, 2001))
        answer = [26, 26, 27, 28, 29, 30, 30, 31, 32, 32]
        test = dt.delta_t_from_ymd(years, 1)
        self.assertTrue(np.all(test == answer))
        self.assertEqual(test.dtype.kind, 'i')

        test = dt.leapsecs_from_ymd(years, 1)
        self.assertTrue(np.all(test == answer))
        self.assertEqual(test.dtype.kind, 'i')

        # FuncDeltaT and extrapolations
        dt1 = FuncDeltaT(delta_t_long_term, first=-np.inf, last=np.inf)
        dt2 = LeapDeltaT(INFO, before=5)
        dt = MergedDeltaT(dt1, dt2)     # leap seconds are overridden completely

        self.assertEqual(dt.delta_t_from_ymd(1820,1,1), -20)
        self.assertEqual(dt.leapsecs_from_ymd(1820,1,1), 5)

        y = np.arange(-1000, 3000, 10)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1) - answer).max(), 1.e-10)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == dt2.leapsecs_from_ymd(y,1,1)))

        # LeapDeltaT (starting 1972) above FuncDeltaT
        dt1 = FuncDeltaT(delta_t_long_term, first=-np.inf, last=np.inf)
        dt2 = LeapDeltaT(INFO)
        dt = MergedDeltaT(dt2, dt1)
        self.assertEqual(dt.delta_t_from_ymd(1970,1,1), dt1.delta_t_from_ymd(1970,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1990,1,1), dt2.delta_t_from_ymd(1990,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt2.delta_t_from_ymd(9999,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt2.delta_t_from_ymd(2020,1,1))

        self.assertNotIsInstance(dt.delta_t_from_ymd(1970,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1990,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(9999,1,1), numbers.Integral)

        y = np.arange(-1000, 3000, 10)
        answer = -20. + 32 * ((y - 1820.)/100.)**2
        mask = y < 1972
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1)[mask] - answer[mask]).max(), 1.e-10)
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,1,1)[~mask]
                               == dt2.delta_t_from_ymd(y,1,1)[~mask]))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == dt2.leapsecs_from_ymd(y,1,1)))

        # Set last year of LeapDeltaT
        dt2.set_last_year(2050)
        mask = (y < 1972) | (y > 2050)
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1)[mask] - answer[mask]).max(), 1.e-10)
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,1,1)[~mask]
                               == dt2.delta_t_from_ymd(y,1,1)[~mask]))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == dt2.leapsecs_from_ymd(y,1,1)))

        # Insert a negative leap second in 2052
        dt2.insert_leap_second(2052, 1, -1)
        mask = (y < 1972) | (y > 2052)
        self.assertLess(np.abs(dt.delta_t_from_ymd(y,1,1)[mask] - answer[mask]).max(), 1.e-10)
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,1,1)[~mask]
                               == dt2.delta_t_from_ymd(y,1,1)[~mask]))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == dt2.leapsecs_from_ymd(y,1,1)))

        # LeapDeltaT (1972-2040) above FuncDeltaT
        dt1 = FuncDeltaT(delta_t_long_term, first=-np.inf, last=np.inf)
        dt2 = LeapDeltaT(INFO, last=2040)
        dt = MergedDeltaT(dt2, dt1)
        self.assertEqual(dt.delta_t_from_ymd(1970,1,1), dt1.delta_t_from_ymd(1970,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1990,1,1), dt2.delta_t_from_ymd(1990,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2040,1,1), dt2.delta_t_from_ymd(2040,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2041,1,1), dt1.delta_t_from_ymd(2041,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt1.delta_t_from_ymd(9999,1,1))

        self.assertNotIsInstance(dt.delta_t_from_ymd(1970,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1990,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(2040,1,1), numbers.Integral)
        self.assertNotIsInstance(dt.delta_t_from_ymd(2041,1,1), numbers.Integral)
        self.assertNotIsInstance(dt.delta_t_from_ymd(9999,1,1), numbers.Integral)

        # LeapDeltaT (1972-2040) above FuncDeltaT (ending 1960)
        dt1 = FuncDeltaT(delta_t_long_term, first=-np.inf, last=1960)
        dt2 = LeapDeltaT(INFO, last=2040)
        dt = MergedDeltaT(dt2, dt1)
        self.assertEqual(dt.delta_t_from_ymd(1960,1,1), dt1.delta_t_from_ymd(1960,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1970,1,1), dt2.delta_t_from_ymd(1970,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1972,1,1), dt2.delta_t_from_ymd(1972,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1990,1,1), dt2.delta_t_from_ymd(1990,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2040,1,1), dt2.delta_t_from_ymd(2040,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2041,1,1), dt2.delta_t_from_ymd(2041,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt2.delta_t_from_ymd(9999,1,1))

        self.assertNotIsInstance(dt.delta_t_from_ymd(1960,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1970,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1972,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1990,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(2040,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(2041,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(9999,1,1), numbers.Integral)

        # LeapDeltaT (1972-2040) above FuncDeltaT (starting 2050)
        dt1 = FuncDeltaT(delta_t_long_term, first=2050)
        dt2 = LeapDeltaT(INFO, last=2040)
        dt = MergedDeltaT(dt2, dt1)
        self.assertEqual(dt.delta_t_from_ymd(1960,1,1), dt2.delta_t_from_ymd(1960,1,1))
        self.assertEqual(dt.delta_t_from_ymd(1990,1,1), dt2.delta_t_from_ymd(1990,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2040,1,1), dt2.delta_t_from_ymd(2040,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2041,1,1), dt2.delta_t_from_ymd(2041,1,1))
        self.assertEqual(dt.delta_t_from_ymd(2050,1,1), dt1.delta_t_from_ymd(2050,1,1))
        self.assertEqual(dt.delta_t_from_ymd(9999,1,1), dt1.delta_t_from_ymd(9999,1,1))

        self.assertIsInstance(dt.delta_t_from_ymd(1960,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(1990,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(2040,1,1), numbers.Integral)
        self.assertIsInstance(dt.delta_t_from_ymd(2041,1,1), numbers.Integral)
        self.assertNotIsInstance(dt.delta_t_from_ymd(2050,1,1), numbers.Integral)
        self.assertNotIsInstance(dt.delta_t_from_ymd(9999,1,1), numbers.Integral)

        self.assertEqual(dt.leapsecs_from_ymd(1960,1,1), dt2.leapsecs_from_ymd(1960,1,1))
        self.assertEqual(dt.leapsecs_from_ymd(1990,1,1), dt2.leapsecs_from_ymd(1990,1,1))
        self.assertEqual(dt.leapsecs_from_ymd(2040,1,1), dt2.leapsecs_from_ymd(2040,1,1))
        self.assertEqual(dt.leapsecs_from_ymd(2041,1,1), dt2.leapsecs_from_ymd(2041,1,1))
        self.assertEqual(dt.leapsecs_from_ymd(2050,1,1), 37)
        self.assertEqual(dt.leapsecs_from_ymd(9999,1,1), 37)

        self.assertIsInstance(dt.leapsecs_from_ymd(1960,1,1), numbers.Integral)
        self.assertIsInstance(dt.leapsecs_from_ymd(1990,1,1), numbers.Integral)
        self.assertIsInstance(dt.leapsecs_from_ymd(2040,1,1), numbers.Integral)
        self.assertIsInstance(dt.leapsecs_from_ymd(2041,1,1), numbers.Integral)
        self.assertIsInstance(dt.leapsecs_from_ymd(2050,1,1), numbers.Integral)
        self.assertIsInstance(dt.leapsecs_from_ymd(9999,1,1), numbers.Integral)

        y = [1960, 1990, 2040, 2041, 2050, 9999]
        answer = [dt2.delta_t_from_ymd(1960,1,1), dt2.delta_t_from_ymd(1990,1,1),
                  dt2.delta_t_from_ymd(2040,1,1), dt2.delta_t_from_ymd(2041,1,1),
                  dt1.delta_t_from_ymd(2050,1,1), dt1.delta_t_from_ymd(9999,1,1)]
        self.assertTrue(np.all(dt.delta_t_from_ymd(y,1,1) == answer))
        self.assertTrue(np.all(dt.leapsecs_from_ymd(y,1,1) == dt2.leapsecs_from_ymd(y,1,1)))

        # No LeapDeltaT
        dt1 = SplineDeltaT(info1, before=7, last=1990)
        dt2 = FuncDeltaT(delta_t_long_term, first=2050)
        dt = MergedDeltaT(dt1, dt2)
        years = np.array([0, 1000, 1971, 1972, 2017, 2040, 2041, 9999]).reshape(2,4)
        self.assertTrue(np.all(dt.leapsecs_from_ymd(years,1,1) == 0))
        self.assertEqual(dt.leapsecs_from_ymd(years,1,1).shape, years.shape)

        # Nested MergedDeltaT
        dt1 = SplineDeltaT(info1, before=9, last=1990)
        dt2 = LeapDeltaT(INFO)
        dt3 = MergedDeltaT(dt1, dt2)
        dt4 = LeapDeltaT(INFO)
        self.assertRaises(TypeError, MergedDeltaT, dt3, dt4)

        # Duplicated LeapDeltaT
        dt1 = LeapDeltaT(info1, before=9, last=1990)
        dt2 = SplineDeltaT(info1, before=9, last=1990)
        dt3 = LeapDeltaT(INFO)
        self.assertRaises(ValueError, MergedDeltaT, dt1, dt2, dt3)

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
