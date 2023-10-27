##########################################################################################
# julian/test_date_parser.py
##########################################################################################

import numpy as np
import pathlib
import sys
import unittest

from julian.date_parser import (
    day_from_string,
    day_in_string,
    days_in_string,
    days_in_strings,
    _date_pattern_filter,
)

from julian.calendar    import day_from_yd, day_from_ymd
from julian.utc_tai_tdb import day_sec_from_tai, tai_from_tdt

class Test_date_parser(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian.warning import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # Note: test_date_pyparser.py has more extensive unit tests

        # _date_pattern_filter
        self.assertFalse(_date_pattern_filter('abcdefg1 2'))
        self.assertFalse(_date_pattern_filter('abcdefg3000'))
        self.assertFalse(_date_pattern_filter('abcdefgwedhijk'))

        self.assertTrue(_date_pattern_filter('abcdefg wedhijkl'))
        self.assertTrue(_date_pattern_filter('abcdefg jANhijkl'))
        self.assertTrue(_date_pattern_filter('abcdefg1 2 3 4 56hijkl'))
        self.assertTrue(_date_pattern_filter('abcdefg1 2 3456hijkl'))
        self.assertTrue(_date_pattern_filter('abcdefg1000hijkl'))

        self.assertTrue(_date_pattern_filter( 'abcdefg3000 399hijkl', doy=True))
        self.assertFalse(_date_pattern_filter('abcdefg3000 399hijkl', doy=False))
        self.assertFalse(_date_pattern_filter('abcdefg3000 400hijkl', doy=False))

        self.assertTrue(_date_pattern_filter( 'abcdefg MJTd hijkl', mjd=True))
        self.assertFalse(_date_pattern_filter('abcdefg Jed hijkl', mjd=False))
        self.assertFalse(_date_pattern_filter('abcdefgJd hijkl',  mjd=True))
        self.assertFalse(_date_pattern_filter('abcdefg mJdhijkl', mjd=True))

        # Check if day_from_string works like day_from_ymd
        self.assertEqual(day_from_string('2000-01-01'),
                         day_from_ymd(2000,1,1))

        # Check day_from_string
        self.assertEqual(day_from_string('01-02-2000', order='MDY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_from_string('01-02-00', order='MDY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_from_string('02-01-2000', order='DMY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_from_string('02-01-00', order='DMY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_from_string('2000-02-29', order='DMY'),
                         day_from_ymd(2000,2,29))

        self.assertEqual(day_from_string('1582-10-01', proleptic=True),   -152398)
        self.assertEqual(day_from_string('1582-10-01', use_julian=False), -152398)
        self.assertEqual(day_from_string('1582-10-01', proleptic=False),  -152388)
        self.assertEqual(day_from_string('1582-10-01', use_julian=True),  -152388)

        self.assertRaises(ValueError, day_from_string, 'whatever')

        # Check date validator, weekdays
        self.assertRaises(ValueError, day_from_string, '2001-11-31', validate=True)
        self.assertRaises(ValueError, day_from_string, '2001-02-29', validate=True)
        self.assertRaises(ValueError, day_from_string, '2001-02-ab')

        self.assertEqual(day_from_string('Monday, 2000-01-01', weekdays=True,
                                         validate=False), 0)
        self.assertRaises(ValueError, day_from_string, 'Monday, 2000-01-01',
                                      weekdays=True, validate=True)    # it was a Saturday
        self.assertRaises(ValueError, day_from_string, 'Monday, 2000-001',
                                      weekdays=True, validate=True)

        # Check day_in_string
        self.assertEqual(day_in_string('Today is 01-02-2000!', order='MDY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_in_string('Today is:[01-02-00]', order='MDY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_in_string('Is this today?02-01-2000-0', order='DMY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_in_string('Test--02-01-00-00', order='DMY'),
                         day_from_ymd(2000,1,2))
        self.assertEqual(day_in_string('Test 2000-02-29=today', order='DMY'),
                         day_from_ymd(2000,2,29))
        self.assertEqual(day_in_string('Using DOY is 2020-366'),
                         day_from_ymd(2020,12,31))
        self.assertEqual(day_in_string('Using DOY is 2020-367'), None)

        # Check days_in_string
        self.assertEqual(days_in_string('Today is 01-02-2000!', order='MDY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_string('Today is:[01-02-00]', order='MDY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_string('Is this today?02-01-2000-0', order='DMY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_string('Test--02-01-00-00', order='DMY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_string('Test 2000-02-29=today', order='DMY'),
                         [day_from_ymd(2000,2,29)])
        self.assertEqual(days_in_string('Test 2000=today', order='DMY'),
                         [])
        self.assertEqual(days_in_string('2020-01-01|30-10-20, etc.'),
                         [day_from_ymd(2020,1,1), day_from_ymd(2030,10,20)])

        # Check days_in_strings
        self.assertEqual(days_in_strings('Today is 2000-01-02!'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings(['Today is 2000-01-02!', 'Not 2000-13-02']),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings('Today is 01-02-2000!', order='MDY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings(['Today is 01-02-2000!', 'I think'], order='MDY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings(['Maybe', 'Today is:[01-02-00]'], order='MDY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', 'Or tomorrow?'],
                                         order='DMY'),
                         [day_from_ymd(2000,1,2)])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', '2000-01-03!'],
                                         order='DMY'),
                         [day_from_ymd(2000,1,2), day_from_ymd(2000,1,3)])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', '2000-01-03!'],
                                         order='DMY', first=True),
                         day_from_ymd(2000,1,2))
        self.assertEqual(days_in_strings(['Is this today?02-01-xxx0-0', '2000-xx-03!'],
                                         order='DMY', first=True),
                         None)
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', '2000-01-03!'],
                                         order='DMY', substrings=True),
                         [(day_from_ymd(2000,1,2), '02-01-2000'),
                          (day_from_ymd(2000,1,3), '2000-01-03')])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', '2000-01-03!'],
                                         order='DMY', substrings=True, first=True),
                         (day_from_ymd(2000,1,2), '02-01-2000'))
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', ' MJD 51544.5'],
                                         order='DMY', mjd=False, substrings=True),
                         [(day_from_ymd(2000,1,2), '02-01-2000')])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', ' MJD 51544.5'],
                                         order='DMY', mjd=True, substrings=True),
                         [(day_from_ymd(2000,1,2), '02-01-2000'),
                          (day_from_ymd(2000,1,1), 'MJD 51544')])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', ' 2001-001'],
                                         order='DMY', mjd=True, doy=True, substrings=True),
                         [(day_from_ymd(2000,1,2), '02-01-2000'),
                          (day_from_yd(2001,1), '2001-001')])
        self.assertEqual(days_in_strings(['Is this today?02-01-2000-0', ' 2000-366'],
                                         order='DMY', mjd=True, doy=True, substrings=True),
                         [(day_from_ymd(2000,1,2), '02-01-2000'),
                          (day_from_yd(2000,366), '2000-366')])
        self.assertEqual(days_in_strings(' 1001-001', doy=True, substrings=True),
                         [(day_from_yd(1001,1), '1001-001')])

        # Check date validator
        self.assertEqual(days_in_strings('Today=(2001-11-31)',
                                         validate=True, first=True), None)
        self.assertEqual(days_in_strings('Today 2001-02-29T12:34:56',
                                         validate=True, first=True), None)
        self.assertEqual(day_in_string('Today 2001-01-01, not tomorrow', remainder=True),
                                       (366, ', not tomorrow'))

        # Real-world test
        julian_root_dir = pathlib.Path(sys.modules['julian'].__file__).parent
        test_path = julian_root_dir / 'test_files' / 'cpck15Dec2017.tpc'
        with test_path.open() as f:
            strings = f.readlines()
        f.close()

        PCK_ANSWER = [(6571, '2017-12-28'),
                      (6558, '2017-DEC-15'),
                      (6558, '2017-Dec-15'),
                      (6513, '2017-Oct-31'),
                      (6512, '2017-Oct-30'),
                      (6503, '2017-Oct-21'),
                      (6435, '2017-Aug-14'),
                      (6415, '2017-Jul-25'),
                      (6338, '2017-May-09'),
                      (6295, '2017-Mar-27'),
                      (6288, '2017-Mar-20'),
                      (6269, '2017-Mar-01'),
                      (6268, '2017-Feb-28'),
                      (6193, '2016-Dec-15'),
                      (6190, '2016-Dec-12'),
                      (6165, '2016-Nov-17'),
                      (6082, '2016-Aug-26'),
                      (6045, '2016-Jul-20'),
                      (6003, '2016-Jun-08'),
                      (5984, '2016-May-20'),
                      (5947, '2016-Apr-13'),
                      (5933, '2016-Mar-30'),
                      (5927, '2016-Mar-24'),
                      (5872, '2016-Jan-29'),
                      (5798, '2015-Nov-16'),
                      (5795, '2015-Nov-13'),
                      (5784, '2015-Nov-02'),
                      (5765, '2015-Oct-14'),
                      (5764, '2015-Oct-13'),
                      (5763, '2015-Oct-12'),
                      (5718, '2015-Aug-28'),
                      (5693, '2015-Aug-03'),
                      (5639, '2015-Jun-10'),
                      (5541, '2015-Mar-04'),
                      (5500, '2015-Jan-22'),
                      (5486, '2015-Jan-08'),
                      (5429, '2014-Nov-12'),
                      (5365, '2014-Sep-09'),
                      (5364, '2014-Sep-08'),
                      (5324, '2014-Jul-30'),
                      (5219, '2014-Apr-16'),
                      (5057, '2013-Nov-05'),
                      (5045, '2013-Oct-24'),
                      (4967, '2013-Aug-07'),
                      (4966, '2013-Aug-06'),
                      (4939, '2013-Jul-10'),
                      (4855, '2013-Apr-17'),
                      (4828, '2013-Mar-21'),
                      (4826, '2013-Mar-19'),
                      (4825, '2013-Mar-18'),
                      (4758, '2013-Jan-10'),
                      (4724, '2012-Dec-07'),
                      (4718, '2012-Dec-01'),
                      (4625, '2012-Aug-30'),
                      (4563, '2012-Jun-29'),
                      (4526, '2012-May-23'),
                      (4499, '2012-Apr-26'),
                      (4491, '2012-Apr-18'),
                      (4441, '2012-Feb-28'),
                      (4401, '2012-Jan-19'),
                      (4399, '2012-Jan-17'),
                      (4304, '2011-Oct-14'),
                      (4300, '2011-Oct-10'),
                      (4239, '2011-Aug-10'),
                      (4157, '2011-May-20'),
                      (4052, '2011-Feb-04'),
                      (4036, '2011-Jan-19'),
                      (4003, '2010-Dec-17'),
                      (3939, '2010-Oct-14'),
                      (3908, '2010-Sep-13'),
                      (3860, '2010-Jul-27'),
                      (3839, '2010-Jul-06'),
                      (3828, '2010-Jun-25'),
                      (3819, '2010-Jun-16'),
                      (3762, '2010-Apr-20'),
                      (3736, '2010-Mar-25'),
                      (3693, '2010-Feb-10'),
                      (3666, '2010-Jan-14'),
                      (3665, '2010-Jan-13'),
                      (3659, '2010-Jan-07'),
                      (3630, '2009-Dec-09'),
                      (3609, '2009-Nov-18'),
                      (3567, '2009-Oct-07'),
                      (3554, '2009-Sep-24'),
                      (3552, '2009-Sep-22'),
                      (3516, '2009-Aug-17'),
                      (3505, '2009-Aug-06'),
                      (3476, '2009-Jul-08'),
                      (3469, '2009-Jul-01'),
                      (3462, '2009-Jun-24'),
                      (3449, '2009-Jun-11'),
                      (3428, '2009-May-21'),
                      (3414, '2009-May-07'),
                      (3400, '2009-Apr-23'),
                      (3344, '2009-Feb-26'),
                      (3320, '2009-Feb-02'),
                      (3307, '2009-Jan-20'),
                      (3273, '2008-Dec-17'),
                      (3259, '2008-Dec-03'),
                      (3226, '2008-Oct-31'),
                      (3181, '2008-Sep-16'),
                      (3170, '2008-Sep-05'),
                      (3091, '2008-Jun-18'),
                      (3079, '2008-Jun-06'),
                      (3057, '2008-May-15'),
                      (3044, '2008-May-02'),
                      (3009, '2008-Mar-28'),
                      (2991, '2008-Mar-10'),
                      (2946, '2008-Jan-25'),
                      (2943, '2008-Jan-22'),
                      (2887, '2007-Nov-27'),
                      (2847, '2007-Oct-18'),
                      (2791, '2007 August 23'),
                      (2767, '2007 July 30'),
                      (2746, '2007 July 9'),
                      (2732, '2007 June 25'),
                      (2732, '2007-JUN-25'),
                      (2713, '2007 June 06'),
                      (2693, '2007 May 17'),
                      (2684, '2007 May 8'),
                      (2677, '2007 May 1'),
                      (2651, '2007 Apr. 5'),
                      (2627, '2007 Mar. 12'),
                      (2601, '2007 Feb. 14'),
                      (2597, '2007 Feb. 10'),
                      (2582, '2007 Jan. 26'),
                      (2582, '2007 Jan. 26'),
                      (2573, '2007 Jan. 17'),
                      (2566, '2007 Jan. 10'),
                      (2539, '2006 Dec. 14'),
                      (2526, '2006 Dec. 01'),
                      (2511, '2006 Nov. 16'),
                      (2503, '2006 Nov. 08'),
                      (2480, '2006 Oct. 16'),
                      (2460, '2006 Sep. 26'),
                      (2441, '2006 Sep. 07'),
                      (2414, '2006 AUG 11'),
                      (2392, '2006 July 20'),
                      (2356, '2006 June 14'),
                      (2326, '2006 MAY 15'),
                      (2299, '2006 Apr 18'),
                      (2271, '2006 Mar 21'),
                      (2265, '2006 Mar 15'),
                      (2236, '2006 Feb 14'),
                      (1201, '16-Apr-2003'),
                      (2203, '2006 Jan 12'),
                      (2173, '2005 Dec 13'),
                      (2145, '2005 Nov 15'),
                      (2120, '2005 Oct 21'),
                      (2110, '2005 Oct 11'),
                      (2092, '2005 Sep 23'),
                      (2077, '2005 Sep 08'),
                      (2064, '2005 Aug 26'),
                      (2040, '2005 Aug 02'),
                      (2018, '2005 Jul 11'),
                      (2012, '2005 Jul 05'),
                      (1986, '2005 Jun 09'),
                      (1965, '2005 May 19'),
                      (1951, '2005 May 05'),
                      (1945, '2005 Apr 29'),
                      (1937, '2005 Apr 21'),
                      (1928, '2005 Apr 12'),
                      (1886, '2005 Mar 01'),
                      (1885, '2005 Feb 28'),
                      (1836, '2005 Jan 10'),
                      (1804, '2004 Dec 9'),
                      (1836, '2005 Jan 10'),
                      (1804, '2004 Dec 9'),
                      (1733, '2004 Sep 29'),
                      (1633, '2004 Jun 21'),
                      (1628, '16 June 2004'),
                      (1586, '2004 May 05'),
                      (3897, '2010-SEP-02'),
                      (3897, '2010 Sep 02'),
                      (3028, '2008 Apr 16'),
                      (1804, '2004 Dec 09'),
                      (1748, '2004 Oct 14'),
                      (1633, '2004 Jun 21'),
                      (1628, '16 June 2004'),
                      (1525, '2004 Mar 05'),
                      (1490, '1/30/2004'),
                      (1496, '2/5/2004'),
                      (1424, '25 Nov 2003'),
                      (1004, '2002 Oct 01'),
                      (0, '1/1/2000'),
                      (-1437, '25 January 1996'),
                      (-80, '13 Oct 1999'),
                      (1490, '1/30/2004'),
                      (1496, '2/5/2004'),
                      (1628, '16 June 2004'),
                      (1726, '2004 September 22')]

        self.assertEqual(days_in_strings(strings, substrings=True), PCK_ANSWER)

########################################
# Executed from the command line
########################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
