##########################################################################################
# julian/test_datetime_parsers.py
##########################################################################################

import numpy as np
import unittest

from julian.datetime_parsers import (
    day_sec_from_string,
    day_sec_in_strings,
)

from julian._DEPRECATED import (
    day_sec_type_from_string,
    day_sec_type_in_string,
    dates_in_string,
)

from julian.mjd_jd      import jd_from_day_sec, mjd_from_day_sec
from julian._exceptions import JulianParseException as JPE
from julian._exceptions import JulianValidateFailure as JVF


class Test_datetime_parsers(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # Note: test_datetime_pyparser.py has more extensive unit tests

        # Check day_sec_in_strings, day_sec_type_in_string
        for first in (True, False):
          for timesys in (True, False):
            for substrings in (True, False):
              for info in [
                ("Time:2000-01-01 00:00",          0, 0.0, "UTC", '2000-01-01 00:00',
                                                                  '2000-01-01 00:00'),
                ("Time[2000-01-01 00:00 tai]",     0, 0.0, "TAI", '2000-01-01 00:00 tai',
                                                                  '2000-01-01 00:00'),
                ("2000-01-01 00:00 Z=now",         0, 0.0, "UTC", '2000-01-01 00:00 Z',
                                                                  '2000-01-01 00:00'),
                ("Now=[[2000-01-01 00:00 ET]]",    0, 0.0, "TDB", '2000-01-01 00:00 ET',
                                                                  '2000-01-01 00:00'),
                ("2000-01-01 00:00 TDT was today", 0, 0.0, "TT",  '2000-01-01 00:00 TDT',
                                                                  '2000-01-01 00:00'),
              ]:

                (test, day, sec, tsys, substr1, substr2) = info
                result = day_sec_in_strings(test, first=first, timesys=timesys,
                                            timezones=timesys, substrings=substrings)
                answer = [day, sec]
                if timesys:
                    answer.append(tsys)
                    if substrings:
                        answer.append(substr1)
                elif substrings:
                    answer.append(substr2)

                if first:
                    self.assertEqual(result, tuple(answer))
                else:
                    self.assertEqual(result, [tuple(answer)])

        self.assertIsNone(day_sec_in_strings('whatever', first=True))
        self.assertEqual(day_sec_in_strings(['2000-01-01', '2000-01-01 00:01'],
                         treq=True, first=True), (0, 60))

        # Check day_sec_type_in_string, DEPRECATED
        for remainder in (True, False):
            for info in [
                ("Time:2000-01-01 00:00:00.00",         0, 0.0, "UTC", ''),
                ("Time[2000-01-01 00:00:00.00 tai]",    0, 0.0, "TAI", ']'),
                ("Today is [[2000-01-01 00:00:00 ET]]", 0, 0.0, "TDB", ']]'),
                ("2000-01-01 00:00 TDT was today",      0, 0.0, "TT",  ' was today'),
            ]:

                (test, day, sec, tsys, remainder) = info
                result = day_sec_type_in_string(test, remainder=remainder)
                answer = info[1:] if remainder else info[1:-1]
                self.assertEqual(result, answer)

        self.assertEqual(day_sec_type_in_string("[2000-01 00:00:00.00 TDB]]"),
                         None)
        self.assertRaises(JVF, day_sec_type_in_string, "d= 2000-02-31 00:00:00.00 TDB]]")

        # Check if DMY is same as MDY
        self.assertEqual(day_sec_from_string('31-12-2000 12:34:56', order='DMY'),
                         day_sec_from_string('12-31-2000 12:34:56', order='MDY'))
        self.assertEqual(day_sec_type_from_string('31-12-2000 12:34:56', order='DMY'),
                         day_sec_type_from_string('12-31-2000 12:34:56', order='MDY'))

        # Check leap second validator
        self.assertEqual(day_sec_from_string('1998-12-31 23:59:60', timesys=True),
                         (-366, 86400, 'UTC'))
        self.assertEqual(day_sec_from_string('1998-12-31 23:59:60.99', timesys=True),
                         (-366, 86400.99, 'UTC'))
        self.assertEqual(day_sec_from_string('1998-12-31 23:59:60', timesys=False),
                         (-366, 86400))
        self.assertEqual(day_sec_from_string('1998-12-31 23:59:60.99', timesys=False),
                         (-366, 86400.99))
        self.assertEqual(day_sec_type_from_string('1998-12-31 23:59:60'),
                         (-366, 86400, 'UTC'))
        self.assertEqual(day_sec_type_from_string('1998-12-31 23:59:60.99'),
                         (-366, 86400.99, 'UTC'))

        self.assertEqual(type(day_sec_from_string('1998-12-31 23:59:60')[0]), int)
        self.assertEqual(type(day_sec_from_string('1998-12-31 23:59:60')[1]), int)
        self.assertEqual(type(day_sec_from_string('1998-12-31 23:59:60.99')[0]), int)
        self.assertEqual(type(day_sec_from_string('1998-12-31 23:59:60.99')[1]), float)

        self.assertRaises(JVF, day_sec_from_string, '2000-01-01 23:59:60', leapsecs=True)
        self.assertRaises(JVF, day_sec_from_string, '1999-12-31 23:59:61', leapsecs=True)
        self.assertRaises(JPE, day_sec_from_string, 'whatever')

        # MJD on a day with a leap second
        # MJD 51178 is December 31, 1998
        self.assertEqual(day_sec_from_string('MJD 51178.5', mjd=True,
                                             timesys=False, leapsecs=True),
                         (-366, 43200.5))
        self.assertEqual(day_sec_from_string('MJD 51178.5', mjd=True,
                                             timesys=False, leapsecs=False),
                         (-366, 43200.0))
        self.assertEqual(day_sec_from_string('MJD 51178.5', mjd=True,
                                             timesys=True, leapsecs=True),
                         (-366, 43200.5, 'UTC'))
        self.assertEqual(day_sec_from_string('MJD 51178.5', mjd=True,
                                             timesys=True, leapsecs=False),
                         (-366, 43200.0, 'UTC'))

        # explicit time system overrides leapsecs option
        self.assertEqual(day_sec_from_string('MJED 51178.5', mjd=True,
                                             timesys=True, leapsecs=True),
                         (-366, 43200.0, 'TDB'))
        self.assertEqual(day_sec_from_string('MJED 51178.5', mjd=True,
                                             timesys=True, leapsecs=False),
                         (-366, 43200.0, 'TDB'))
        self.assertEqual(day_sec_from_string('MJD 51178.5 tai', mjd=True,
                                             timesys=True, leapsecs=True),
                         (-366, 43200.0, 'TAI'))
        self.assertEqual(day_sec_from_string('MJTD 51178.5', mjd=True,
                                             timesys=True, leapsecs=True),
                         (-366, 43200.0, 'TT'))

        # Numeric times
        self.assertEqual(day_sec_from_string('2000-01-01', timesys=True),
                         (0, 0, 'UTC'))
        self.assertEqual(day_sec_from_string('2000-01-01', timesys=False),
                         (0, 0))
        self.assertEqual(day_sec_type_from_string('MJD 51544'),
                         (0, 0, 'UTC'))
        self.assertEqual(day_sec_from_string('51544 (MJD)', timesys=True),
                         (0, 0, 'UTC'))
        self.assertEqual(day_sec_from_string('51544 (MJD)', timesys=False),
                         (0, 0))
        self.assertEqual(day_sec_type_from_string('JD 2451545'),
                         (0, 43200, 'UTC'))
        self.assertEqual(day_sec_type_from_string('2451545.  jd'),
                         (0, 43200, 'UTC'))
        self.assertEqual(day_sec_type_from_string('2451545.  jed'),
                         day_sec_type_from_string('51544.5  mjed'))
        self.assertEqual(day_sec_type_from_string('2451545.  jd'),
                         (0, 43200, 'UTC'))
        self.assertEqual(day_sec_from_string('JD 2451545.  tdt', timesys=True),
                         (0, 43200, 'TT'))

        # Check earlier rounding error for dates before MJD=0
        for k in range(-20,21):
            mjd = k * 1000
            day_sec = day_sec_from_string('MJD ' + str(mjd))
            self.assertEqual(mjd_from_day_sec(*day_sec), mjd)

            jd = jd_from_day_sec(*day_sec)
            jd = np.round(jd, 1)
            day_sec = day_sec_from_string('JD ' + str(jd))
            self.assertEqual(jd_from_day_sec(*day_sec), jd)

        # Check day_sec_type_in_string
        self.assertEqual(day_sec_type_in_string('Time:2000-01-01 00:00:00.00'),
                         (0, 0.0, 'UTC'))
        self.assertEqual(day_sec_type_in_string('Time[2000-01-01 00:00:00.00 tai]'),
                         (0, 0.0, 'TAI'))
        self.assertEqual(day_sec_type_in_string('2000-01-01 00:00:00.00 Z=now'),
                         (0, 0.0, 'UTC'))
        self.assertEqual(day_sec_type_in_string('Today is [[2000-01-01 00:00:00.00 TDB]]'),
                         (0, 0.0, 'TDB'))

        # Check if DMY is same as MDY
        self.assertEqual(day_sec_type_in_string('Today-31-12-2000 12:34:56!', order='DMY'),
                         day_sec_type_in_string('Today:12-31-2000 12:34:56?', order='MDY'))

        # Check leap second validator
        self.assertEqual(day_sec_type_in_string('Date-1998-12-31 23:59:60 xyz'),
                         (-366, 86400, 'UTC'))
        self.assertEqual(day_sec_type_in_string('Date? 1998-12-31 23:59:60.99 XYZ'),
                         (-366, 86400.99, 'UTC'))

        self.assertRaises(JVF, day_sec_type_in_string,
                          'Today 2000-01-01 23:59:60=leapsecond')
        self.assertRaises(JVF, day_sec_type_in_string,
                          'today 1999-12-31 23:59:61 leapsecond')

        # dates_in_string
        self.assertEqual(dates_in_string('Time:2000-01-01 00:00:00.00'),
                         [(0, 0.0, 'UTC')])
        self.assertEqual(dates_in_string('Time[2000-01-01 00:00:00.00 tai]'),
                         [(0, 0.0, 'TAI')])
        self.assertEqual(dates_in_string('2000-01-01 00:00:00.00 Z=now'),
                         [(0, 0.0, 'UTC')])
        self.assertEqual(dates_in_string('Today is [[2000-01-01 00:00:00.00 TDB]]'),
                         [(0, 0.0, 'TDB')])
        self.assertEqual(dates_in_string('Today is [[200z-01-01 0z:00:0z.00 TDB]]'),
                         [])

        # Real-world test
        test_path = 'test_files/cpck15Dec2017.tpc'
        with open(test_path, 'r') as f:
            strings = f.readlines()
        f.close()

        PCK_ANSWER = [(6571, 61767, '2017-12-28T17:09:27'),
                      (6558, 0, '2017-DEC-15'),
                      (6558, 0, '2017-Dec-15'),
                      (6513, 0, '2017-Oct-31'),
                      (6512, 0, '2017-Oct-30'),
                      (6503, 0, '2017-Oct-21'),
                      (6435, 0, '2017-Aug-14'),
                      (6415, 0, '2017-Jul-25'),
                      (6338, 0, '2017-May-09'),
                      (6295, 0, '2017-Mar-27'),
                      (6288, 0, '2017-Mar-20'),
                      (6269, 0, '2017-Mar-01'),
                      (6268, 0, '2017-Feb-28'),
                      (6193, 0, '2016-Dec-15'),
                      (6190, 0, '2016-Dec-12'),
                      (6165, 0, '2016-Nov-17'),
                      (6082, 0, '2016-Aug-26'),
                      (6045, 0, '2016-Jul-20'),
                      (6003, 0, '2016-Jun-08'),
                      (5984, 0, '2016-May-20'),
                      (5947, 0, '2016-Apr-13'),
                      (5933, 0, '2016-Mar-30'),
                      (5927, 0, '2016-Mar-24'),
                      (5872, 0, '2016-Jan-29'),
                      (5798, 0, '2015-Nov-16'),
                      (5795, 0, '2015-Nov-13'),
                      (5784, 0, '2015-Nov-02'),
                      (5765, 0, '2015-Oct-14'),
                      (5764, 0, '2015-Oct-13'),
                      (5763, 0, '2015-Oct-12'),
                      (5718, 0, '2015-Aug-28'),
                      (5693, 0, '2015-Aug-03'),
                      (5639, 0, '2015-Jun-10'),
                      (5541, 0, '2015-Mar-04'),
                      (5500, 0, '2015-Jan-22'),
                      (5486, 0, '2015-Jan-08'),
                      (5429, 0, '2014-Nov-12'),
                      (5365, 0, '2014-Sep-09'),
                      (5364, 0, '2014-Sep-08'),
                      (5324, 0, '2014-Jul-30'),
                      (5219, 0, '2014-Apr-16'),
                      (5057, 0, '2013-Nov-05'),
                      (5045, 0, '2013-Oct-24'),
                      (4967, 0, '2013-Aug-07'),
                      (4966, 0, '2013-Aug-06'),
                      (4939, 0, '2013-Jul-10'),
                      (4855, 0, '2013-Apr-17'),
                      (4828, 0, '2013-Mar-21'),
                      (4826, 0, '2013-Mar-19'),
                      (4825, 0, '2013-Mar-18'),
                      (4758, 0, '2013-Jan-10'),
                      (4724, 0, '2012-Dec-07'),
                      (4718, 0, '2012-Dec-01'),
                      (4625, 0, '2012-Aug-30'),
                      (4563, 0, '2012-Jun-29'),
                      (4526, 0, '2012-May-23'),
                      (4499, 0, '2012-Apr-26'),
                      (4491, 0, '2012-Apr-18'),
                      (4441, 0, '2012-Feb-28'),
                      (4401, 0, '2012-Jan-19'),
                      (4399, 0, '2012-Jan-17'),
                      (4304, 0, '2011-Oct-14'),
                      (4300, 0, '2011-Oct-10'),
                      (4239, 0, '2011-Aug-10'),
                      (4157, 0, '2011-May-20'),
                      (4052, 0, '2011-Feb-04'),
                      (4036, 0, '2011-Jan-19'),
                      (4003, 0, '2010-Dec-17'),
                      (3939, 0, '2010-Oct-14'),
                      (3908, 0, '2010-Sep-13'),
                      (3860, 0, '2010-Jul-27'),
                      (3839, 0, '2010-Jul-06'),
                      (3828, 0, '2010-Jun-25'),
                      (3819, 0, '2010-Jun-16'),
                      (3762, 0, '2010-Apr-20'),
                      (3736, 0, '2010-Mar-25'),
                      (3693, 0, '2010-Feb-10'),
                      (3666, 0, '2010-Jan-14'),
                      (3665, 0, '2010-Jan-13'),
                      (3659, 0, '2010-Jan-07'),
                      (3630, 0, '2009-Dec-09'),
                      (3609, 0, '2009-Nov-18'),
                      (3567, 0, '2009-Oct-07'),
                      (3554, 0, '2009-Sep-24'),
                      (3552, 0, '2009-Sep-22'),
                      (3516, 0, '2009-Aug-17'),
                      (3505, 0, '2009-Aug-06'),
                      (3476, 0, '2009-Jul-08'),
                      (3469, 0, '2009-Jul-01'),
                      (3462, 0, '2009-Jun-24'),
                      (3449, 0, '2009-Jun-11'),
                      (3428, 0, '2009-May-21'),
                      (3414, 0, '2009-May-07'),
                      (3400, 0, '2009-Apr-23'),
                      (3344, 0, '2009-Feb-26'),
                      (3320, 0, '2009-Feb-02'),
                      (3307, 0, '2009-Jan-20'),
                      (3273, 0, '2008-Dec-17'),
                      (3259, 0, '2008-Dec-03'),
                      (3226, 0, '2008-Oct-31'),
                      (3181, 0, '2008-Sep-16'),
                      (3170, 0, '2008-Sep-05'),
                      (3091, 0, '2008-Jun-18'),
                      (3079, 0, '2008-Jun-06'),
                      (3057, 0, '2008-May-15'),
                      (3044, 0, '2008-May-02'),
                      (3009, 0, '2008-Mar-28'),
                      (2991, 0, '2008-Mar-10'),
                      (2946, 0, '2008-Jan-25'),
                      (2943, 0, '2008-Jan-22'),
                      (2887, 0, '2007-Nov-27'),
                      (2847, 0, '2007-Oct-18'),
                      (2791, 0, '2007 August 23'),
                      (2767, 0, '2007 July 30'),
                      (2746, 0, '2007 July 9'),
                      (2732, 0, '2007 June 25'),
                      (2732, 0, '2007-JUN-25'),
                      (2713, 0, '2007 June 06'),
                      (2693, 0, '2007 May 17'),
                      (2684, 0, '2007 May 8'),
                      (2677, 0, '2007 May 1'),
                      (2651, 0, '2007 Apr. 5'),
                      (2627, 0, '2007 Mar. 12'),
                      (2601, 0, '2007 Feb. 14'),
                      (2597, 0, '2007 Feb. 10'),
                      (2582, 0, '2007 Jan. 26'),
                      (2582, 0, '2007 Jan. 26'),
                      (2573, 0, '2007 Jan. 17'),
                      (2566, 0, '2007 Jan. 10'),
                      (2539, 0, '2006 Dec. 14'),
                      (2526, 0, '2006 Dec. 01'),
                      (2511, 0, '2006 Nov. 16'),
                      (2503, 0, '2006 Nov. 08'),
                      (2480, 0, '2006 Oct. 16'),
                      (2460, 0, '2006 Sep. 26'),
                      (2441, 0, '2006 Sep. 07'),
                      (2414, 0, '2006 AUG 11'),
                      (2392, 0, '2006 July 20'),
                      (2356, 0, '2006 June 14'),
                      (2326, 0, '2006 MAY 15'),
                      (2299, 0, '2006 Apr 18'),
                      (2271, 0, '2006 Mar 21'),
                      (2265, 0, '2006 Mar 15'),
                      (2236, 0, '2006 Feb 14'),
                      (1201, 0, '16-Apr-2003'),
                      (2203, 0, '2006 Jan 12'),
                      (2173, 0, '2005 Dec 13'),
                      (2145, 0, '2005 Nov 15'),
                      (2120, 0, '2005 Oct 21'),
                      (2110, 0, '2005 Oct 11'),
                      (2092, 0, '2005 Sep 23'),
                      (2077, 0, '2005 Sep 08'),
                      (2064, 0, '2005 Aug 26'),
                      (2040, 0, '2005 Aug 02'),
                      (2018, 0, '2005 Jul 11'),
                      (2012, 0, '2005 Jul 05'),
                      (1986, 0, '2005 Jun 09'),
                      (1965, 0, '2005 May 19'),
                      (1951, 0, '2005 May 05'),
                      (1945, 0, '2005 Apr 29'),
                      (1937, 0, '2005 Apr 21'),
                      (1928, 0, '2005 Apr 12'),
                      (1886, 0, '2005 Mar 01'),
                      (1885, 0, '2005 Feb 28'),
                      (1836, 0, '2005 Jan 10'),
                      (1804, 0, '2004 Dec 9'),
                      (1836, 0, '2005 Jan 10'),
                      (1804, 0, '2004 Dec 9'),
                      (1733, 0, '2004 Sep 29'),
                      (1633, 0, '2004 Jun 21'),
                      (1628, 0, '16 June 2004'),
                      (1586, 0, '2004 May 05'),
                      (3897, 0, '2010-SEP-02'),
                      (3897, 0, '2010 Sep 02'),
                      (3028, 0, '2008 Apr 16'),
                      (1804, 0, '2004 Dec 09'),
                      (1748, 0, '2004 Oct 14'),
                      (1633, 0, '2004 Jun 21'),
                      (1628, 0, '16 June 2004'),
                      (1525, 0, '2004 Mar 05'),
                      (1490, 0, '1/30/2004'),
                      (1496, 0, '2/5/2004'),
                      (1424, 58961, 'Tue, 25 Nov 2003 16:22:41'),
                      (1004, 0, '2002 Oct 01'),
                      (0, 0, '1/1/2000'),
                      (-1437, 0, '25 January 1996'),
                      (-80, 0, '13 Oct 1999'),
                      (1490, 0, '1/30/2004'),
                      (1496, 0, '2/5/2004'),
                      (1628, 0, '16 June 2004'),
                      (1726, 0, '2004 September 22')]

        self.assertEqual(day_sec_in_strings(strings, substrings=True, weekdays=True),
                         PCK_ANSWER)

        # Check fractional day
        test = day_sec_from_string('2000-01-31.25', floating=True)
        self.assertEqual(test, (30, 21600.))
        self.assertIs(type(test[1]), float)

##########################################################################################
