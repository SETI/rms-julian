##########################################################################################
# julian/test_formatters.py
##########################################################################################

import numpy as np
import unittest

from julian.formatters import (
    format_day,
    format_day_sec,
    format_sec,
    iso_from_tai,
)

from julian._DEPRECATED import (
    hms_format_from_sec,
    yd_format_from_day,
    ydhms_format_from_day_sec,
    ydhms_format_from_tai,
    ymd_format_from_day,
    ymdhms_format_from_day_sec,
    ymdhms_format_from_tai,
)

from julian.calendar    import day_from_ymd
from julian._exceptions import JulianValidateFailure as JVF

DAY_TESTS = [0, 100000, -200000]

# This code generates the DAY_ANSWERS answers below...

# for order in ('YMD', 'MDY', 'DMY', 'YD', 'DY'):
#   for ydigits in (4,2):
#     for dash in ('-', '/', '', '{}'):
#       for proleptic in (False, True):
#         answers = format_day(DAY_TESTS, order=order, ydigits=ydigits, dash=dash,
#                                         proleptic=proleptic)
#         rec = ['    (', repr(order), ' ' if len(order) == 2 else '', ', ',
#                str(ydigits), ', ', repr(dash), (2-len(dash)) * ' ', ', ',
#                'True ' if proleptic else 'False', '): [']
#         for answer in answers:
#             rec += [repr(answer), (12-len(answer)) * ' ', ', ']
#         rec[-1] = '],'
#         print(''.join(rec))

DAY_ANSWERS = {
    ('YMD', 4, '-' , False): ['2000-01-01'  , '2273-10-16'  , '1452-05-24'  ],
    ('YMD', 4, '-' , True ): ['2000-01-01'  , '2273-10-16'  , '1452-06-02'  ],
    ('YMD', 4, '/' , False): ['2000/01/01'  , '2273/10/16'  , '1452/05/24'  ],
    ('YMD', 4, '/' , True ): ['2000/01/01'  , '2273/10/16'  , '1452/06/02'  ],
    ('YMD', 4, ''  , False): ['20000101'    , '22731016'    , '14520524'    ],
    ('YMD', 4, ''  , True ): ['20000101'    , '22731016'    , '14520602'    ],
    ('YMD', 4, '{}', False): ['2000{}01{}01', '2273{}10{}16', '1452{}05{}24'],
    ('YMD', 4, '{}', True ): ['2000{}01{}01', '2273{}10{}16', '1452{}06{}02'],
    ('YMD', 2, '-' , False): ['00-01-01'    , '73-10-16'    , '52-05-24'    ],
    ('YMD', 2, '-' , True ): ['00-01-01'    , '73-10-16'    , '52-06-02'    ],
    ('YMD', 2, '/' , False): ['00/01/01'    , '73/10/16'    , '52/05/24'    ],
    ('YMD', 2, '/' , True ): ['00/01/01'    , '73/10/16'    , '52/06/02'    ],
    ('YMD', 2, ''  , False): ['000101'      , '731016'      , '520524'      ],
    ('YMD', 2, ''  , True ): ['000101'      , '731016'      , '520602'      ],
    ('YMD', 2, '{}', False): ['00{}01{}01'  , '73{}10{}16'  , '52{}05{}24'  ],
    ('YMD', 2, '{}', True ): ['00{}01{}01'  , '73{}10{}16'  , '52{}06{}02'  ],
    ('MDY', 4, '-' , False): ['01-01-2000'  , '10-16-2273'  , '05-24-1452'  ],
    ('MDY', 4, '-' , True ): ['01-01-2000'  , '10-16-2273'  , '06-02-1452'  ],
    ('MDY', 4, '/' , False): ['01/01/2000'  , '10/16/2273'  , '05/24/1452'  ],
    ('MDY', 4, '/' , True ): ['01/01/2000'  , '10/16/2273'  , '06/02/1452'  ],
    ('MDY', 4, ''  , False): ['01012000'    , '10162273'    , '05241452'    ],
    ('MDY', 4, ''  , True ): ['01012000'    , '10162273'    , '06021452'    ],
    ('MDY', 4, '{}', False): ['01{}01{}2000', '10{}16{}2273', '05{}24{}1452'],
    ('MDY', 4, '{}', True ): ['01{}01{}2000', '10{}16{}2273', '06{}02{}1452'],
    ('MDY', 2, '-' , False): ['01-01-00'    , '10-16-73'    , '05-24-52'    ],
    ('MDY', 2, '-' , True ): ['01-01-00'    , '10-16-73'    , '06-02-52'    ],
    ('MDY', 2, '/' , False): ['01/01/00'    , '10/16/73'    , '05/24/52'    ],
    ('MDY', 2, '/' , True ): ['01/01/00'    , '10/16/73'    , '06/02/52'    ],
    ('MDY', 2, ''  , False): ['010100'      , '101673'      , '052452'      ],
    ('MDY', 2, ''  , True ): ['010100'      , '101673'      , '060252'      ],
    ('MDY', 2, '{}', False): ['01{}01{}00'  , '10{}16{}73'  , '05{}24{}52'  ],
    ('MDY', 2, '{}', True ): ['01{}01{}00'  , '10{}16{}73'  , '06{}02{}52'  ],
    ('DMY', 4, '-' , False): ['01-01-2000'  , '16-10-2273'  , '24-05-1452'  ],
    ('DMY', 4, '-' , True ): ['01-01-2000'  , '16-10-2273'  , '02-06-1452'  ],
    ('DMY', 4, '/' , False): ['01/01/2000'  , '16/10/2273'  , '24/05/1452'  ],
    ('DMY', 4, '/' , True ): ['01/01/2000'  , '16/10/2273'  , '02/06/1452'  ],
    ('DMY', 4, ''  , False): ['01012000'    , '16102273'    , '24051452'    ],
    ('DMY', 4, ''  , True ): ['01012000'    , '16102273'    , '02061452'    ],
    ('DMY', 4, '{}', False): ['01{}01{}2000', '16{}10{}2273', '24{}05{}1452'],
    ('DMY', 4, '{}', True ): ['01{}01{}2000', '16{}10{}2273', '02{}06{}1452'],
    ('DMY', 2, '-' , False): ['01-01-00'    , '16-10-73'    , '24-05-52'    ],
    ('DMY', 2, '-' , True ): ['01-01-00'    , '16-10-73'    , '02-06-52'    ],
    ('DMY', 2, '/' , False): ['01/01/00'    , '16/10/73'    , '24/05/52'    ],
    ('DMY', 2, '/' , True ): ['01/01/00'    , '16/10/73'    , '02/06/52'    ],
    ('DMY', 2, ''  , False): ['010100'      , '161073'      , '240552'      ],
    ('DMY', 2, ''  , True ): ['010100'      , '161073'      , '020652'      ],
    ('DMY', 2, '{}', False): ['01{}01{}00'  , '16{}10{}73'  , '24{}05{}52'  ],
    ('DMY', 2, '{}', True ): ['01{}01{}00'  , '16{}10{}73'  , '02{}06{}52'  ],
    ('YD' , 4, '-' , False): ['2000-001'    , '2273-289'    , '1452-145'    ],
    ('YD' , 4, '-' , True ): ['2000-001'    , '2273-289'    , '1452-154'    ],
    ('YD' , 4, '/' , False): ['2000/001'    , '2273/289'    , '1452/145'    ],
    ('YD' , 4, '/' , True ): ['2000/001'    , '2273/289'    , '1452/154'    ],
    ('YD' , 4, ''  , False): ['2000001'     , '2273289'     , '1452145'     ],
    ('YD' , 4, ''  , True ): ['2000001'     , '2273289'     , '1452154'     ],
    ('YD' , 4, '{}', False): ['2000{}001'   , '2273{}289'   , '1452{}145'   ],
    ('YD' , 4, '{}', True ): ['2000{}001'   , '2273{}289'   , '1452{}154'   ],
    ('YD' , 2, '-' , False): ['00-001'      , '73-289'      , '52-145'      ],
    ('YD' , 2, '-' , True ): ['00-001'      , '73-289'      , '52-154'      ],
    ('YD' , 2, '/' , False): ['00/001'      , '73/289'      , '52/145'      ],
    ('YD' , 2, '/' , True ): ['00/001'      , '73/289'      , '52/154'      ],
    ('YD' , 2, ''  , False): ['00001'       , '73289'       , '52145'       ],
    ('YD' , 2, ''  , True ): ['00001'       , '73289'       , '52154'       ],
    ('YD' , 2, '{}', False): ['00{}001'     , '73{}289'     , '52{}145'     ],
    ('YD' , 2, '{}', True ): ['00{}001'     , '73{}289'     , '52{}154'     ],
    ('DY' , 4, '-' , False): ['001-2000'    , '289-2273'    , '145-1452'    ],
    ('DY' , 4, '-' , True ): ['001-2000'    , '289-2273'    , '154-1452'    ],
    ('DY' , 4, '/' , False): ['001/2000'    , '289/2273'    , '145/1452'    ],
    ('DY' , 4, '/' , True ): ['001/2000'    , '289/2273'    , '154/1452'    ],
    ('DY' , 4, ''  , False): ['0012000'     , '2892273'     , '1451452'     ],
    ('DY' , 4, ''  , True ): ['0012000'     , '2892273'     , '1541452'     ],
    ('DY' , 4, '{}', False): ['001{}2000'   , '289{}2273'   , '145{}1452'   ],
    ('DY' , 4, '{}', True ): ['001{}2000'   , '289{}2273'   , '154{}1452'   ],
    ('DY' , 2, '-' , False): ['001-00'      , '289-73'      , '145-52'      ],
    ('DY' , 2, '-' , True ): ['001-00'      , '289-73'      , '154-52'      ],
    ('DY' , 2, '/' , False): ['001/00'      , '289/73'      , '145/52'      ],
    ('DY' , 2, '/' , True ): ['001/00'      , '289/73'      , '154/52'      ],
    ('DY' , 2, ''  , False): ['00100'       , '28973'       , '14552'       ],
    ('DY' , 2, ''  , True ): ['00100'       , '28973'       , '15452'       ],
    ('DY' , 2, '{}', False): ['001{}00'     , '289{}73'     , '145{}52'     ],
    ('DY' , 2, '{}', True ): ['001{}00'     , '289{}73'     , '154{}52'     ],
}

FDAY_TESTS = [DAY_TESTS[0] + 0., DAY_TESTS[1] + 0.25, DAY_TESTS[2] + 0.375]

# This code generates the FDAY_ANSWERS answers below...

# for order in ('YMD', 'MDY', 'YD'):
#     for ddigits in (None, -1, 0, 1, 2):
#         answers = format_day(FDAY_TESTS, order=order, ddigits=ddigits)
#         rec = ['    (', repr(order), ' ' if len(order) == 2 else '', ', ',
#                'None' if ddigits is None else '%4d' % ddigits, '): [']
#         for answer in answers:
#             rec += [repr(answer), (13-len(answer)) * ' ', ', ']
#         rec[-1] = '],'
#         print(''.join(rec))

FDAY_ANSWERS = {
    ('YMD', None): ['2000-01-01'   , '2273-10-16'   , '1452-06-02'   ],
    ('YMD',   -1): ['2000-01-01'   , '2273-10-16'   , '1452-06-02'   ],
    ('YMD',    0): ['2000-01-01.'  , '2273-10-16.'  , '1452-06-02.'  ],
    ('YMD',    1): ['2000-01-01.0' , '2273-10-16.3' , '1452-06-02.4' ],
    ('YMD',    2): ['2000-01-01.00', '2273-10-16.25', '1452-06-02.38'],
    ('MDY', None): ['01-01-2000'   , '10-16-2273'   , '06-02-1452'   ],
    ('MDY',   -1): ['01-01-2000'   , '10-16-2273'   , '06-02-1452'   ],
    ('MDY',    0): ['01-01.-2000'  , '10-16.-2273'  , '06-02.-1452'  ],
    ('MDY',    1): ['01-01.0-2000' , '10-16.3-2273' , '06-02.4-1452' ],
    ('MDY',    2): ['01-01.00-2000', '10-16.25-2273', '06-02.38-1452'],
    ('YD' , None): ['2000-001'     , '2273-289'     , '1452-154'     ],
    ('YD' ,   -1): ['2000-001'     , '2273-289'     , '1452-154'     ],
    ('YD' ,    0): ['2000-001.'    , '2273-289.'    , '1452-154.'    ],
    ('YD' ,    1): ['2000-001.0'   , '2273-289.3'   , '1452-154.4'   ],
    ('YD' ,    2): ['2000-001.00'  , '2273-289.25'  , '1452-154.38'  ],
}

TIME_TESTS = [0, 7263, 86409]

# This code generates the TIME_ANSWERS below...

# for colon in (':', '', '{}'):
#     for suffix in ('', 'Z', '-08'):
#         answers = format_sec(TIME_TESTS, colon=colon, suffix=suffix)
#         rec = ['    (', repr(colon), (2-len(colon)) * ' ', ', ',
#                repr(suffix), (3-len(suffix)) * ' ', '): [']
#         for answer in answers:
#             rec += [repr(answer), (13-len(answer)) * ' ', ', ']
#         rec[-1] = '],'
#         print(''.join(rec))

TIME_ANSWERS = {
    (':' , ''   ): ['00:00:00'     , '02:01:03'     , '23:59:69'     ],
    (':' , 'Z'  ): ['00:00:00Z'    , '02:01:03Z'    , '23:59:69Z'    ],
    (':' , '-08'): ['00:00:00-08'  , '02:01:03-08'  , '23:59:69-08'  ],
    (''  , ''   ): ['000000'       , '020103'       , '235969'       ],
    (''  , 'Z'  ): ['000000Z'      , '020103Z'      , '235969Z'      ],
    (''  , '-08'): ['000000-08'    , '020103-08'    , '235969-08'    ],
    ('{}', ''   ): ['00{}00{}00'   , '02{}01{}03'   , '23{}59{}69'   ],
    ('{}', 'Z'  ): ['00{}00{}00Z'  , '02{}01{}03Z'  , '23{}59{}69Z'  ],
    ('{}', '-08'): ['00{}00{}00-08', '02{}01{}03-08', '23{}59{}69-08'],
}

FTIME_TESTS = [0., 7263.5, 86409.875]

# This code generates the FTIME_ANSWERS below...

# for digits in (None, -1, 0, 1, 2, 3):
#     answers = format_sec(FTIME_TESTS, digits=digits)
#     rec = ['    ', 'None' if digits is None else '%4d' % digits, ': [']
#     for answer in answers:
#         rec += [repr(answer), (12-len(answer)) * ' ', ', ']
#     rec[-1] = '],'
#     print(''.join(rec))

FTIME_ANSWERS = {
    None: ['00:00:00'    , '02:01:03'    , '23:59:69'    ],
      -1: ['00:00:00'    , '02:01:03'    , '23:59:69'    ],     # noqa
       0: ['00:00:00.'   , '02:01:03.'   , '23:59:69.'   ],     # noqa
       1: ['00:00:00.0'  , '02:01:03.5'  , '23:59:69.9'  ],     # noqa
       2: ['00:00:00.00' , '02:01:03.50' , '23:59:69.88' ],     # noqa
       3: ['00:00:00.000', '02:01:03.500', '23:59:69.875'],     # noqa
}


class Test_formatters(unittest.TestCase):

    def test_format_day(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        for key, answers in DAY_ANSWERS.items():
            (order, ydigits, dash, proleptic) = key

            for ddigits in (None, -1, 0, 1):    # ignored for integer days, right?

                # kind = "U", shape = (3,), buffer=None
                results = format_day(DAY_TESTS, order=order, ydigits=ydigits, dash=dash,
                                     proleptic=proleptic, ddigits=ddigits)
                for k in range(3):
                    self.assertEqual(answers[k], results[k])

                # kind = "U", shape = (), buffer=None
                for k in range(3):
                    result = format_day(DAY_TESTS[k], order=order, ydigits=ydigits,
                                        dash=dash, proleptic=proleptic, ddigits=ddigits)
                    self.assertEqual(answers[k], result)

                # kind = "S", shape = (3,), buffer=None
                results = format_day(DAY_TESTS, order=order, ydigits=ydigits, dash=dash,
                                     proleptic=proleptic, ddigits=ddigits, kind='S')
                for k in range(3):
                    self.assertEqual(answers[k].encode('latin8'), results[k])

                # kind = "S", shape = (), buffer=None
                for k in range(3):
                    result = format_day(DAY_TESTS[k], order=order, ydigits=ydigits,
                                        dash=dash, proleptic=proleptic, ddigits=ddigits,
                                        kind='S')
                    self.assertEqual(answers[k].encode('latin8'), result)

                # kind = "U", shape = (3,), buffer provided
                buffer = np.empty((4,), dtype='=U30')
                results = format_day(DAY_TESTS, order=order, ydigits=ydigits, dash=dash,
                                     proleptic=proleptic, ddigits=ddigits,
                                     buffer=buffer)
                self.assertIs(results, buffer)
                for k in range(3):
                    self.assertEqual(answers[k], buffer[k])
                self.assertEqual(buffer[3], '')

                # kind = "U", shape = (), buffer provided
                for k in range(3):
                    result = format_day(DAY_TESTS[k], order=order, ydigits=ydigits,
                                        dash=dash, proleptic=proleptic, ddigits=ddigits,
                                        buffer=buffer)
                    self.assertIs(result, buffer)
                    self.assertEqual(answers[k], result[k])

                # kind = "S", shape = (3,), buffer provided
                buffer = np.empty((4,), dtype='|S30')
                results = format_day(DAY_TESTS, order=order, ydigits=ydigits, dash=dash,
                                     proleptic=proleptic, ddigits=ddigits,
                                     buffer=buffer)
                self.assertIs(results, buffer)
                for k in range(3):
                    self.assertEqual(answers[k].encode('latin8'), buffer[k])
                self.assertEqual(buffer[3], b'')

                # kind = "S", shape = (), buffer provided
                for k in range(3):
                    result = format_day(DAY_TESTS[k], order=order, ydigits=ydigits,
                                        dash=dash, proleptic=proleptic, ddigits=ddigits,
                                        buffer=buffer)
                    self.assertIs(result, buffer)
                    self.assertEqual(answers[k].encode('latin8'), result[k])

                # shape = (3,), buffer too small
                for buffer in [np.empty((2,), dtype='=U30'),
                               np.empty((2,), dtype='|S30')]:
                    self.assertRaises(ValueError, format_day, DAY_TESTS,
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, ddigits=ddigits, buffer=buffer)

                for buffer in [np.empty((4,), dtype='=U4'),
                               np.empty((4,), dtype='|S4')]:
                    self.assertRaises(ValueError, format_day, DAY_TESTS,
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, ddigits=ddigits, buffer=buffer)

                # shape = (), buffer too small
                for buffer in [np.empty((4,), dtype='=U4'),
                               np.empty((4,), dtype='|S4')]:
                    self.assertRaises(ValueError, format_day, DAY_TESTS[0],
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, ddigits=ddigits, buffer=buffer)

        for key, answers in FDAY_ANSWERS.items():
            (order, ddigits) = key

            # kind = "U"
            results = format_day(FDAY_TESTS, order=order, ddigits=ddigits, kind='U',
                                 proleptic=True)
            for k in range(3):
                self.assertEqual(answers[k], results[k])

            for k in range(3):
                result = format_day(FDAY_TESTS[k], order=order, ddigits=ddigits, kind='U',
                                    proleptic=True)
                self.assertEqual(answers[k], result)

            # kind = "S"
            results = format_day(FDAY_TESTS, order=order, ddigits=ddigits, kind='S',
                                 proleptic=True)
            for k in range(3):
                self.assertEqual(answers[k].encode('latin8'), results[k])

            for k in range(3):
                result = format_day(FDAY_TESTS[k], order=order, ddigits=ddigits, kind='S',
                                    proleptic=True)
                self.assertEqual(answers[k].encode('latin8'), result)

        # Old tests, just keep 'em around
        self.assertEqual(ymd_format_from_day(0), '2000-01-01')
        self.assertEqual(ymd_format_from_day(0, dash=''), '20000101')
        self.assertEqual(ymd_format_from_day(0, dash='/'), '2000/01/01')
        self.assertEqual(ymd_format_from_day(0, ydigits=2), '00-01-01')
        self.assertEqual(ymd_format_from_day(0, ydigits=2, dash=''), '000101')
        self.assertEqual(ymd_format_from_day(0, ydigits=2, dash='/'), '00/01/01')
        self.assertEqual(ymd_format_from_day(0, ydigits=2, ddigits=1), '00-01-01')

        self.assertEqual(ymd_format_from_day(31.), '2000-02-01')
        self.assertEqual(ymd_format_from_day(31., dash=''), '20000201')
        self.assertEqual(ymd_format_from_day(31., ydigits=2, ddigits=2), '00-02-01.00')
        self.assertEqual(ymd_format_from_day(31., dash='', ddigits=1), '20000201.0')

        self.assertEqual(ymd_format_from_day(31.5, ddigits=0), '2000-02-02.')
        self.assertEqual(ymd_format_from_day(31.49999, ddigits=0), '2000-02-01.')

        self.assertTrue(np.all(ymd_format_from_day([0,31.]) ==
                                    ['2000-01-01', '2000-02-01']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], dash='') ==
                                    ['20000101', '20000201']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], dash='/') ==
                                    ['2000/01/01', '2000/02/01']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], ydigits=2) ==
                                    ['00-01-01', '00-02-01']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], ydigits=2, dash='') ==
                                    ['000101', '000201']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], ydigits=2, dash='/') ==
                                    ['00/01/01', '00/02/01']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.], ydigits=2, ddigits=1) ==
                                    ['00-01-01.0', '00-02-01.0']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.005], ddigits=2) ==
                                    ['2000-01-01.00', '2000-02-01.01']))
        self.assertTrue(np.all(ymd_format_from_day([0,31.004999], ddigits=2) ==
                                    ['2000-01-01.00', '2000-02-01.00']))

        self.assertEqual(ymd_format_from_day(31.), '2000-02-01')
        self.assertEqual(ymd_format_from_day(31., dash=''), '20000201')
        self.assertEqual(ymd_format_from_day(31., ydigits=2, ddigits=2), '00-02-01.00')
        self.assertEqual(ymd_format_from_day(31., dash='', ddigits=1), '20000201.0')

        self.assertTrue(np.all(ymd_format_from_day([-365,0,366])
                               == ['1999-01-01', '2000-01-01', '2001-01-01']))

        # yd_format_from_day()
        self.assertEqual(yd_format_from_day(0), '2000-001')

        self.assertTrue(np.all(yd_format_from_day([-365,0,366])
                               == ['1999-001', '2000-001', '2001-001']))

        # Check if yd_format_from_day start from 2000-001
        self.assertEqual(yd_format_from_day(0), '2000-001')

        # Errors
        self.assertRaises(ValueError, format_day, 0, order='YYY')
        self.assertRaises(ValueError, format_day, 0, ydigits=3)
        self.assertRaises(ValueError, format_day, 0, kind='X')
        self.assertRaises(ValueError, format_day, 0, buffer=np.empty((3,), dtype='int'))
        self.assertRaises(ValueError, format_day, [[0,0],[0,0]],
                                                  buffer=np.empty((3,3), dtype='U40'))

    def test_format_sec(self):

        for key, answers in TIME_ANSWERS.items():
            (colon, suffix) = key

            # kind = "U", shape = (3,), buffer=None
            results = format_sec(TIME_TESTS, colon=colon, suffix=suffix)
            for k in range(3):
                self.assertEqual(answers[k], results[k])

            # kind = "U", shape = (), buffer=None
            for k in range(3):
                result = format_sec(TIME_TESTS[k], colon=colon, suffix=suffix)
                self.assertEqual(answers[k], result)

            # kind = "S", shape = (3,), buffer=None
            results = format_sec(TIME_TESTS, colon=colon, suffix=suffix, kind='S')
            for k in range(3):
                self.assertEqual(answers[k].encode('latin8'), results[k])

            # kind = "S", shape = (), buffer=None
            for k in range(3):
                result = format_sec(TIME_TESTS[k], colon=colon, suffix=suffix,
                                    kind='S')
                self.assertEqual(answers[k].encode('latin8'), result)

            # kind = "U", shape = (3,), buffer provided
            buffer = np.empty((4,), dtype='=U30')
            results = format_sec(TIME_TESTS, colon=colon, suffix=suffix,
                                 buffer=buffer)
            self.assertIs(results, buffer)
            for k in range(3):
                self.assertEqual(answers[k], buffer[k])
            self.assertEqual(buffer[3], '')

            # kind = "U", shape = (), buffer provided
            for k in range(3):
                result = format_sec(TIME_TESTS[k], colon=colon, suffix=suffix,
                                    buffer=buffer)
                self.assertIs(result, buffer)
                self.assertEqual(answers[k], result[k])

            # kind = "S", shape = (3,), buffer provided
            buffer = np.empty((4,), dtype='|S30')
            results = format_sec(TIME_TESTS, colon=colon, suffix=suffix,
                                 buffer=buffer)
            self.assertIs(results, buffer)
            for k in range(3):
                self.assertEqual(answers[k].encode('latin8'), buffer[k])
            self.assertEqual(buffer[3], b'')

            # kind = "S", shape = (), buffer provided
            for k in range(3):
                result = format_sec(TIME_TESTS[k], colon=colon, suffix=suffix,
                                    buffer=buffer)
                self.assertIs(result, buffer)
                self.assertEqual(answers[k].encode('latin8'), result[k])

            # shape = (3,), buffer too small
            for buffer in [np.empty((2,), dtype='=U30'),
                           np.empty((2,), dtype='|S30')]:
                self.assertRaises(ValueError, format_sec, TIME_TESTS,
                                  colon=colon, suffix=suffix, buffer=buffer)

            for buffer in [np.empty((4,), dtype='=U4'),
                           np.empty((4,), dtype='|S4')]:
                self.assertRaises(ValueError, format_sec, TIME_TESTS,
                                  colon=colon, suffix=suffix, buffer=buffer)

            # shape = (), buffer too small
            for buffer in [np.empty((4,), dtype='=U4'),
                           np.empty((4,), dtype='|S4')]:
                self.assertRaises(ValueError, format_sec, TIME_TESTS[0],
                                  colon=colon, suffix=suffix, buffer=buffer)

        for digits, answers in FTIME_ANSWERS.items():

            # kind = "U"
            results = format_sec(FTIME_TESTS, digits=digits, kind='U')
            for k in range(3):
                self.assertEqual(answers[k], results[k])

            for k in range(3):
                result = format_sec(FTIME_TESTS[k], digits=digits, kind='U')
                self.assertEqual(answers[k], result)

            # kind = "S"
            results = format_sec(FTIME_TESTS, digits=digits, kind='S')
            for k in range(3):
                self.assertEqual(answers[k].encode('latin8'), results[k])

            for k in range(3):
                result = format_sec(FTIME_TESTS[k], digits=digits, kind='S')
                self.assertEqual(answers[k].encode('latin8'), result)

        # old tests...

        # Check if one day is 86400 seconds
        self.assertEqual(hms_format_from_sec(86400), '23:59:60')

        # Check if hms_format_from_sec end with 86409
        self.assertEqual(hms_format_from_sec(86409), '23:59:69')

        # Check if hms_format_from_sec returns the correct format.
        self.assertEqual(hms_format_from_sec(0.), '00:00:00')
        self.assertEqual(hms_format_from_sec(0., digits=3), '00:00:00.000')
        self.assertEqual(hms_format_from_sec(0., digits=3, suffix='Z'), '00:00:00.000Z')

        # Check if hms_format_from_sec accepts seconds over 86410
        self.assertRaises(JVF, hms_format_from_sec, 86411)

        # Errors
        self.assertRaises(ValueError, format_sec, 0, kind='X')
        self.assertRaises(ValueError, format_sec, 0, buffer=np.empty((3,), dtype='int'))
        self.assertRaises(ValueError, format_sec, [[0,0],[0,0]],
                                                  buffer=np.empty((3,3), dtype='U40'))

    def test_format_day_sec(self):

        for dkey, d_answers in DAY_ANSWERS.items():
          (day_order, ydigits, dash, proleptic) = dkey

          for tkey, t_answers in TIME_ANSWERS.items():
            (colon, suffix) = tkey

          for sep in ('T', ' ', '', '///'):
            for tbefore in (True, False):
                if tbefore:
                    answers = [t_answers[k] + sep + d_answers[k] for k in range(2)]
                    order = 'T' + day_order
                else:
                    answers = [d_answers[k] + sep + t_answers[k] for k in range(2)]
                    order = day_order + 'T'

                # kind = "U", shape = (3,), buffer=None
                results = format_day_sec(DAY_TESTS[:2], TIME_TESTS[:2],
                                         order=order, ydigits=ydigits, dash=dash,
                                         proleptic=proleptic, sep=sep, colon=colon,
                                         suffix=suffix)
                for k in range(2):
                    self.assertEqual(answers[k], results[k])

                # kind = "U", shape = (), buffer=None
                for k in range(2):
                    result = format_day_sec(DAY_TESTS[k], TIME_TESTS[k],
                                            order=order, ydigits=ydigits, dash=dash,
                                            proleptic=proleptic, sep=sep, colon=colon,
                                            suffix=suffix)
                    self.assertEqual(answers[k], result)

                # kind = "S", shape = (3,), buffer=None
                results = format_day_sec(DAY_TESTS[:2], TIME_TESTS[:2],
                                         order=order, ydigits=ydigits, dash=dash,
                                         proleptic=proleptic, sep=sep, colon=colon,
                                         suffix=suffix, kind='S')
                for k in range(2):
                    self.assertEqual(answers[k].encode('latin8'), results[k])

                # kind = "S", shape = (), buffer=None
                for k in range(2):
                    result = format_day_sec(DAY_TESTS[k], TIME_TESTS[k],
                                            order=order, ydigits=ydigits, dash=dash,
                                            proleptic=proleptic, sep=sep, colon=colon,
                                            suffix=suffix, kind='S')
                    self.assertEqual(answers[k].encode('latin8'), result)

                # kind = "U", shape = (3,), buffer provided
                buffer = np.empty((4,), dtype='=U50')
                results = format_day_sec(DAY_TESTS[:2], TIME_TESTS[:2],
                                         order=order, ydigits=ydigits, dash=dash,
                                         proleptic=proleptic, sep=sep, colon=colon,
                                         suffix=suffix, buffer=buffer)
                self.assertIs(results, buffer)
                for k in range(2):
                    self.assertEqual(answers[k], buffer[k])
                self.assertEqual(buffer[2], '')

                # kind = "U", shape = (), buffer provided
                for k in range(2):
                    result = format_day_sec(DAY_TESTS[k], TIME_TESTS[k],
                                            order=order, ydigits=ydigits, dash=dash,
                                            proleptic=proleptic, sep=sep, colon=colon,
                                            suffix=suffix, buffer=buffer)
                    self.assertIs(result, buffer)
                    self.assertEqual(answers[k], result[k])

                # kind = "S", shape = (3,), buffer provided
                buffer = np.empty((4,), dtype='|S50')
                results = format_day_sec(DAY_TESTS[:2], TIME_TESTS[:2],
                                         order=order, ydigits=ydigits, dash=dash,
                                         proleptic=proleptic, sep=sep, colon=colon,
                                         suffix=suffix, buffer=buffer)
                self.assertIs(results, buffer)
                for k in range(2):
                    self.assertEqual(answers[k].encode('latin8'), buffer[k])
                self.assertEqual(buffer[2], b'')

                # kind = "S", shape = (), buffer provided
                for k in range(2):
                    result = format_day_sec(DAY_TESTS[k], TIME_TESTS[k],
                                            order=order, ydigits=ydigits, dash=dash,
                                            proleptic=proleptic, sep=sep, colon=colon,
                                            suffix=suffix, buffer=buffer)
                    self.assertIs(result, buffer)
                    self.assertEqual(answers[k].encode('latin8'), result[k])

                # shape = (3,), buffer too small
                for buffer in [np.empty((1,), dtype='=U50'),
                               np.empty((1,), dtype='|S50')]:
                    self.assertRaises(ValueError, format_day_sec,
                                      DAY_TESTS[:2], TIME_TESTS[:2],
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, sep=sep, colon=colon,
                                      suffix=suffix, buffer=buffer)

                for buffer in [np.empty((4,), dtype='=U4'),
                               np.empty((4,), dtype='|S4')]:
                    self.assertRaises(ValueError, format_day_sec,
                                      DAY_TESTS[:2], TIME_TESTS[:2],
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, sep=sep, colon=colon,
                                      suffix=suffix, buffer=buffer)

                # shape = (), buffer too small
                for buffer in [np.empty((4,), dtype='=U4'),
                               np.empty((4,), dtype='|S4')]:
                    self.assertRaises(ValueError, format_day_sec,
                                      DAY_TESTS[0], TIME_TESTS[0],
                                      order=order, ydigits=ydigits, dash=dash,
                                      proleptic=proleptic, colon=colon, suffix=suffix,
                                      buffer=buffer)

            # Check a case with the exact right buffer size so no "extra"
            result = format_day_sec(0, 43201, buffer=None)
            self.assertEqual(result, '2000-01-01T12:00:01')

            for l in (len(result), len(result)+1):
                result = format_day_sec(0, 43201, buffer=np.empty((), 'U' + str(l)))
                self.assertEqual(result, '2000-01-01T12:00:01')

                result = format_day_sec(0, 43201, buffer=np.empty((), 'S' + str(l)))
                self.assertEqual(result, b'2000-01-01T12:00:01')

        # old tests...

        # Check if ymdhms_format_from_day_sec returns the correct format.
        self.assertEqual(ymdhms_format_from_day_sec(0, 0),
                         '2000-01-01T00:00:00')
        self.assertEqual(ymdhms_format_from_day_sec(0, 0, sep='T', digits=3),
                         '2000-01-01T00:00:00.000')
        self.assertEqual(ymdhms_format_from_day_sec(0, 0, sep='T', digits=3,
                                                          suffix='Z'),
                         '2000-01-01T00:00:00.000Z')
        self.assertEqual(ymdhms_format_from_day_sec(0, 0, sep='T', digits=None),
                         '2000-01-01T00:00:00')
        self.assertEqual(ymdhms_format_from_day_sec(0, 0, sep='T', digits=None,
                                                          suffix='Z'),
                         '2000-01-01T00:00:00Z')
        self.assertEqual(ydhms_format_from_day_sec(0, 0, sep='T', digits=None,
                                                         suffix='Z', kind='S'),
                         b'2000-001T00:00:00Z')

        self.assertEqual(ymdhms_format_from_tai(32 - 43200),
                         '2000-01-01T00:00:00')
        self.assertEqual(ymdhms_format_from_tai(32 - 43200, sep='T', digits=3),
                         '2000-01-01T00:00:00.000')
        self.assertEqual(ymdhms_format_from_tai(32 - 43200, sep='T', digits=3,
                                                          suffix='Z'),
                         '2000-01-01T00:00:00.000Z')
        self.assertEqual(ymdhms_format_from_tai(32 - 43200, sep='T', digits=None),
                         '2000-01-01T00:00:00')
        self.assertEqual(ymdhms_format_from_tai(32 - 43200, sep='T', digits=None,
                                                          suffix='Z'),
                         '2000-01-01T00:00:00Z')
        self.assertEqual(ydhms_format_from_tai(32 - 43200, sep='T', digits=None,
                                                         suffix='Z', kind='S'),
                         b'2000-001T00:00:00Z')
        self.assertEqual(iso_from_tai(23456789012.345, ymd=True, digits=3, suffix='Z'),
                         ymdhms_format_from_tai(23456789012.345, digits=3, suffix='Z'))
        self.assertEqual(iso_from_tai(-23456789012.345, ymd=False, digits=3, suffix='Z'),
                         ydhms_format_from_tai(-23456789012.345, digits=3, suffix='Z'))

        ymdhms = ymdhms_format_from_day_sec([0,366],[0,43200])
        self.assertTrue(np.all(ymdhms == ('2000-01-01T00:00:00', '2001-01-01T12:00:00')))

        # Check TAI formatting
        # The 32's below are for the offset between TAI and UTC
        self.assertTrue(np.all(ydhms_format_from_tai([32.-43200,366.*86400.+32.-43200])
                               == ('2000-001T00:00:00', '2001-001T00:00:00')))

        # Buffers
        answer = np.array(['1999-001', '2000-001', '2001-001'])
        buffer = np.empty(answer.shape, answer.dtype)
        result = yd_format_from_day([-365,0,366], buffer=buffer)
        self.assertTrue(result is buffer)

        # Check overflow to next day
        self.assertEqual(format_day_sec(60, 86399  ), '2000-03-01T23:59:59')
        self.assertEqual(format_day_sec(60, 86399.9), '2000-03-02T00:00:00')

        results = format_day_sec(60, np.arange(86399, 86400, 0.25))
        self.assertEqual(results[0], '2000-03-01T23:59:59')
        self.assertEqual(results[1], '2000-03-01T23:59:59')
        self.assertEqual(results[2], '2000-03-02T00:00:00')
        self.assertEqual(results[3], '2000-03-02T00:00:00')

        # Check leap seconds
        days = day_from_ymd([1973, 2016, 2018], 12, 31)
        results = format_day_sec(days, 86400)
        self.assertEqual(results[0], '1973-12-31T23:59:60')
        self.assertEqual(results[1], '2016-12-31T23:59:60')
        self.assertEqual(results[2], '2019-01-01T00:00:00')

        result = format_day_sec(days[0], 86400)
        self.assertEqual(result, '1973-12-31T23:59:60')

        results = format_day_sec(days, 86400.96, digits=2)
        self.assertEqual(results[0], '1973-12-31T23:59:60.96')
        self.assertEqual(results[1], '2016-12-31T23:59:60.96')
        self.assertEqual(results[2], '2019-01-01T00:00:00.96')

        result = format_day_sec(days[2], 86400.96, digits=2)
        self.assertEqual(result, '2019-01-01T00:00:00.96')

        results = format_day_sec(days, 86400.96, digits=1)
        self.assertEqual(results[0], '1974-01-01T00:00:00.0')
        self.assertEqual(results[1], '2017-01-01T00:00:00.0')
        self.assertEqual(results[2], '2019-01-01T00:00:01.0')

        result = format_day_sec(days[1], 86400.96, digits=1)
        self.assertEqual(result, '2017-01-01T00:00:00.0')

        # Errors
        self.assertRaises(ValueError, format_day_sec, 0, 0., order='YMD')
        self.assertRaises(ValueError, format_day_sec, 0, 0., kind='X')
        self.assertRaises(ValueError, format_day_sec, 0, 0.,
                                                      buffer=np.empty((3,), dtype='int'))
        self.assertRaises(ValueError, format_day_sec, [[0,0],[0,0]], 0.,
                                                      buffer=np.empty((3,3), dtype='U40'))

##########################################################################################
