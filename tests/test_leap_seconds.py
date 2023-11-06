##########################################################################################
# julian/test_leap_seconds.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian             import leap_seconds
from julian.calendar    import day_from_ymd
from julian.iso_parsers import tai_from_iso
from julian._exceptions import JulianValidateFailure

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
    _delta_t_neg1999_3000,
)

class Test_leap_seconds(unittest.TestCase):

    def test_leap_seconds(self):

        set_ut_model('SPICE')
        self.assertEqual(seconds_on_day(day_from_ymd(1971,12,31), timesys='UTC'), 86401)
        self.assertEqual(seconds_on_day(day_from_ymd(1971,12,31), timesys='TAI'), 86401)
        self.assertEqual(leapsecs_from_ym(1958, 1), 9)
        self.assertEqual(leapsecs_from_ym(1964, 1), 9)
        self.assertEqual(leapsecs_from_ym(1971,12), 9)
        self.assertEqual(leapsecs_from_ym(1972, 1), 10)
        self.assertEqual(leapsecs_from_ym(2022, 1), 37)
        self.assertTrue(np.all(leapsecs_from_ym([1971, 1964, 1958], 1) == 9))

        self.assertEqual(delta_t_from_ymd(1958, 1), 9)
        self.assertEqual(delta_t_from_ymd(1964, 1), 9)
        self.assertEqual(delta_t_from_ymd(1971,12), 9)
        self.assertEqual(delta_t_from_ymd(1972, 1), 10)
        self.assertEqual(delta_t_from_ymd(2022, 1), 37)
        self.assertTrue(np.all(delta_t_from_ymd([1971, 1964, 1958], 1) == 9))

        self.assertEqual(leapsecs_from_day(day_from_ymd(1972, 1, 1)), 10)
        self.assertEqual(leapsecs_on_day(day_from_ymd(1972, 1, 1)), 10)
        self.assertEqual(delta_t_from_day(day_from_ymd(1972, 1, 1)), 10)

        self.assertTrue(np.all(leapsecs_from_day(
                                day_from_ymd([1971, 1964, 1958], 1, 1)) == 9))
        self.assertTrue(np.all(delta_t_from_day(
                                day_from_ymd([1971, 1964, 1958], 1, 1)) == 9))

        set_ut_model('LEAPS')
        self.assertEqual(seconds_on_day(day_from_ymd(1971,12,31), timesys='UTC'), 86400)
        self.assertEqual(seconds_on_day(day_from_ymd(1971,12,31), timesys='TAI'), 86400)
        self.assertEqual(leapsecs_from_ymd(1958, 1), 10)
        self.assertEqual(leapsecs_from_ymd(1964, 1), 10)
        self.assertEqual(leapsecs_from_ymd(1971,12), 10)
        self.assertEqual(leapsecs_from_ymd(1972, 1), 10)
        self.assertEqual(leapsecs_from_ymd(2022, 1), 37)
        self.assertTrue(np.all(leapsecs_from_ymd([1972, 1971, 1964, 1958], 1) == 10))

        self.assertEqual(delta_t_from_ymd(1958, 1), 10)
        self.assertEqual(delta_t_from_ymd(1964, 1), 10)
        self.assertEqual(delta_t_from_ymd(1971,12), 10)
        self.assertEqual(delta_t_from_ymd(1972, 1), 10)
        self.assertEqual(delta_t_from_ymd(2022, 1), 37)
        self.assertTrue(np.all(delta_t_from_ymd([1972, 1971, 1964, 1958], 1) == 10))

        self.assertEqual(leapsecs_from_day(day_from_ymd(1972, 1, 1)), 10)
        self.assertEqual(delta_t_from_day(day_from_ymd(1972, 1, 1)), 10)

        self.assertTrue(np.all(leapsecs_from_day(
                                day_from_ymd([1972, 1971, 1964, 1958], 1, 1)) == 10))
        self.assertTrue(np.all(delta_t_from_day(
                                day_from_ymd([1972, 1971, 1964, 1958], 1, 1)) == 10))

        set_ut_model('PRE-1972')
        self.assertEqual(leapsecs_from_ym(1956, 1), 10)
        self.assertEqual(leapsecs_from_ym(1960,12,31), 10)
        self.assertEqual(leapsecs_from_ym(1972,1,1), 10)
        self.assertEqual(leapsecs_from_ym(2022, 1), 37)
        self.assertTrue(np.all(leapsecs_from_ym([1972, 1960], 1) == [10,10]))
        self.assertIsInstance(leapsecs_from_ym(1965,5,1), numbers.Integral)

        self.assertEqual(delta_t_from_ymd(1956, 1), 0)
        self.assertEqual(delta_t_from_ymd(1960,12,31), 0)
        self.assertEqual(delta_t_from_ymd(1972,1,1), 10)
        self.assertEqual(delta_t_from_ymd(2022, 1), 37)
        self.assertTrue(np.all(delta_t_from_ymd([1972, 1960], 1) == [10,0]))
        self.assertNotIsInstance(delta_t_from_ymd(1965,5,1), numbers.Integral)

        set_ut_model('CANON')
        self.assertEqual(leapsecs_from_ym(1956, 1), 10)
        self.assertEqual(leapsecs_from_ym(1960,12,31), 10)
        self.assertEqual(leapsecs_from_ym(1972,1,1), 10)
        self.assertEqual(leapsecs_from_ymd(2022, 1), 37)
        self.assertEqual(leapsecs_from_ymd(9999, 1), 37)
        self.assertTrue(np.all(leapsecs_from_ym([1972, 1960], 1) == [10,10]))
        self.assertIsInstance(leapsecs_from_ym(1965,5,1), numbers.Integral)

        self.assertAlmostEqual(delta_t_from_ymd(1600, 1, 1), 86.1862447)
        self.assertEqual(delta_t_from_ymd(1960,12,31), 0)
        self.assertEqual(delta_t_from_ymd(1972,1,1), 10)
        self.assertEqual(delta_t_from_ymd(2022, 1), 37)
        self.assertEqual(delta_t_from_ymd(9999, 1), 37)
        self.assertTrue(np.all(delta_t_from_ymd([1972, 1960], 1) == [10,0]))
        self.assertNotIsInstance(delta_t_from_ymd(1965,5,1), numbers.Integral)

        set_ut_model('CANON', future=2030)
        year = np.arange(-600, 2300, 10)
        delta_t = delta_t_from_ymd(year,1,1)
        canon_dt = _delta_t_neg1999_3000(year,1,1)
        mask = (year < 1958) | (year >= 2030)
        self.assertTrue(np.all(delta_t[mask] == canon_dt[mask]))

        set_ut_model('PRE-1972')
        year = year[~mask]
        pre1972_dt = delta_t_from_ymd(year,1,1)
        self.assertTrue(np.all(delta_t[~mask] == pre1972_dt))

        year = np.arange(1960, 2020)
        answers = [0, 1.422818, 1.845858, 2.255826, 2.765794, 3.54013 ,
                      4.31317 , 5.25925 , 6.20533 , 7.054002, 8.000082, 8.946162,
                   10, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 22, 23, 23,
                   24, 24, 25, 26, 26, 27, 28, 29, 30, 30, 31, 32, 32, 32, 32, 32,
                   32, 32, 33, 33, 33, 34, 34, 34, 34, 35, 35, 35, 36, 37, 37, 37]

        self.assertLess(np.abs(delta_t_from_ymd(year,1,1) - answers).max(), 1.e-14)

        set_ut_model('SPICE')
        answers = 12*[9] + answers[12:]
        self.assertTrue(np.all(delta_t_from_ymd(year,1,1) == answers))

        set_ut_model('LEAPS')

        # insert_leap_second()
        count = leapsecs_from_ym(2021,1)
        insert_leap_second(2020,7)
        self.assertEqual(leapsecs_from_ym(2021,1), count + 1)

        insert_leap_second(2020,9,3)
        self.assertEqual(leapsecs_from_ym(2021,1), count + 4)

        insert_leap_second(2020,11,-4)
        self.assertEqual(leapsecs_from_ym(2021,1), count)

        # Restore without added leap seconds
        load_lsk()
        self.assertEqual(leapsecs_from_ym(2021,1), count)
        self.assertEqual(leap_seconds._SELECTED_UT_MODEL, 'LEAPS')
        self.assertIs(leap_seconds._SELECTED_DELTA_T, leap_seconds._DELTA_T_DICT['LEAPS'])

        # A large number of dates, spanning > 200 years
        daylist = range(-40001, 40000, 83)

        for name in ('LEAPS', 'SPICE', 'PRE-1972', 'CANON'):
            set_ut_model(name)

            # Check all seconds are within the range
            self.assertTrue(np.all(seconds_on_day(daylist) >= 86400))
            self.assertTrue(np.all(seconds_on_day(daylist) <= 86401))

            self.assertEqual(seconds_on_day(day_from_ymd(1998,12,31)), 86401)
            self.assertEqual(seconds_on_day(day_from_ymd(1972, 6,30)), 86401)

            # Check cases where leap seconds are ignored
            self.assertTrue(np.all(seconds_on_day(daylist, leapsecs=False) == 86400))
            self.assertEqual(seconds_on_day(day_from_ymd(1998,12,31), leapsecs=False),
                                            86400)

            for secs, y, mon, d in leap_seconds._DELTET_DELTA_AT[1:]:
                day = day_from_ymd(int(y), 1 if mon == 'JAN' else 7, int(d))
                self.assertEqual(leapsecs_from_day(day), int(secs))
                self.assertEqual(leapsecs_from_day(day-1), int(secs)-1)

            self.assertEqual(leapsecs_from_day(day + 10000), int(secs))

        # Go back to the default
        set_ut_model('LEAPS')

        # Restore without added leap seconds
        load_lsk()

    # Test for continuity of the "CANON" model
    def test_delta_t_neg1999_3000(self):

        for year in [-500, 500, 1600, 1700, 1800, 1860, 1900, 1920, 1941, 1961, 1986,
                     2005, 2050, 2150]:

            delta_t = _delta_t_neg1999_3000(year,1,1)

            # Extrapolate value from before the jump in formula
            dt1 = _delta_t_neg1999_3000(year-1, 12, 31.8)
            dt2 = _delta_t_neg1999_3000(year-1, 12, 31.9)
            extrap = 2 * dt2 - dt1

            self.assertLess(abs(extrap - delta_t), 0.26)

    # Negative leap seconds...
    def test_negative_leap_seconds(self):

        insert_leap_second(2030, 1, -1)
        insert_leap_second(2031, 1, -2)
        insert_leap_second(2040, 1, 1)

        self.assertEqual(seconds_on_day(day_from_ymd(2030,1,1)  ), 86400)
        self.assertEqual(seconds_on_day(day_from_ymd(2030,1,1)-1), 86399)

        self.assertEqual(seconds_on_day(day_from_ymd(2031,1,1)  ), 86400)
        self.assertEqual(seconds_on_day(day_from_ymd(2031,1,1)-1), 86398)

        self.assertEqual(seconds_on_day(day_from_ymd(2040,1,1)  ), 86400)
        self.assertEqual(seconds_on_day(day_from_ymd(2040,1,1)-1), 86401)

        self.assertTrue(np.all(seconds_on_day(day_from_ymd([2030,2031,2040],1,1)-1)
                               == [86399, 86398, 86401]))

        tai = tai_from_iso('2030-01-01T00:00:00')
        self.assertEqual(tai_from_iso('2029-12-31T23:59:58', validate=True), tai-1)
        self.assertEqual(tai_from_iso('2029-12-31T23:59:59', validate=False), tai)
        self.assertRaises(JulianValidateFailure,
                          tai_from_iso, '2029-12-31T23:59:59', validate=True)

        tai = tai_from_iso('2031-01-01T00:00:00')
        self.assertEqual(tai_from_iso('2030-12-31T23:59:57', validate=True), tai-1)
        self.assertRaises(JulianValidateFailure,
                          tai_from_iso, '2030-12-31T23:59:58', validate=True)
        self.assertRaises(JulianValidateFailure,
                          tai_from_iso, '2030-12-31T23:59:59', validate=True)

        load_lsk()

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
