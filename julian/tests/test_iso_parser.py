##########################################################################################
# julian/test_iso_parser.py
##########################################################################################
import numpy as np
import unittest

from julian.iso_parser import (
    day_from_iso,
    day_sec_from_iso,
    sec_from_iso,
    tai_from_iso,
    tdb_from_iso,
    time_from_iso,
)

from julian.utc_tai_tdb import tai_from_day_sec, tdb_from_tai, tt_from_tai


class Test_iso_parser(unittest.TestCase):

    def test_day_from_iso(self):

        import warnings
        from julian.warning import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # YYYY-MM-DD
        for x in ('-', ''):
            self.assertEqual(day_from_iso(f'2001{x}01{x}01'), 366)
            self.assertEqual(day_from_iso(f'2001{x}01{x}01.5'), 366.5)
            self.assertEqual(day_from_iso(f'  2001{x}01{x}01', strip=True), 366)
            self.assertEqual(day_from_iso(f'  2001{x}01{x}01.5', strip=True), 366.5)
            self.assertRaises(ValueError, day_from_iso, '  2001{x}01{x}01')

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}01{x}01']
            days    = [            -365 ,                0 ,              366 ]
            self.assertTrue(np.all(day_from_iso(strings) == days))

            strings = [f'  1999{x}01{x}01', f'  2000{x}01{x}01', f'  2001{x}01{x}01']
            self.assertTrue(np.all(day_from_iso(strings, strip=True) == days))
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01  ', f'2000{x}01{x}01  ', f'2001{x}01{x}01  ']
            self.assertTrue(np.all(day_from_iso(strings, strip=True) == days))
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01  ', f'  2000{x}01{x}01', f' 2001{x}01{x}01 ']
            self.assertRaises(ValueError, day_from_iso, strings, strip=False)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', '2001{x}01{x}aa']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}aa', f'2000{x}01{x}01', f'2001{x}01{x}01']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}01{x} 1']
            self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}01{x}00']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}00{x}01']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}13{x}01']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [f'1999{x}01{x}01', f'2000{x}01{x}01', f'2001{x}02{x}29']
            self.assertRaises(ValueError, day_from_iso, strings)

            strings = [[f' 2000{x}01{x}01', f' 2000{x}01{x}02'],
                       [f' 2000{x}01{x}03', f'x2000{x}01{x}04']]
            days    = [[                0 ,                 1 ],
                       [                2 ,                 3 ]]
            self.assertTrue(np.all(day_from_iso(strings, strip=True, syntax=False) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=True, syntax=True)

            strings = [[f'2000{x}01{x}01 ', f'2000{x}01{x}02 '],
                       [f'2000{x}01{x}03 ', f'2000{x}01{x}04x']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True, syntax=False) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=True, syntax=True)

            self.assertRaises(ValueError, day_from_iso, f'2000{x}02{x}30', validate=True)
            self.assertRaises(ValueError, day_from_iso, f'2001{x}02{x}29', validate=True)

        strings = ['1999-01-01', '2000-01-01', '2001-01+01']
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        strings = ['1999-01-01', '2000+01-01', '2001-01-01']
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        strings = ['1999-01-01', '2000-01-01', ' 2001-01 01']
        self.assertRaises(ValueError, day_from_iso, strings, validate=True)

        strings = ['1999-01-01', '2000-01-01', ' 2001-01--1']
        self.assertRaises(ValueError, day_from_iso, strings, validate=True)

        strings = [b'2000-01-01\0', b'2001-01-01\0']
        self.assertTrue(np.all(day_from_iso(strings, syntax=True) == [0, 366]))

        strings = [b'2000-01-01\0', b'2001-01-01x']
        self.assertTrue(np.all(day_from_iso(strings, syntax=False) == [0, 366]))
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        strings = [b'20000101\0', b'20010101\0']
        self.assertTrue(np.all(day_from_iso(strings, syntax=True) == [0, 366]))

        strings = [b'20000101\0', b'20010101x']
        self.assertTrue(np.all(day_from_iso(strings, syntax=False) == [0, 366]))
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        # YYYY-DDD
        for x in ('-', ''):
            strings = [[f'2000{x}001', f'2000{x}002'], [f'2000{x}003', f'2000{x}004']]
            days    = [[           0 ,            1 ], [           2 ,            3 ]]
            self.assertTrue(np.all(day_from_iso(strings) == days))

            strings = [[f' 2000{x}001', f' 2000{x}002'], [f' 2000{x}003', f' 2000{x}004']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=False)

            strings = [[f'2000{x}001 ', f'2000{x}002 '],
                       [f'2000{x}003 ', f'2000{x}004 ']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=False)

            strings = [[f' 2000{x}001 ', f' 2000{x}002 '],
                       [f' 2000{x}003 ', f' 2000{x}004 ']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=False)

            strings = [[f' 2000{x}001', f' 2000{x}002'],
                       [f' 2000{x}003', f'x2000{x}004']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True, syntax=False) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=True, syntax=True)

            strings = [[f'2000{x}001 ', f'2000{x}002 '],
                       [f'2000{x}003 ', f'2000{x}004x']]
            self.assertTrue(np.all(day_from_iso(strings, strip=True, syntax=False) == days))
            self.assertRaises(ValueError, day_from_iso, strings, strip=True, syntax=True)

            self.assertRaises(ValueError, day_from_iso, f'2000{x}000', validate=True)
            self.assertRaises(ValueError, day_from_iso, f'2000{x}367', validate=True)

        self.assertRaises(ValueError, day_from_iso, '2000+001', syntax=True)

        strings = [b'2000-001\0', b'2001-001\0']
        self.assertTrue(np.all(day_from_iso(strings, syntax=True) == [0, 366]))

        strings = [b'2000-001\0', b'2001-001x']
        self.assertTrue(np.all(day_from_iso(strings, syntax=False) == [0, 366]))
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        strings = [b'2000001\0', b'2001001\0']
        self.assertTrue(np.all(day_from_iso(strings, syntax=True) == [0, 366]))

        strings = [b'2000001\0', b'2001001x']
        self.assertTrue(np.all(day_from_iso(strings, syntax=False) == [0, 366]))
        self.assertRaises(ValueError, day_from_iso, strings, syntax=True)

        self.assertRaises(ValueError, day_from_iso, ['2010-01-01', '2010-01- 1'],
                                                    syntax=True)
        self.assertRaises(ValueError, day_from_iso, ['20100201', '201002-1'],
                                                    syntax=True)

        self.assertEqual(day_from_iso('1500-01-01', proleptic=True),   -182621)
        self.assertEqual(day_from_iso('1500-01-01', use_julian=False), -182621)
        self.assertEqual(day_from_iso('1500-01-01', proleptic=False),  -182612)
        self.assertEqual(day_from_iso('1500-01-01', use_julian=True),  -182612)


    def test_sec_from_iso(self):

        for c in (':', ''):
            self.assertEqual(sec_from_iso(f'01{c}00{c}00'),     3600)
            self.assertEqual(sec_from_iso(f'23{c}59{c}60'),    86400)
            self.assertEqual(sec_from_iso(f'23{c}59{c}69'),    86409)
            self.assertEqual(sec_from_iso(f'23{c}59{c}69Z'),   86409)
            self.assertEqual(sec_from_iso(f'23{c}59{c}69.10'), 86409.10)
            self.assertEqual(sec_from_iso(f'23{c}59{c}69.5Z'), 86409.5)
            self.assertEqual(sec_from_iso(f'12{c}00'),         43200)
            self.assertEqual(sec_from_iso(f'12{c}01.5'),       43290)

            strings = [f'00{c}00{c}00', f'00{c}01{c}00', f'00{c}02{c}00']
            secs    = [             0 ,             60 ,            120 ]
            self.assertTrue(np.all(sec_from_iso(strings) == secs))

            strings = [f' 00{c}00{c}00', f' 00{c}01{c}00', f' 00{c}02{c}00']
            self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
            self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

            strings = [f' 00{c}00{c}00  ', f' 00{c}01{c}00  ', f' 00{c}02{c}00  ']
            self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
            self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

            strings = [f'00{c}00{c}00    ', f'00{c}01{c}00    ', f'00{c}02{c}00    ']
            self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
            self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

            strings = [f'00{c}00{c}00    ', f'00{c}01{c}00    ', f'00{c}02{c}00   x']
            self.assertTrue(np.all(sec_from_iso(strings, strip=True, validate=False) == secs))
            self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

            strings = [f' 00{c}00{c}00', f' 00{c}01{c}00', f'x00{c}02{c}00']
            self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

            strings = [[f'00{c}02{c}00Z', f'00{c}04{c}00Z'],
                       [f'00{c}06{c}00Z', f'00{c}08{c}01Z']]
            secs    = [[           120  ,            240  ],
                       [            360 ,             481 ]]
            self.assertTrue(np.all(sec_from_iso(strings) == secs))

            strings = [[f'00{c}02{c}00Z', f'00{c}04{c}00Z'],
                      [f'00{c}06{c}00Z', f'00{c}08{c}01 ']]
            secs    = [[           120  ,            240  ],
                      [            360 ,             481 ]]
            self.assertTrue(np.all(sec_from_iso(strings, validate=False) == secs))
            self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'23{c}59{c}69.03']
            secs    = [             0.01 ,             60.02 ,          86409.03 ]
            self.assertTrue(np.all(sec_from_iso(strings) == secs))

            self.assertEqual(sec_from_iso(f'00{c}00{c}69', validate=False), 69)
            self.assertRaises(ValueError, sec_from_iso, f'00{c}00{c}69', validate=True)
            self.assertRaises(ValueError, sec_from_iso, f'24{c}00{c}00', validate=True)
            self.assertRaises(ValueError, sec_from_iso, f'00{c}60{c}00', validate=True)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'00{c}02{c} 0.03']
            self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

            strings = [f'00{c}02{c}00.1Z', f'00{c}04{c}00.2Z', f'00{c}06{c}00.3z']
            self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'-0{c}02{c}00.03']
            self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'24{c}02{c}00.03']
            self.assertRaises(ValueError, sec_from_iso, strings)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'00{c}60{c}00.03']
            self.assertRaises(ValueError, sec_from_iso, strings)

            strings = [f'00{c}00{c}00', f'00{c}01{c}00', f'00{c}00{c}70']
            self.assertRaises(ValueError, sec_from_iso, strings)

            strings = [f'00{c}00{c}00.01', f'00{c}01{c}00.02', f'00{c}00{c}69.00']
            self.assertRaises(ValueError, sec_from_iso, strings)

        strings = ['00:00:00.01', '00:01:00.02', '00:02+00.03']
        self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

        strings = ['00:00:00.01', '00:01:00.02', '00:02:00+03']
        self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

        self.assertEqual(sec_from_iso('12.5'), 43200 + 1800)

        # bytes, colons
        self.assertEqual(sec_from_iso(b'01:00:00'),     3600)
        self.assertEqual(sec_from_iso(b'23:59:60'),    86400)
        self.assertEqual(sec_from_iso(b'23:59:69'),    86409)
        self.assertEqual(sec_from_iso(b'23:59:69Z'),   86409)
        self.assertEqual(sec_from_iso(b'23:59:69.10'), 86409.10)
        self.assertEqual(sec_from_iso(b'23:59:69.5Z'), 86409.5)
        self.assertEqual(sec_from_iso(b'12:00'),         43200)
        self.assertEqual(sec_from_iso(b'12:01.5'),       43290)

        strings = [b'00:00:00', b'00:01:00', b'00:02:00']
        secs    = [         0 ,         60 ,        120 ]
        self.assertTrue(np.all(sec_from_iso(strings) == secs))

        strings = [b' 00:00:00', b' 00:01:00', b' 00:02:00']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b' 00:00:00  ', b' 00:01:00  ', b' 00:02:00  ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'00:00:00    ', b'00:01:00    ', b'00:02:00    ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'00:00:00    ', b'00:01:00    ', b'00:02:00   x']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True, validate=False) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 00:00:00', b' 00:01:00', b'x00:02:00']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b'00:00:00', b'00:01:00', b'00:02:00']
        secs    = [         0 ,         60 ,        120 ]
        self.assertTrue(np.all(sec_from_iso(strings) == secs))

        strings = [b' 00:00:00', b' 00:01:00', b' 00:02:00']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b' 00:00:00  ', b' 00:01:00  ', b' 00:02:00  ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'00:00:00    ', b'00:01:00    ', b'00:02:00    ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'00:00:00    ', b'00:01:00    ', b'00:02:00   x']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True, validate=False) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 00:00:00', b' 00:01:00', b'x00:02:00']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 00:00:00', b' 00:01:00', b' 00:02-00']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 00:00:00', b' 00-01:00', b' 00:02:00']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        # bytes, no colons
        self.assertEqual(sec_from_iso(b'010000'),     3600)
        self.assertEqual(sec_from_iso(b'235960'),    86400)
        self.assertEqual(sec_from_iso(b'235969'),    86409)
        self.assertEqual(sec_from_iso(b'235969Z'),   86409)
        self.assertEqual(sec_from_iso(b'235969.10'), 86409.10)
        self.assertEqual(sec_from_iso(b'235969.5Z'), 86409.5)
        self.assertEqual(sec_from_iso(b'1200'),         43200)
        self.assertEqual(sec_from_iso(b'1201.5'),       43290)

        strings = [b'000000', b'000100', b'000200']
        secs    = [       0 ,       60 ,      120 ]
        self.assertTrue(np.all(sec_from_iso(strings) == secs))

        strings = [b' 000000', b' 000100', b' 000200']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b' 000000  ', b' 000100  ', b' 000200  ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'000000    ', b'000100    ', b'000200    ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'000000    ', b'000100    ', b'000200   x']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True, validate=False) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 000000', b' 000100', b'x000200']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b'000000', b'000100', b'000200']
        secs    = [       0 ,       60 ,      120 ]
        self.assertTrue(np.all(sec_from_iso(strings) == secs))

        strings = [b' 000000', b' 000100', b' 000200']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b' 000000  ', b' 000100  ', b' 000200  ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'000000    ', b'000100    ', b'000200    ']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        strings = [b'000000    ', b'000100    ', b'000200   x']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True, validate=False) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        strings = [b' 000000', b' 000100', b'x000200']
        self.assertRaises(ValueError, sec_from_iso, strings, strip=True, syntax=True)

        # bytes, no colons, with nulls
        self.assertEqual(sec_from_iso(b'010000\0'),     3600)
        self.assertEqual(sec_from_iso(b'235960\0'),    86400)
        self.assertEqual(sec_from_iso(b'235969\0'),    86409)
        self.assertEqual(sec_from_iso(b'235969Z\0'),   86409)
        self.assertEqual(sec_from_iso(b'235969.10\0'), 86409.10)
        self.assertEqual(sec_from_iso(b'235969.5Z\0'), 86409.5)
        self.assertEqual(sec_from_iso(b'1200\0'),      43200)
        self.assertEqual(sec_from_iso(b'1201.5\0'),    43290)

        strings = [b'000000\0', b'000100\0', b'000200\0']
        secs    = [         0 ,         60 ,        120 ]
        self.assertTrue(np.all(sec_from_iso(strings, syntax=False) == secs))
        self.assertTrue(np.all(sec_from_iso(strings, syntax=True) == secs))

        strings = [b'000000\0', b'000100\0', b'000200q']
        secs    = [         0 ,         60 ,       120 ]
        self.assertTrue(np.all(sec_from_iso(strings, syntax=False) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, syntax=True)

        strings = [b' 000000\0', b' 000100\0', b' 000200\0']
        self.assertTrue(np.all(sec_from_iso(strings, strip=True) == secs))
        self.assertRaises(ValueError, sec_from_iso, strings, strip=False)

        # Errors
        self.assertRaises(ValueError, sec_from_iso, '12:34:56:78')
        self.assertRaises(ValueError, sec_from_iso, '12:34.:56.78')
        self.assertRaises(ValueError, sec_from_iso, '12:34.:56')
        self.assertRaises(ValueError, sec_from_iso, '12:34:5.6')
        self.assertRaises(ValueError, sec_from_iso, '12345.6')
        self.assertRaises(ValueError, sec_from_iso, '12:3.:56')
        self.assertRaises(ValueError, sec_from_iso, ['12:34:56:78 ', '12:34:56:78'])
        self.assertRaises(ValueError, sec_from_iso, ['12:34.:56.78', '12:34.:56.78'])
        self.assertRaises(ValueError, sec_from_iso, ['12:34.:56'   , '12:34.:56'])
        self.assertRaises(ValueError, sec_from_iso, ['12:34:5.6'   , '12:34:5.6'])


    def test_day_sec_from_iso(self):

        import warnings
        from julian.warning import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        self.assertEqual(day_sec_from_iso('2001-01-01'), (366, 0))
        self.assertEqual(day_sec_from_iso('2001-01-01  ', strip=True), (366, 0))
        self.assertEqual(day_sec_from_iso(' 2001-01-01 ', strip=True), (366, 0))
        self.assertEqual(day_sec_from_iso('2001-01-01 01:00:00'), (366, 3600))
        self.assertEqual(day_sec_from_iso('2001-01-01T01:00:00'), (366, 3600))
        self.assertEqual(day_sec_from_iso('1998-12-31 23:59:60'), (-366, 86400))
        self.assertEqual(day_sec_from_iso('  1998-12-31 23:59:60 ', strip=True),
                         (-366, 86400))

        self.assertRaises(ValueError, day_sec_from_iso, '2000-01-01 23:59:60')
        self.assertRaises(ValueError, day_sec_from_iso, '1999-12-31 23:59:61')

        strings = ['1999-01-01', '2000-01-01', '2001-01-01']
        days    = [       -365 ,           0 ,         366 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == 0))

        strings = [['2000-001', '2000-002'], ['2000-003', '2000-004']]
        days    = [[        0 ,         1 ], [        2 ,         3 ]]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == 0))

        strings = ['1998-12-31 23:59:60', '2001-01-01 01:00:01']
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == secs))

        strings = ['1998-12-31T23:59:60', '2001-01-01T01:00:01']
        days    = [       -366          ,         366          ]
        secs    = [               86400 ,                 3601 ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == secs))

        strings = ['1998-12-31 23:59:60Z', '2001-01-01 01:00:01Z']
        days    = [       -366           ,         366           ]
        secs    = [               86400  ,                 3601  ]
        self.assertTrue(np.all(day_sec_from_iso(strings)[0] == days))
        self.assertTrue(np.all(day_sec_from_iso(strings)[1] == secs))

        strings = ['1998-12-31 23:59:60Z', '2001-01-01x01:00:01Z']
        self.assertRaises(ValueError, day_sec_from_iso, strings, syntax=True)

        strings = ['1998-12-31 23:59:60Z', '1998-12-31 23:59:61Z']
        self.assertRaises(ValueError, day_sec_from_iso, strings)

        self.assertEqual(day_sec_from_iso('1500-01-01T12:00:00', proleptic=True),
                         (-182621, 43200))
        self.assertEqual(day_sec_from_iso('1500-01-01T12:00:00', use_julian=False),
                         (-182621, 43200))
        self.assertEqual(day_sec_from_iso('1500-01-01T12:00:00', proleptic=False),
                         (-182612, 43200))
        self.assertEqual(day_sec_from_iso('1500-01-01T12:00:00', use_julian=True),
                         (-182612, 43200))

    def test_time_from_iso(self):

        self.assertEqual(tai_from_iso( '2001-01-01 01:00:00'),
                         tai_from_day_sec(366, 3600))
        self.assertEqual(tai_from_iso( '2001-01-01T01:00:00'),
                         tai_from_day_sec(366, 3600))
        self.assertEqual(tai_from_iso('1998-12-31 23:59:60'),
                         tai_from_day_sec(-366, 86400))
        self.assertEqual(tai_from_iso('  1998-12-31 23:59:60 ', strip=True),
                         tai_from_day_sec(-366, 86400))

        pro_tai = tai_from_iso('1500-12-31 00:00:00', proleptic=True)
        jul_tai = tai_from_iso('1500-12-31 00:00:00', proleptic=False)
        self.assertEqual(pro_tai, -15747047990)
        self.assertEqual(jul_tai, -15746183990)
        self.assertEqual(pro_tai, tai_from_iso('1500-12-31 00:00:00', use_julian=False))
        self.assertEqual(jul_tai, tai_from_iso('1500-12-31 00:00:00', use_julian=True))

        self.assertEqual(tdb_from_iso( '2001-01-01 01:00:00'),
                         tdb_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(tdb_from_iso( '2001-01-01T01:00:00'),
                         tdb_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(tdb_from_iso('1998-12-31 23:59:60'),
                         tdb_from_tai(tai_from_day_sec(-366, 86400)))
        self.assertEqual(tdb_from_iso('  1998-12-31 23:59:60 ', strip=True),
                         tdb_from_tai(tai_from_day_sec(-366, 86400)))

        self.assertEqual(time_from_iso( '2001-01-01 01:00:00'),
                         tai_from_day_sec(366, 3600))
        self.assertEqual(time_from_iso( '2001-01-01T01:00:00'),
                         tai_from_day_sec(366, 3600))
        self.assertEqual(time_from_iso('1998-12-31 23:59:60'),
                         tai_from_day_sec(-366, 86400))
        self.assertEqual(time_from_iso('  1998-12-31 23:59:60 ', strip=True),
                         tai_from_day_sec(-366, 86400))

        self.assertEqual(time_from_iso( '2001-01-01 01:00:00', timesys='TDB'),
                         tdb_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(time_from_iso( '2001-01-01T01:00:00', timesys='TDB'),
                         tdb_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(time_from_iso('1998-12-31 23:59:60', timesys='TDB'),
                         tdb_from_tai(tai_from_day_sec(-366, 86400)))
        self.assertEqual(time_from_iso(' 1998-12-31 23:59:60', strip=True, timesys='TDB'),
                         tdb_from_tai(tai_from_day_sec(-366, 86400)))

        self.assertEqual(time_from_iso( '2001-01-01 01:00:00', timesys='TT'),
                         tt_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(time_from_iso( '2001-01-01T01:00:00', timesys='TT'),
                         tt_from_tai(tai_from_day_sec(366, 3600)))
        self.assertEqual(time_from_iso('1998-12-31 23:59:60', timesys='TT'),
                         tt_from_tai(tai_from_day_sec(-366, 86400)))
        self.assertEqual(time_from_iso(' 1998-12-31 23:59:60', strip=True, timesys='TT'),
                         tt_from_tai(tai_from_day_sec(-366, 86400)))


########################################
# Executed from the command line
########################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
