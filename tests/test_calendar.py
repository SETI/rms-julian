##########################################################################################
# julian/test_calendar.py
##########################################################################################

import numpy as np
import unittest

from julian.calendar import (
    day_from_yd,
    day_from_ymd,
    days_in_year,
    days_in_ym,
    set_gregorian_start,
    yd_from_day,
    ymd_from_day,
)

from julian.DEPRECATED import (
    days_in_month,
    month_from_ym,
    ym_from_month,
)

from julian._exceptions import JulianValidateFailure as jvf

class Test_calendar(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # day_from_ymd()
        self.assertEqual(day_from_ymd(2000,1,1), 0)
        self.assertIs(type(day_from_ymd(2000,1,1)), int)
        self.assertEqual(day_from_ymd(2000,1,1.), 0.)
        self.assertIs(type(day_from_ymd(2000,1,1.)), float)

        self.assertEqual(day_from_ymd(2000,2,[27,28,29]).tolist(),    [57,58,59])
        self.assertEqual(day_from_ymd(2000,[1,2,3],1).tolist(),       [ 0,31,60])
        self.assertEqual(day_from_ymd([2000,2001,2002],1,1).tolist(), [0,366,731])

        self.assertRaises(jvf, day_from_ymd, 2000, 1,  0, validate=True)
        self.assertRaises(jvf, day_from_ymd, 2000, 2, 30, validate=True)
        self.assertRaises(jvf, day_from_ymd, 2000, 0,  1, validate=True)
        self.assertRaises(jvf, day_from_ymd, 2000, 13, 1, validate=True)

        self.assertRaises(jvf, day_from_ymd, [2000,2000], [1, 1], [ 1, 0],
                                             validate=True)
        self.assertRaises(jvf, day_from_ymd, [2000,2000], [2, 2], [28,30],
                                             validate=True)
        self.assertRaises(jvf, day_from_ymd, [2000,2000], [1, 0], [ 1, 1],
                                             validate=True)
        self.assertRaises(jvf, day_from_ymd, [2000,2000], [1,13], [ 1, 1],
                                             validate=True)

        self.assertEqual(day_from_ymd(1582, 10, 15,), -152384)
        self.assertEqual(day_from_ymd(1582, 10, 14, proleptic=True), -152385)
        self.assertRaises(jvf, day_from_ymd, 1582, 10, 14, proleptic=False, validate=True)
        self.assertRaises(jvf, day_from_ymd, [1582,1582], [10,10], [15,14],
                                             proleptic=False, validate=True)
        self.assertEqual(day_from_ymd([1582,1582],[10,10],[15,4],
                                      proleptic=True).tolist(), [-152384,-152395])
        self.assertEqual(day_from_ymd([1582,1582],[10,10],[15,4],
                                       proleptic=False).tolist(),[-152384,-152385])
        self.assertEqual(day_from_ymd([1582,1582],[10,10],[3,4],
                                       proleptic=False).tolist(),[-152386,-152385])

        _ = day_from_ymd(1582, 10, 7, validate=False)
        self.assertRaises(jvf, day_from_ymd, 1582, 10, 7, validate=True)

        _ = day_from_ymd(1582, 10, np.arange(1,32), validate=False)
        self.assertRaises(jvf, day_from_ymd, 1582, 10, np.arange(1,32), validate=True)

        # ymd_from_day()
        self.assertEqual(ymd_from_day(0), (2000, 1, 1))
        self.assertIs(type(ymd_from_day(0)[0]), int)
        self.assertIs(type(ymd_from_day(0)[1]), int)
        self.assertIs(type(ymd_from_day(0)[2]), int)

        self.assertEqual(ymd_from_day(0.), (2000, 1, 1.))
        self.assertIs(type(ymd_from_day(0.)[0]), int)
        self.assertIs(type(ymd_from_day(0.)[1]), int)
        self.assertIs(type(ymd_from_day(0.)[2]), float)

        self.assertEqual(ymd_from_day( 60), (2000, 3, 1))
        self.assertEqual(ymd_from_day(365), (2000,12,31))
        self.assertEqual(ymd_from_day(366), (2001, 1, 1))

        self.assertTrue(np.all(np.array(ymd_from_day([  0,  31]))
                               == ([2000,2000],[ 1, 2],[ 1, 1])))
        self.assertTrue(np.all(np.array(ymd_from_day([ 60,  61]))
                               == ([2000,2000],[ 3, 3],[ 1, 2])))
        self.assertTrue(np.all(np.array(ymd_from_day([365, 364]))
                               == ([2000,2000],[12,12],[31,30])))
        self.assertTrue(np.all(np.array(ymd_from_day([366, 365]))
                               == ([2001,2000],[ 1,12],[ 1,31])))

        self.assertEqual(ymd_from_day(-152384), (1582, 10, 15))
        self.assertEqual(ymd_from_day(-152385, proleptic=True),  (1582, 10, 14))
        self.assertEqual(ymd_from_day(-152385, proleptic=False), (1582, 10,  4))

        self.assertTrue(np.all(np.array(ymd_from_day([-152384,-152385], proleptic=True))
                               == ([1582,1582],[10,10],[15,14])))
        self.assertTrue(np.all(np.array(ymd_from_day([-152384,-152385], proleptic=False))
                               == ([1582,1582],[10,10],[15, 4])))

        # There's some weirdness surrounding March 1, 1 BCE (= astronomical year 0)
        for proleptic in (True, False):
            day = np.arange(day_from_ymd(-101, 1, 1, proleptic=proleptic),
                            day_from_ymd(-102, 1, 2, proleptic=proleptic))
            (y, m, d) = ymd_from_day(day, proleptic=proleptic)
            day2 = day_from_ymd(y, m, d, proleptic=proleptic)
            self.assertTrue(np.all(day == day2))

            for dd in day:
                (y, m, d) = ymd_from_day(dd, proleptic=proleptic)
                day2 = day_from_ymd(y, m, d, proleptic=proleptic)
                self.assertEqual(dd, day2)

        # day_from_yd()
        self.assertEqual(day_from_yd(2000,1), 0)
        self.assertEqual(day_from_yd(2001,[2,3,4]).tolist(),  [367,368,369])
        self.assertEqual(day_from_yd([2000,2001],1).tolist(), [ 0,366])
        self.assertEqual(day_from_yd([2000,2001,2002],[1,2,3]).tolist(), [0,367,733])

        self.assertRaises(jvf, day_from_yd, 2000,  0, validate=True)
        self.assertEqual(day_from_yd(2000, 366, validate=True), 365)
        self.assertRaises(jvf, day_from_yd, 2000, 367, validate=True)
        self.assertRaises(jvf, day_from_yd, 1582, 360, validate=True, proleptic=False)
        self.assertRaises(jvf, day_from_yd, 1582, [300,355,360], validate=True,
                                            proleptic=False)

        # In 1582, not a leap year, October 4 was day of year 277
        self.assertEqual(day_from_yd(1582, 277, proleptic=False), -152385)
        self.assertEqual(day_from_yd(1582, [277,278], proleptic=False).tolist(),
                         [-152385,-152384])
        self.assertEqual(day_from_yd(1582, 277, proleptic=True), -152395)
        self.assertEqual(day_from_yd(1582, [277,278], proleptic=True).tolist(),
                         [-152395,-152394])

        # yd_from_day()
        self.assertEqual(yd_from_day(0), (2000,1))
        self.assertEqual(yd_from_day(365), (2000,366))

        # month_from_ym()
        self.assertEqual(month_from_ym(2000, 1, validate=False), 0)
        self.assertEqual(month_from_ym(2000, 1, validate=True),  0)
        self.assertRaises(jvf, month_from_ym, 2000, 0, validate=True)
        self.assertRaises(jvf, month_from_ym, 2000, 13, validate=True)
        self.assertRaises(jvf, month_from_ym, 2000, [12,14], validate=True)
        self.assertRaises(jvf, month_from_ym, [2000, 2001], [12,14], validate=True)

        # days_in_ym()
        for proleptic in (False, True):
            self.assertEqual(days_in_ym(2000, 2, proleptic=proleptic), 29)
            self.assertEqual(type(days_in_ym(2000, 2, proleptic=proleptic)), int)
            self.assertEqual(days_in_ym(1999, 2, proleptic=proleptic), 28)

            self.assertRaises(jvf, days_in_ym, 2000, 0, proleptic=proleptic,
                                                        validate=True)

            self.assertTrue(np.all(days_in_ym(np.arange(2000,2012), 2, proleptic=proleptic)
                                   == 3*[29,28,28,28]))
            self.assertTrue(np.all(days_in_ym(np.arange(2000,2012), 3, proleptic=proleptic)
                                   == 31))

        self.assertEqual(days_in_ym(1582, 10, proleptic=True), 31)
        self.assertEqual(days_in_ym(1582, 10, proleptic=False), 21)
        self.assertEqual(days_in_ym(1582, [10,11], proleptic=False).tolist(), [21,30])

        # days_in_month()
        self.assertEqual(days_in_month(1), 29)
        self.assertEqual(days_in_month(-11), 28)
        month = month_from_ym(1582, 10)
        self.assertEqual(days_in_month(month, proleptic=True), 31)
        self.assertEqual(days_in_month(month, proleptic=False), 21)
        self.assertEqual(days_in_month([month,month+1], proleptic=False).tolist(),
                         [21,30])

        # days_in_year()
        for proleptic in (False, True):
            self.assertEqual(days_in_year(2000, proleptic=proleptic), 366)
            self.assertEqual(type(days_in_year(2000, proleptic=proleptic)), int)
            self.assertTrue(np.all(days_in_year(np.arange(2000,2012), proleptic=proleptic)
                                   == 3*[366,365,365,365]))

        self.assertEqual(days_in_year(1582, proleptic=False), 355)
        self.assertEqual(days_in_year(1582, proleptic=True),  365)

        # A large number of dates, spanning > 200 years
        daylist = np.arange(-40000,40000,83)

        # Convert to ymd and back
        (ylist, mlist, dlist) = ymd_from_day(daylist)
        test_daylist = day_from_ymd(ylist, mlist, dlist)

        self.assertTrue(np.all(test_daylist == daylist),
                        'Large-scale conversion from day to YMD and back failed')

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), 'Month-of-year < 1 found')
        self.assertTrue(np.all(mlist <= 12), 'Month-of-year > 12 found')

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), 'Day < 1 found')
        self.assertTrue(np.all(dlist <= 31), 'Day > 31 found')

        # Another large number of dates, spanning > 200 years
        daylist = np.arange(-40001,40000,79)

        # Convert to yd and back
        (ylist, dlist) = yd_from_day(daylist)
        test_daylist = day_from_yd(ylist, dlist)

        self.assertTrue(np.all(test_daylist == daylist))

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), 'Day < 1 found')
        self.assertTrue(np.all(dlist <= 366), 'Day > 366 found')

        # A large number of months, spanning > 200 years
        monthlist = np.arange(-15002,15000,19)

        # Convert to ym and back
        (ylist, mlist) = ym_from_month(monthlist)
        test_monthlist = month_from_ym(ylist, mlist)

        self.assertTrue(np.all(test_monthlist == monthlist))

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), 'Month-of-year < 1 found')
        self.assertTrue(np.all(mlist <= 12), 'Month-of-year > 12 found')

        # Check the days in each January
        mlist = np.arange(month_from_ym(1980,1),month_from_ym(2220,1),12)
        self.assertTrue(np.all(days_in_month(mlist) == 31),
            'Not every January has 31 days')

        # Check the days in each April
        mlist = np.arange(month_from_ym(1980,4),month_from_ym(2220,4),12)
        self.assertTrue(np.all(days_in_month(mlist) == 30),
            'Not every April has 30 days')

        # Check the days in each year
        ylist = np.arange(1890, 2210)
        dlist = days_in_year(ylist)
        self.assertTrue(np.all((dlist == 365) | (dlist == 366)),
            'Not every year has 365 or 366 days')

        # Every leap year is a multiple of four
        select = np.where(dlist == 366)
        self.assertTrue(np.all(ylist[select]%4 == 0),
                        'Not every leapyear is a multiple of four')

        # February always has 29 days in a leapyear
        self.assertTrue(np.all(days_in_month(month_from_ym(ylist[select],2)) == 29),
                        'Not every leap year February has 29 days')

        # February always has 28 days otherwise
        select = np.where(dlist == 365)
        self.assertTrue(np.all(days_in_month(month_from_ym(ylist[select],2)) == 28),
                        'Not every non-leap year February has 28 days')

        # Julian vs. Gregorian calendars around 1 CE
        for proleptic in (False, True):
            start_day = day_from_ymd(-10, 1, 1, proleptic=proleptic)
            stop_day  = day_from_ymd( 11, 1, 1, proleptic=proleptic)
            days = []
            for day in range(start_day, stop_day+1):
                days.append(day)

                (y, m, d) = ymd_from_day(day, proleptic=proleptic)
                day2 = day_from_ymd(y, m, d, proleptic=proleptic)
                self.assertEqual(day, day2)

                (y, d) = yd_from_day(day, proleptic=proleptic)
                day2 = day_from_yd(y, d, proleptic=proleptic)
                self.assertEqual(day, day2)

            (y, m, d) = ymd_from_day(days, proleptic=proleptic)
            days2 = day_from_ymd(y, m, d, proleptic=proleptic)
            self.assertTrue(np.all(days2 == days))

            (y, d) = yd_from_day(days, proleptic=proleptic)
            days2 = day_from_yd(y, d, proleptic=proleptic)
            self.assertTrue(np.all(days2 == days))

        # Julian vs. Gregorian calendars around 1582
        for proleptic in (False, True):
            start_day = day_from_ymd(1572, 1, 1, proleptic=proleptic)
            stop_day  = day_from_ymd(1593, 1, 1, proleptic=proleptic)
            days = []
            for day in range(start_day, stop_day+1):
                days.append(day)

                (y, m, d) = ymd_from_day(day, proleptic=proleptic)
                day2 = day_from_ymd(y, m, d, proleptic=proleptic)
                self.assertEqual(day, day2)

                (y, d) = yd_from_day(day, proleptic=proleptic)
                day2 = day_from_yd(y, d, proleptic=proleptic)
                self.assertEqual(day, day2)

            (y, m, d) = ymd_from_day(days, proleptic=proleptic)
            days2 = day_from_ymd(y, m, d, proleptic=proleptic)
            self.assertTrue(np.all(days2 == days))

            (y, d) = yd_from_day(days, proleptic=proleptic)
            days2 = day_from_yd(y, d, proleptic=proleptic)
            self.assertTrue(np.all(days2 == days))

        # Dates between calendars
        _ = day_from_ymd(1582, 10, np.arange(1,32), validate=False, proleptic=False)
        _ = day_from_ymd(1582, 10, np.arange(1,32), validate=True, proleptic=True)
        self.assertRaises(jvf, day_from_ymd, 1582, 10, np.arange(1,32), validate=True,
                                             proleptic=False)
        _ = day_from_ymd(1582,  9, np.arange(1,31), validate=True, proleptic=False)
        _ = day_from_ymd(1582, 11, np.arange(1,31), validate=True, proleptic=False)

        # Math jump on March 1 in leap years before 200
        days = day_from_ymd(np.arange(192,205), 3, 1)
        for day in days:
            (y,m,d) = ymd_from_day(day)
            self.assertEqual(m, 3)
            self.assertEqual(d, 1)

            (y,m,d) = ymd_from_day(day+1)
            self.assertEqual(m, 3)
            self.assertEqual(d, 2)

        (y,m,d) = ymd_from_day(days)
        self.assertTrue(np.all(m == 3))
        self.assertTrue(np.all(d == 1))

        # Reality checks, set_gregorian_start
        self.assertEqual(day_from_ymd(-4712, 1, 1, proleptic=False), -2451545)
        self.assertEqual(day_from_ymd(-4713,11,24, proleptic=True),  -2451545)
        self.assertEqual(days_in_year(1582, proleptic=False), 355)
        self.assertEqual(days_in_year(1582, proleptic=True),  365)

        set_gregorian_start(None)
        self.assertEqual(day_from_ymd(-4713,11,24, proleptic=True),  -2451545)
        self.assertEqual(day_from_ymd(-4713,11,24, proleptic=False), -2451545)

        set_gregorian_start(1752, 9, 14)
        self.assertEqual(days_in_year(1582, proleptic=False), 365)
        self.assertEqual(days_in_year(1582, proleptic=True),  365)
        self.assertEqual(days_in_year(1752, proleptic=False), 355)
        self.assertEqual(days_in_year(1752, proleptic=True),  366)

        set_gregorian_start()

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
