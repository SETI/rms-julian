##########################################################################################
# UNIT TESTS
##########################################################################################

import julian as j
import numpy as np
import unittest

########################################
# Calendar conversions
########################################

class Test_Calendar_v1(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # day_from_ymd()
        self.assertEqual(j.day_from_ymd(2000,1,1), 0)
        self.assertEqual(j.day_from_ymd(2000,2,[27,28,29]).tolist(),    [57,58,59])
        self.assertEqual(j.day_from_ymd(2000,[1,2,3],1).tolist(),       [ 0,31,60])
        self.assertEqual(j.day_from_ymd([2000,2001,2002],1,1).tolist(), [0,366,731])

        # ymd_from_day()
        self.assertEqual(j.ymd_from_day(0),   (2000,1,1))
        self.assertEqual(j.ymd_from_day(60),  (2000,3,1))
        self.assertEqual(j.ymd_from_day(365), (2000,12,31))
        self.assertEqual(j.ymd_from_day(366), (2001,1,1))

        # yd_from_day()
        self.assertEqual(j.yd_from_day(0), (2000,1))
        self.assertEqual(j.yd_from_day(365), (2000,366))

        # A large number of dates, spanning > 200 years
        daylist = np.arange(-40000,40000,83)

        # Convert to ymd and back
        (ylist, mlist, dlist) = j.ymd_from_day(daylist)
        test_daylist = j.day_from_ymd(ylist, mlist, dlist)

        self.assertTrue(np.all(test_daylist == daylist),
            "Large-scale conversion from day to YMD and back failed")

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), "Month-of-year < 1 found")
        self.assertTrue(np.all(mlist <= 12), "Month-of-year > 12 found")

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), "Day < 1 found")
        self.assertTrue(np.all(dlist <= 31), "Day > 31 found")

        # Another large number of dates, spanning > 200 years
        daylist = np.arange(-40001,40000,79)

        # Convert to yd and back
        (ylist, dlist) = j.yd_from_day(daylist)
        test_daylist = j.day_from_yd(ylist, dlist)

        self.assertTrue(np.all(test_daylist == daylist))

        # Make sure every day is in range
        self.assertTrue(np.all(dlist >= 1), "Day < 1 found")
        self.assertTrue(np.all(dlist <= 366), "Day > 366 found")

        # A large number of months, spanning > 200 years
        monthlist = np.arange(-15002,15000,19)

        # Convert to ym and back
        (ylist, mlist) = j.ym_from_month(monthlist)
        test_monthlist = j.month_from_ym(ylist, mlist)

        self.assertTrue(np.all(test_monthlist == monthlist))

        # Make sure every month is in range
        self.assertTrue(np.all(mlist >= 1), "Month-of-year < 1 found")
        self.assertTrue(np.all(mlist <= 12), "Month-of-year > 12 found")

        # Check the days in each January
        mlist = np.arange(j.month_from_ym(1980,1), j.month_from_ym(2220,1),12)
        self.assertTrue(np.all(j.days_in_month(mlist) == 31),
            "Not every January has 31 days")

        # Check the days in each April
        mlist = np.arange(j.month_from_ym(1980,4), j.month_from_ym(2220,4),12)
        self.assertTrue(np.all(j.days_in_month(mlist) == 30),
            "Not every April has 30 days")

        # Check the days in each year
        ylist = np.arange(1890, 2210)
        dlist = j.days_in_year(ylist)
        self.assertTrue(np.all((dlist == 365) | (dlist == 366)),
            "Not every year has 365 or 366 days")

        # Every leap year is a multiple of four
        select = np.where(dlist == 366)
        self.assertTrue(np.all(ylist[select]%4 == 0),
            "Not every leapyear is a multiple of four")

        # February always has 29 days in a leapyear
        self.assertTrue(np.all(j.days_in_month(j.month_from_ym(ylist[select],2))
            == 29), "Not every leap year February has 29 days")

        # February always has 28 days otherwise
        select = np.where(dlist == 365)
        self.assertTrue(np.all(j.days_in_month(j.month_from_ym(ylist[select],2))
            == 28), "Not every non-leap year February has 28 days")

        # Julian vs. Gregorian calendars around 1 CE
        for use_julian in (False, True):
          start_day = j.day_from_ymd(-10, 1, 1, proleptic=(not use_julian))
          stop_day  = j.day_from_ymd( 11, 1, 1, proleptic=(not use_julian))
          for day in range(start_day, stop_day+1):
            (y, m, d) = j.ymd_from_day(day, proleptic=(not use_julian))
            day2 = j.day_from_ymd(y, m, d, proleptic=(not use_julian))
            self.assertEqual(day, day2)

        # Julian vs. Gregorian calendars around 1582
        for use_julian in (False, True):
          start_day = j.day_from_ymd(1572, 1, 1, proleptic=(not use_julian))
          stop_day  = j.day_from_ymd(1593, 1, 1, proleptic=(not use_julian))
          for day in range(start_day, stop_day+1):
            (y, m, d) = j.ymd_from_day(day, proleptic=(not use_julian))
            day2 = j.day_from_ymd(y, m, d, proleptic=(not use_julian))
            self.assertEqual(day, day2)

        # Reality checks, set_gregorian_start
        self.assertEqual(j.day_from_ymd(-4712, 1, 1, proleptic=False), -2451545)
        self.assertEqual(j.day_from_ymd(-4713,11,24, proleptic=True),  -2451545)
        self.assertEqual(j.days_in_year(1582, proleptic=False), 355)
        self.assertEqual(j.days_in_year(1582, proleptic=True),  365)

        j.set_gregorian_start(None)
        self.assertEqual(j.day_from_ymd(-4713,11,24, proleptic=True),  -2451545)
        self.assertEqual(j.day_from_ymd(-4713,11,24, proleptic=False), -2451545)

        j.set_gregorian_start(1752, 9, 14)
        self.assertEqual(j.days_in_year(1582, proleptic=False), 365)
        self.assertEqual(j.days_in_year(1582, proleptic=True),  365)
        self.assertEqual(j.days_in_year(1752, proleptic=False), 355)
        self.assertEqual(j.days_in_year(1752, proleptic=True),  366)

        j.set_gregorian_start()

########################################
# Leapsecond routines
########################################

class Test_Leapseconds_v1(unittest.TestCase):

    def runTest(self):

        # A large number of dates, spanning > 200 years
        daylist = range(-40001,40000,83)

        # Check all seconds are within the range
        self.assertTrue(np.all(j.seconds_on_day(daylist) >= 86400))
        self.assertTrue(np.all(j.seconds_on_day(daylist) <= 86401))

        self.assertEqual(j.seconds_on_day(j.day_from_ymd(1998,12,31)), 86401)

        # Check case where leap seconds are ignored
        self.assertTrue(np.all(j.seconds_on_day(daylist,False) == 86400))

        self.assertEqual(j.seconds_on_day(j.day_from_ymd(1998,12,31), False), 86400)

########################################
# TAI - UTC conversions
########################################

class Test_TAI_UTC_v1(unittest.TestCase):

    def runTest(self):

        j.set_tai_origin('MIDNIGHT')

        # Check tai_from_day
        self.assertEqual(j.tai_from_day(0), 32)
        self.assertEqual(j.tai_from_day([0,1])[0],    32)
        self.assertEqual(j.tai_from_day([0,1])[1], 86432)

        # Check day_sec_from_tai
        self.assertEqual(j.day_sec_from_tai(32.), (0, 0.))
        self.assertEqual(j.day_sec_from_tai([35.,86435.])[0][0], 0)
        self.assertEqual(j.day_sec_from_tai([35.,86435.])[0][1], 1)
        self.assertEqual(j.day_sec_from_tai([35.,86435.])[1][0], 3.)
        self.assertEqual(j.day_sec_from_tai([35.,86435.])[1][1], 3.)

        # A large number of dates, spanning > 200 years
        daylist = np.arange(-40000,40000,83)

        # Test as a loop
        for day in daylist:
            (test_day, test_sec) = j.day_sec_from_tai(j.tai_from_day(day))
            self.assertEqual(test_day, day, "Day mismatch at " + str(day))
            self.assertEqual(test_sec, 0,   "Sec mismatch at " + str(day))

        # Test as an array operation
        (test_day, test_sec) = j.day_sec_from_tai(j.tai_from_day(daylist))
        self.assertTrue(np.all(test_day == daylist))
        self.assertTrue(np.all(test_sec == 0))

        j.set_tai_origin('NOON')

########################################
# Time-of-day conversions
########################################

class Test_Time_of_Day_v1(unittest.TestCase):

    def runTest(self):

        #Check hms_from_sec
        self.assertEqual(j.hms_from_sec(0), (0, 0, 0),
                         "0 is not (0, 0, 0).")
        self.assertEqual(j.hms_from_sec(86400), (23, 59, 60),
                         "86400 is not (23, 59, 60).")
        self.assertEqual(j.hms_from_sec(86409), (23, 59, 69),
                         "86469 is not (23, 59, 69).")
        self.assertRaises(ValueError, j.hms_from_sec, 86410)
        self.assertRaises(ValueError, j.hms_from_sec, -1.e-300)

        # Check sec_from_hms
        self.assertEqual(j.sec_from_hms(0, 0, 0), 0,
                         "(0, 0, 0) is not 0 seconds.")
        self.assertEqual(j.sec_from_hms(23, 59, 60), 86400,
                         "(23, 59, 60) is not 86400 seconds.")

        # Array tests
        # This makes about 333,000 non-uniformly spaced transcendental numbers
        secs = 86410. * np.sqrt(np.arange(0., 1., 3.e-6))

        # Because HMS times carry extra precision, inversions should be exact
        (h,m,s) = j.hms_from_sec(secs)
        errors = (j.sec_from_hms(h,m,s) - secs)
        self.assertTrue(np.all(errors == 0.))

        # Test all seconds
        seclist = np.arange(0,86410)

        # Convert to hms and back
        (h, m, t) = j.hms_from_sec(seclist)
        test_seclist = j.sec_from_hms(h, m, t)

        self.assertTrue(np.all(test_seclist == seclist),
            'Large-scale conversion from sec to hms and back failed')

########################################
# TDB - TAI conversions
########################################

class Test_TDB_TAI_v1(unittest.TestCase):

    def runTest(self):

        j.set_tai_origin('MIDNIGHT')

        # Check tdb_from_tai
        self.assertAlmostEqual(j.tdb_from_tai(j.tai_from_day(0)),
                               64.18391281194636-43200, places=15)

        # Check tai_from_tdb
        self.assertTrue(abs(j.tai_from_tdb(64.18391281194636)
                                         - j.tai_from_day(0)) < 1.e15)

        j.set_tai_origin('NOON')

        # Test inversions around tdb = 0.
        # A list of two million small numbers spanning 2 sec
        secs = 2.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = j.tdb_from_tai(j.tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-11 * secs))
        self.assertTrue(np.all(errors > -1.e-11 * secs))

        # Now make sure we get the exact same results when we replace arrays by
        # scalars
        for i in range(0, tdbs.size, 1000):
            self.assertEqual(errors[i],
                             j.tdb_from_tai(j.tai_from_tdb(tdbs[i])) - tdbs[i])

        # A list of two million bigger numbers spanning ~ 20 days
        secs = 20. * 86400.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = j.tdb_from_tai(j.tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-15 * secs))
        self.assertTrue(np.all(errors > -1.e-15 * secs))

        # A list of two million still bigger numbers spanning ~ 2000 years
        secs = 2000. * 365. * 86400.
        tdbs = np.arange(-secs, secs, 1.e-6 * secs)
        errors = j.tdb_from_tai(j.tai_from_tdb(tdbs)) - tdbs
        self.assertTrue(np.all(errors <  1.e-15 * secs))
        self.assertTrue(np.all(errors > -1.e-15 * secs))

########################################
# Julian Date and Modified Julian Date
########################################

class Test_JD_MJD_v1(unittest.TestCase):

    def runTest(self):

        # Test integer conversions...
        self.assertEqual(j.mjd_from_day(0), 51544)
        self.assertEqual(j.day_from_mjd(51545), 1)

        self.assertTrue(np.all(j.mjd_from_day(np.arange(10)) ==
                               np.arange(10) + 51544))

        self.assertTrue(np.all(j.day_from_mjd(np.arange(10)) ==
                               np.arange(10) - 51544))

        # Test MJD floating-point conversions spanning 1000 years
        span = 1000. * 365.25
        mjdlist = np.arange(-span, span, np.pi) + j.mjd_jd._MJD_OF_JAN_1_2000

        test = j.mjd_from_time(j.time_from_mjd(mjdlist))
        error = np.max(np.abs(test - mjdlist))
        self.assertTrue(np.max(np.abs(test - mjdlist)) < span * 1.e-15)

        for mjd in mjdlist[:100]:
            error = abs(j.mjd_from_time(j.time_from_mjd(mjd)) - mjd)
            self.assertTrue(error < span * 1.e-15)

        (day,sec) = j.day_sec_from_mjd(mjdlist)
        test = j.mjd_from_day_sec(day,sec)
        error = np.abs(test - mjdlist)
        self.assertTrue(np.max(np.abs(test - mjdlist)) < span * 1.e-15)

        for mjd in mjdlist[:100]:
            (day,sec) = j.day_sec_from_mjd(mjd)
            error = abs(j.mjd_from_day_sec(day,sec) - mjd)
            self.assertTrue(error < span * 1.e-15)

        # Test JD floating-point conversions spanning 100 years
        span = 100. * 365.25
        jdlist = np.arange(-span, span, np.pi/10.) + j.mjd_jd._JD_OF_JAN_1_2000

        test = j.jd_from_time(j.time_from_jd(jdlist))
        error = np.max(np.abs(test - jdlist))
        self.assertTrue(np.max(np.abs(test - jdlist)) < j.mjd_jd._JD_OF_JAN_1_2000*1.e-15)

        for jd in jdlist[:100]:
            error = abs(j.jd_from_time(j.time_from_jd(jd)) - jd)
            self.assertTrue(error < span * 1.e-15)

        (day,sec) = j.day_sec_from_jd(jdlist)
        test = j.jd_from_day_sec(day,sec)
        error = np.abs(test - jdlist)
        self.assertTrue(np.max(np.abs(test - jdlist)) < j.mjd_jd._JD_OF_JAN_1_2000*1.e-15)

        for jd in jdlist[:100]:
            (day,sec) = j.day_sec_from_jd(jd)
            error = abs(j.jd_from_day_sec(day,sec) - jd)
            self.assertTrue(error < span * 1.e-15)

########################################
# Time System conversions
########################################

class Test_Conversions_v1(unittest.TestCase):

    def runTest(self):

        # TAI tests...
        j.set_ut_model('LEAPS')

        # TAI was 31-32 seconds ahead of UTC in 1999,2000,2001
        (day,sec) = j.day_sec_as_type_from_utc((-366,0,366),0.,"TAI")
        self.assertTrue(np.all(day == (-366,0,366)))
        self.assertTrue(np.all(sec == (31.,32.,32.)))

        # Inverse of the above
        (day,sec) = j.utc_from_day_sec_as_type((-366,0,366),32.,"TAI")
        self.assertTrue(np.all(day == (-366,0,366)))
        self.assertTrue(np.all(sec == (1.,0.,0.)))

        # TAI did not jump ahead of UTC at the beginning of 1972
        (day,sec) = j.day_sec_as_type_from_utc(j.day_from_ymd(1972,1,1),0,"TAI")
        self.assertEqual(sec,10)
        (day,sec) = j.day_sec_as_type_from_utc(j.day_from_ymd(1971,12,31),0,"TAI")
        self.assertEqual(sec,10)

        # Inverses of the above
        (day,sec) = j.utc_from_day_sec_as_type(j.day_from_ymd(1972,1,1),10,"TAI")
        self.assertEqual(sec,0)
        (day,sec) = j.utc_from_day_sec_as_type(j.day_from_ymd(1971,12,31),10,"TAI")
        self.assertEqual(sec,0)

        # Now do a batch test 1971-2012. Conversions should be exact.
        daylist = np.arange(j.day_from_ymd(1971,1,1), j.day_from_ymd(2012,1,1))

        (day,sec) = j.day_sec_as_type_from_utc(daylist,43200.,"TAI")
        (dtest,stest) = j.utc_from_day_sec_as_type(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 43200.))

        (day,sec) = j.day_sec_as_type_from_utc(daylist,0.,"TAI")
        (dtest,stest) = j.utc_from_day_sec_as_type(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 0.))

        (day,sec) = j.utc_from_day_sec_as_type(daylist,0.,"TAI")
        (dtest,stest) = j.day_sec_as_type_from_utc(day,sec,"TAI")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(stest == 0.))

        # TDB tests...

        self.assertTrue(abs(j.day_sec_as_type_from_utc(0,0,"TDB")[1]
                            - 64.183927284731055) < 1.e15)
        self.assertTrue(abs(j.utc_from_day_sec_as_type(0,0,"TDB")[1]
                            + 64.183927284731055) < 1.e15)

        (day,sec) = j.day_sec_as_type_from_utc(daylist,43200.,"TDB")
        (dtest,stest) = j.utc_from_day_sec_as_type(day,sec,"TDB")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(np.abs(stest - 43200.) < 1.e-6))

        (day,sec) = j.utc_from_day_sec_as_type(daylist,43200.,"TDB")
        (dtest,stest) = j.day_sec_as_type_from_utc(day,sec,"TDB")
        self.assertTrue(np.all(dtest == daylist))
        self.assertTrue(np.all(np.abs(stest - 43200.) < 1.e-6))

        j.set_ut_model('LEAPS')

########################################
# Formatting Routines
########################################

class Test_Formatting_v1(unittest.TestCase):

    def runTest(self):

        # ymd_format_from_day()
        self.assertEqual(j.ymd_format_from_day(0), "2000-01-01")

        self.assertTrue(np.all(j.ymd_format_from_day([-365,0,366]) ==
                        ["1999-01-01", "2000-01-01", "2001-01-01"]))

        # yd_format_from_day()
        self.assertEqual(j.yd_format_from_day(0), "2000-001")

        self.assertTrue(np.all(j.yd_format_from_day([-365,0,366]) ==
                        ["1999-001", "2000-001", "2001-001"]))

        # Check if yd_format_from_day start from 2000-001
        self.assertEqual(j.yd_format_from_day(0), "2000-001")

        # Check if one day is 86400 seconds
        self.assertEqual(j.hms_format_from_sec(86400), "23:59:60")

        # Check if hms_format_from_sec end with 86410
        self.assertEqual(j.hms_format_from_sec(86409), "23:59:69")

        # Check if hms_format_from_sec returns the correct format.
        self.assertEqual(j.hms_format_from_sec(0), "00:00:00")
        self.assertEqual(j.hms_format_from_sec(0,3), "00:00:00.000")
        self.assertEqual(j.hms_format_from_sec(0,3,'Z'), "00:00:00.000Z")

        # Check if hms_format_from_sec accepts seconds over 86410
        self.assertRaises(ValueError, j.hms_format_from_sec, 86411) #!!!

        # Check if ymdhms_format_from_day_sec returns the correct format.
        self.assertEqual(j.ymdhms_format_from_day_sec(0,0),
                         "2000-01-01T00:00:00")
        self.assertEqual(j.ymdhms_format_from_day_sec(0,0,'T',3),
                         "2000-01-01T00:00:00.000")
        self.assertEqual(j.ymdhms_format_from_day_sec(0,0,'T',3,'Z'),
                         "2000-01-01T00:00:00.000Z")
        self.assertEqual(j.ymdhms_format_from_day_sec(0,0,'T',None),
                         "2000-01-01T00:00:00")
        self.assertEqual(j.ymdhms_format_from_day_sec(0,0,'T',None,'Z'),
                         "2000-01-01T00:00:00Z")

        ymdhms = j.ymdhms_format_from_day_sec([0,366],[0,43200])
        self.assertTrue(np.all(ymdhms == ("2000-01-01T00:00:00",
                                          "2001-01-01T12:00:00")))

        # Check TAI formatting

        j.set_tai_origin('MIDNIGHT')

        # The 32's below are for the offset between TAI and UTC
        self.assertTrue(np.all(j.ydhms_format_from_tai([32.,366.*86400.+32.]) ==
                        ("2000-001T00:00:00", "2001-001T00:00:00")))
        j.set_tai_origin('NOON')

########################################
# ISO format parsers
########################################

class Test_ISO_Parsing_v1(unittest.TestCase):

    def runTest(self):

        # day_from_iso()
        self.assertEqual(j.day_from_iso( "2001-01-01"), 366)

        strings = ["1999-01-01", "2000-01-01", "2001-01-01"]
        days    = [       -365 ,           0 ,         366 ]
        self.assertTrue(np.all(j.day_from_iso(strings) == days))

        strings = [["2000-001", "2000-002"], ["2000-003", "2000-004"]]
        days    = [[        0 ,         1 ], [        2 ,         3 ]]
        self.assertTrue(np.all(j.day_from_iso(strings) == days))

        strings = ["1999-01-01", "2000-01-01", "2001-01+01"]
        self.assertRaises(ValueError, j.day_from_iso, strings, syntax=True)

        strings = ["1999-01-01", "2000-01-01", "2001-01-aa"]
        self.assertRaises(ValueError, j.day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-01- 1"]
        self.assertRaises(ValueError, j.day_from_iso, strings, syntax=True)

        strings = ["1999-01-01", "2000-01-01", "2001-01-00"]
        self.assertRaises(ValueError, j.day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-00-01"]
        self.assertRaises(ValueError, j.day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-13-01"]
        self.assertRaises(ValueError, j.day_from_iso, strings)

        strings = ["1999-01-01", "2000-01-01", "2001-02-29"]
        self.assertRaises(ValueError, j.day_from_iso, strings)

        # sec_from_iso()
        self.assertEqual(j.sec_from_iso("01:00:00"),     3600)
        self.assertEqual(j.sec_from_iso("23:59:60"),    86400)
        self.assertEqual(j.sec_from_iso("23:59:69"),    86409)
        self.assertEqual(j.sec_from_iso("23:59:69Z"),   86409)
        self.assertEqual(j.sec_from_iso("23:59:69.10"), 86409.10)
        self.assertEqual(j.sec_from_iso("23:59:69.5Z"), 86409.5)

        strings = ["00:00:00", "00:01:00", "00:02:00"]
        secs    = [        0 ,        60 ,       120 ]
        self.assertTrue(np.all(j.sec_from_iso(strings) == secs))

        strings = [["00:02:00Z", "00:04:00Z"], ["00:06:00Z", "00:08:01Z"]]
        secs    = [[      120  ,       240  ], [       360 ,        481 ]]
        self.assertTrue(np.all(j.sec_from_iso(strings) == secs))

        strings = ["00:00:00.01", "00:01:00.02", "23:59:69.03"]
        secs    = [        0.01 ,        60.02 ,     86409.03 ]
        self.assertTrue(np.all(j.sec_from_iso(strings) == secs))

        strings = ["00:00:00.01", "00:01:00.02", "00:02+00.03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings, syntax=True)

        strings = ["00:00:00.01", "00:01:00.02", "00:02: 0.03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings, syntax=True)

        strings = ["00:02:00.1Z", "00:04:00.2Z", "00:06:00.3z"]
        self.assertRaises(ValueError, j.sec_from_iso, strings, syntax=True)

        strings = ["00:00:00.01", "00:01:00.02", "00:02:00+03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings, syntax=True)

        strings = ["00:00:00.01", "00:01:00.02", "-0:02:00.03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings, syntax=True)

        strings = ["00:00:00.01", "00:01:00.02", "24:02:00.03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:60:00.03"]
        self.assertRaises(ValueError, j.sec_from_iso, strings)

        strings = ["00:00:00", "00:01:00", "00:00:70"]
        self.assertRaises(ValueError, j.sec_from_iso, strings)

        strings = ["00:00:00.01", "00:01:00.02", "00:00:69.00"]
        self.assertRaises(ValueError, j.sec_from_iso, strings)

        # day_sec_from_iso()
        self.assertEqual(j.day_sec_from_iso( "2001-01-01 01:00:00"), (366,3600))
        self.assertEqual(j.day_sec_from_iso( "2001-01-01T01:00:00"), (366,3600))

        self.assertEqual(j.day_sec_from_iso("1998-12-31 23:59:60"), (-366, 86400))

        self.assertRaises(ValueError, j.day_sec_from_iso, "2000-01-01 23:59:60")
        self.assertRaises(ValueError, j.day_sec_from_iso, "1999-12-31 23:59:61")

        strings = ["1999-01-01", "2000-01-01", "2001-01-01"]
        days    = [       -365 ,           0 ,         366 ]
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[1] == 0))

        strings = [["2000-001", "2000-002"], ["2000-003", "2000-004"]]
        days    = [[        0 ,         1 ], [        2 ,         3 ]]
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[1] == 0))

        strings = ["1998-12-31 23:59:60", "2001-01-01 01:00:01"]
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[1] == secs))

        strings = ["1998-12-31T23:59:60", "2001-01-01T01:00:01"]
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[1] == secs))

        strings = ["1998-12-31 23:59:60Z", "2001-01-01 01:00:01Z"]
        days    = [       -366           ,         366           ]
        secs    = [               86400  ,                 3601  ]
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(j.day_sec_from_iso(strings)[1] == secs))

        strings = ["1998-12-31 23:59:60Z", "2001-01-01x01:00:01Z"]
        self.assertRaises(ValueError, j.day_sec_from_iso, strings, syntax=True)

        strings = ["1998-12-31 23:59:60Z", "1998-12-31 23:59:61Z"]
        self.assertRaises(ValueError, j.day_sec_from_iso, strings)

########################################
# General Parsing Routines
########################################

class Test_General_Parsing_v1(unittest.TestCase):

    def runTest(self):

        # Note: julian_dateparser.py has more extensive unit tests

        # Check if day_from_string works like day_from_ymd
        self.assertEqual(j.day_from_string("2000-01-01"),
                         j.day_from_ymd(2000,1,1))

        # Check day_from_string
        self.assertEqual(j.day_from_string("01-02-2000", "MDY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_from_string("01-02-00", "MDY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_from_string("02-01-2000", "DMY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_from_string("02-01-00", "DMY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_from_string("2000-02-29","DMY"),
                         j.day_from_ymd(2000,2,29))

        # Check date validator
        self.assertRaises(ValueError, j.day_from_string, "2001-11-31")
        self.assertRaises(ValueError, j.day_from_string, "2001-02-29")

        # Check day_in_string
        self.assertEqual(j.day_in_string("Today is 01-02-2000!", "MDY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_in_string("Today is:[01-02-00]", "MDY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_in_string("Is this today?02-01-2000-0", "DMY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_in_string("Test--02-01-00-00", "DMY"),
                         j.day_from_ymd(2000,1,2))
        self.assertEqual(j.day_in_string("Test 2000-02-29=today","DMY"),
                         j.day_from_ymd(2000,2,29))

        # Check days_in_string
        self.assertEqual(j.days_in_string("Today is 01-02-2000!", "MDY"),
                         [j.day_from_ymd(2000,1,2)])
        self.assertEqual(j.days_in_string("Today is:[01-02-00]", "MDY"),
                         [j.day_from_ymd(2000,1,2)])
        self.assertEqual(j.days_in_string("Is this today?02-01-2000-0", "DMY"),
                         [j.day_from_ymd(2000,1,2)])
        self.assertEqual(j.days_in_string("Test--02-01-00-00", "DMY"),
                         [j.day_from_ymd(2000,1,2)])
        self.assertEqual(j.days_in_string("Test 2000-02-29=today","DMY"),
                         [j.day_from_ymd(2000,2,29)])
        self.assertEqual(j.days_in_string("Test 2000=today","DMY"),
                         [])
        self.assertEqual(j.days_in_string("2020-01-01|30-10-20, etc.",),
                         [j.day_from_ymd(2020,1,1), j.day_from_ymd(2030,10,20)])

        # Check date validator
        self.assertEqual(j.day_in_string("Today=(2001-11-31)"), None)
        self.assertEqual(j.day_in_string("Today 2001-02-29T12:34:56"), None)

        self.assertEqual(j.day_in_string("Today 2001-01-01, not tomorrow",
                                         remainder=True), (366, ', not tomorrow'))

        # Check sec_from_string
        self.assertEqual(j.sec_from_string("00:00:00.000"), 0.0)
        self.assertEqual(j.sec_from_string("00:00:00"), 0)
        self.assertEqual(j.sec_from_string("00:00:59.000"), 59.0)
        self.assertEqual(j.sec_from_string("00:00:59"), 59)

        # Check leap seconds
        self.assertEqual(j.sec_from_string("23:59:60.000"), 86400.0)
        self.assertEqual(j.sec_from_string("23:59:69.000"), 86409.0)
        self.assertRaises(ValueError, j.sec_from_string, "23:59:70.000")

        # Check time_in_string
        self.assertEqual(j.time_in_string("This is the time--00:00:00.000"), 0.0)
        self.assertEqual(j.time_in_string("Is this the time? 00:00:00=now"), 0)
        self.assertEqual(j.time_in_string("Time:00:00:59.000 is now"), 59.0)
        self.assertEqual(j.time_in_string("Time (00:00:59)"), 59)

        # Check time_in_string with leap seconds
        self.assertEqual(j.time_in_string("End time[23:59:60.000]"), 86400.0)
        self.assertEqual(j.time_in_string("End time is 23:59:69.000 and later"), 86409.0)
        self.assertEqual(j.time_in_string("Error 23:5z:00.000:0"), None)

        # Check times_in_string with leap seconds
        self.assertEqual(j.times_in_string("End time[23:59:60.000]"), [86400.0])
        self.assertEqual(j.times_in_string("End time is 23:59:69.000 and later"), [86409.0])
        self.assertEqual(j.times_in_string("Error 23:5z:00.000:0"), [])

        # Check day_sec_type_from_string
        self.assertEqual(j.day_sec_type_from_string("2000-01-01 00:00:00.00"),
                         (0, 0.0, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("2000-01-01 00:00:00.00 tai"),
                         (0, 0.0, "TAI"))
        self.assertEqual(j.day_sec_type_from_string("2000-01-01 00:00:00.00Z"),
                         (0, 0.0, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("2000-01-01 00:00:00.00 TDB"),
                         (0, 0.0, "TDB"))

        # Check if DMY is same as MDY
        self.assertEqual(j.day_sec_type_from_string("31-12-2000 12:34:56", "DMY"),
                         j.day_sec_type_from_string("12-31-2000 12:34:56", "MDY"))

        # Check leap second validator
        self.assertEqual(j.day_sec_type_from_string("1998-12-31 23:59:60"),
                         (-366, 86400, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("1998-12-31 23:59:60.99"),
                         (-366, 86400.99, "UTC"))

        self.assertRaises(ValueError, j.day_sec_type_from_string,
                                      "2000-01-01 23:59:60")
        self.assertRaises(ValueError, j.day_sec_type_from_string,
                                      "1999-12-31 23:59:61")

        # Numeric times
        self.assertEqual(j.day_sec_type_from_string("2000-01-01"),
                         (0, 0, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("MJD 51544"),
                         (0, 0, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("51544 (MJD)"),
                         (0, 0, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("JD 2451545"),
                         (0, 43200, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("2451545.  jd"),
                         (0, 43200, "UTC"))
        self.assertEqual(j.day_sec_type_from_string("2451545.  jed"),
                         j.day_sec_type_from_string("JAN-1.5-2000  TDB"))
        self.assertEqual(j.day_sec_type_from_string("51544.5  mjed"),
                         j.day_sec_type_from_string("JAN-1.5-2000  TDB"))

        # Check day_sec_type_in_string
        self.assertEqual(j.day_sec_type_in_string("Time:2000-01-01 00:00:00.00"),
                         (0, 0.0, "UTC"))
        self.assertEqual(j.day_sec_type_in_string("Time[2000-01-01 00:00:00.00 tai]"),
                         (0, 0.0, "TAI"))
        self.assertEqual(j.day_sec_type_in_string("2000-01-01 00:00:00.00 Z=now"),
                         (0, 0.0, "UTC"))
        self.assertEqual(j.day_sec_type_in_string("Today is [[2000-01-01 00:00:00.00 TDB]]"),
                         (0, 0.0, "TDB"))

        # Check if DMY is same as MDY
        self.assertEqual(j.day_sec_type_in_string("Today-31-12-2000 12:34:56!", "DMY"),
                         j.day_sec_type_in_string("Today:12-31-2000 12:34:56?", "MDY"))

        # Check leap second validator
        self.assertEqual(j.day_sec_type_in_string("Date-1998-12-31 23:59:60 xyz"),
                         (-366, 86400, "UTC"))
        self.assertEqual(j.day_sec_type_in_string("Date? 1998-12-31 23:59:60.99 XYZ"),
                         (-366, 86400.99, "UTC"))

        self.assertEqual(j.day_sec_type_in_string("Today 2000-01-01 23:59:60=leapsecond"),
                         None)
        self.assertEqual(j.day_sec_type_in_string("today 1999-12-31 23:59:61 leapsecond"),
                         None)

        # dates_in_string
        self.assertEqual(j.dates_in_string("Time:2000-01-01 00:00:00.00"),
                         [(0, 0.0, "UTC")])
        self.assertEqual(j.dates_in_string("Time[2000-01-01 00:00:00.00 tai]"),
                         [(0, 0.0, "TAI")])
        self.assertEqual(j.dates_in_string("2000-01-01 00:00:00.00 Z=now"),
                         [(0, 0.0, "UTC")])
        self.assertEqual(j.dates_in_string("Today is [[2000-01-01 00:00:00.00 TDB]]"),
                         [(0, 0.0, "TDB")])
        self.assertEqual(j.dates_in_string("Today is [[200z-01-01 0z:00:0z.00 TDB]]"),
                         [])

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
