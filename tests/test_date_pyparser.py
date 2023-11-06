##########################################################################################
# julian/test_date_pyparser.py
##########################################################################################

import numbers
import unittest
import warnings

from pyparsing import ParseException, StringEnd

from julian.date_pyparser import date_pyparser
from julian.mjd_pyparser  import mjd_pyparser


class Test_date_pyparser(unittest.TestCase):

    def _confirm_failure(self, parser, test, msg):

        try:
            pairs = parser.parse_string(test).as_list()

        except ParseException:                      # correct exception; proceed
            self.assertRaises(ParseException, parser.parse_string, test)

        except Exception as e:  # pragma: no cover  # wrong exception; warn and proceed
            warnings.warn(msg + f'; Incorrect exception {type(e)}: {e}')
            self.assertRaises(Exception, parser.parse_string, test)

        else:
            # It could be that the reason this was not an exception is that a partial
            # match did succeed. This is a valid outcome.
            parse_dict = {pair[0]:pair[1] for pair in pairs}
            msg += f'; {parse_dict}'    # add diagnostic info to the message
            remainder = test[parse_dict['~']:].lstrip()
            self.assertNotIn(remainder, ('', 'xxx'), msg=msg)

    def _confirm_success(self, parser, test, msg, values=[]):

        error = None
        try:
            pairs = parser.parse_string(test).as_list()
        except Exception as e:  # pragma: no cover
            error = e

        # Print the error info and then the message
        self.assertIsNone(error, msg)

        parse_dict = {pair[0]:pair[1] for pair in pairs}
        msg += f'; {parse_dict}'

        for name, value in values:
            self.assertIn(name, parse_dict, msg=msg)
            self.assertEqual(parse_dict[name], value, msg=msg)

        remainder = test[parse_dict['~']:].lstrip()
        self.assertIn(remainder, ('', 'xxx'), msg=msg)

        return parse_dict

    ####################################################################
    # year
    ####################################################################

    def test_year(self):

        from julian.date_pyparser import year, year_strict

        ################################
        # year_strict
        ################################

        p = year_strict

        # Success
        self.assertEqual(p.parse_string('1000')[0][0], 'YEAR')
        self.assertEqual(p.parse_string('1000')[0][1], 1000)
        self.assertEqual(p.parse_string('2000')[0][1], 2000)
        self.assertEqual(p.parse_string('2000a ')[0][1], 2000)
        self.assertEqual(p.parse_string('20000 ')[0][1], 2000)
        self.assertEqual(p.parse_string('17760704')[0][1], 1776)

        # Failure
        self.assertRaises(ParseException, p.parse_string, '00')
        self.assertRaises(ParseException, p.parse_string, '50')
        self.assertRaises(ParseException, p.parse_string, '3000')
        self.assertRaises(ParseException, p.parse_string, '0300')
        self.assertRaises(ParseException, p.parse_string, ' 2000')
        self.assertRaises(ParseException, p.parse_string, '   00')
        self.assertRaises(ParseException, p.parse_string, ' ')
        self.assertRaises(ParseException, p.parse_string, 'a')
        self.assertRaises(ParseException, p.parse_string, '0')
        self.assertRaises(ParseException, p.parse_string, '000')

        ################################
        # year
        ################################

        p = year

        # Success
        self.assertEqual(p.parse_string('1000')[0][0], 'YEAR')
        self.assertEqual(p.parse_string('1000')[0][1], 1000)
        self.assertEqual(p.parse_string('2000')[0][1], 2000)
        self.assertEqual(p.parse_string('00')[0][1],   2000)
        self.assertEqual(p.parse_string('50')[0][1],   1950)
        self.assertEqual(p.parse_string('49')[0][1],   2049)
        self.assertEqual(p.parse_string('2000a ')[0][1], 2000)
        self.assertEqual(p.parse_string('20000 ')[0][1], 2000)
        self.assertEqual(p.parse_string('17760704')[0][1], 1776)
        self.assertEqual(p.parse_string('3000')[0][1], 3000)
        self.assertEqual(p.parse_string('0300')[0][1],  300)
        self.assertEqual(p.parse_string('0000')[0][1],    0)
        self.assertEqual(p.parse_string('100')[0][1],  2010)

        # Failure
        self.assertRaises(ParseException, p.parse_string, ' 300')
        self.assertRaises(ParseException, p.parse_string, '  30')
        self.assertRaises(ParseException, p.parse_string, ' 2000')
        self.assertRaises(ParseException, p.parse_string, ' ')
        self.assertRaises(ParseException, p.parse_string, 'a')
        self.assertRaises(ParseException, p.parse_string, '0')

    ####################################################################
    # month
    ####################################################################

    def test_month(self):

        from julian.date_pyparser import month_2digit, numeric_month, month, month_strict

        NAMES = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL','MAY', 'JUNE',
                 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

        ################################
        # month_2digit
        ################################

        p = month_2digit + StringEnd()

        self.assertEqual(p.parse_string('01').as_list()[0][0], 'MONTH')

        # Success
        for m in range(1, 13):
            tests = ['%02d' % m]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], m)

        # Failure
        for m in range(1, 9):
            tests = [str(m), ' ' + str(m), '0' + str(m) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for m in range(10, 13):
            tests = [' ' + str(m), '0' + str(m), str(m) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '0')
        self.assertRaises(ParseException, p.parse_string, ' 0')
        self.assertRaises(ParseException, p.parse_string, '13')
        self.assertRaises(ParseException, p.parse_string, '00')
        self.assertRaises(ParseException, p.parse_string, ' 01')
        self.assertRaises(ParseException, p.parse_string, '001')

        ################################
        # numeric_month
        ################################

        p = numeric_month
        pp = p + StringEnd()

        self.assertEqual(p.parse_string('01').as_list()[0][0], 'MONTH')

        # Success
        for m in range(1, 13):
            tests = [str(m), '%2d' % m, '%02d' % m, str(m) + 'x', '%2dx' % m, '%02dx' % m]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], m)

        # Failure
        for m in range(1, 9):
            tests = [' ' + str(m) + '1', '0' + str(m) + '1']
            for test in tests:
                self.assertRaises(ParseException, pp.parse_string, test)

        self.assertRaises(ParseException, pp.parse_string, '0')
        self.assertRaises(ParseException, pp.parse_string, ' 0')
        self.assertRaises(ParseException, pp.parse_string, '13')
        self.assertRaises(ParseException, pp.parse_string, '00')
        self.assertRaises(ParseException, pp.parse_string, ' 01')
        self.assertRaises(ParseException, pp.parse_string, '001')

        ################################
        # month
        ################################

        p = month
        pp = p + StringEnd()

        self.assertEqual(p.parse_string('JAN').as_list()[0][0], 'MONTH')

        # Success
        for m in range(1, 13):
            tests = [str(m), '%2d'%m, '%02d'%m, str(m) + 'x', '%2dx'%m, '%02dx'%m,
                     NAMES[m-1], NAMES[m-1].lower(), NAMES[m-1].capitalize(),
                     NAMES[m-1][:3], NAMES[m-1][:3].capitalize(),
                     NAMES[m-1][:3] + '.', NAMES[m-1][:3].capitalize() + '.',
                     NAMES[m-1] + ',', NAMES[m-1][:3] + '.x', NAMES[m-1][:3] + '.1']
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], m)

        # Failure
        for m in range(1, 9):
            tests = [' ' + str(m) + '1', '0' + str(m) + '1',
                     NAMES[m-1] + 'x', NAMES[m-1][:3] + 'x']
            for test in tests:
                self.assertRaises(ParseException, pp.parse_string, test)

        self.assertRaises(ParseException, pp.parse_string, 'xxx')
        self.assertRaises(ParseException, pp.parse_string, 'JANU')
        self.assertRaises(ParseException, pp.parse_string, ' 0')
        self.assertRaises(ParseException, pp.parse_string, '13')
        self.assertRaises(ParseException, pp.parse_string, '00')
        self.assertRaises(ParseException, pp.parse_string, ' 01')
        self.assertRaises(ParseException, pp.parse_string, '001')

        ################################
        # month_strict
        ################################

        p = month_strict

        self.assertEqual(p.parse_string('JAN').as_list()[0][0], 'MONTH')

        # Success
        for m in range(1, 13):
            tests = [NAMES[m-1], NAMES[m-1].lower(), NAMES[m-1].capitalize(),
                     NAMES[m-1][:3], NAMES[m-1][:3].capitalize(),
                     NAMES[m-1][:3] + '.', NAMES[m-1][:3].capitalize() + '.',
                     NAMES[m-1] + ',', NAMES[m-1][:3] + '.x', NAMES[m-1][:3] + '.1']
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], m)

        # Failure
        for m in range(1, 9):
            tests = [str(m), '%2d'%m, '%02d'%m, str(m) + 'x', '%2dx'%m, '%02dx'%m,
                     ' ' + str(m) + '1', '0' + str(m) + '1',
                     NAMES[m-1] + 'x', NAMES[m-1][:3] + 'x']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, 'xxx')
        self.assertRaises(ParseException, p.parse_string, 'JANU')
        self.assertRaises(ParseException, p.parse_string, ' 0')
        self.assertRaises(ParseException, p.parse_string, '13')
        self.assertRaises(ParseException, p.parse_string, '00')
        self.assertRaises(ParseException, p.parse_string, ' 01')
        self.assertRaises(ParseException, p.parse_string, '001')

    ####################################################################
    # date
    ####################################################################

    def test_date(self):

        from julian.date_pyparser import date, date_2digit, date_float

        ################################
        # date_2digit
        ################################

        p = date_2digit

        self.assertEqual(p.parse_string('01').as_list()[0][0], 'DAY')

        # Success
        for d in range(1, 32):
            tests = ['%02d' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

        # Failure
        for d in range(1, 9):
            tests = [str(d), ' ' + str(d), '0' + str(d) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(10, 32):
            tests = [' ' + str(d), '0' + str(d), str(d) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '0')
        self.assertRaises(ParseException, p.parse_string, ' 0')
        self.assertRaises(ParseException, p.parse_string, '32')
        self.assertRaises(ParseException, p.parse_string, '00')
        self.assertRaises(ParseException, p.parse_string, ' 01')
        self.assertRaises(ParseException, p.parse_string, '001')

        ################################
        # date
        ################################

        p = date

        self.assertEqual(p.parse_string('01').as_list()[0][0], 'DAY')

        # Success
        for d in range(1, 32):
            tests = [str(d), '%2d' % d, '%02d' % d, str(d) + 'a', '%2dx' % d, '%02dx' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

        # Failure
        for d in range(1, 9):
            tests = [' ' + str(d) + '1', '0' + str(d) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(10, 32):
            tests = [str(d) + '1', '0' + str(d) + '1']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '0')
        self.assertRaises(ParseException, p.parse_string, ' 0')
        self.assertRaises(ParseException, p.parse_string, '32')
        self.assertRaises(ParseException, p.parse_string, '00')
        self.assertRaises(ParseException, p.parse_string, ' 01')
        self.assertRaises(ParseException, p.parse_string, '001')

        ################################
        # date_float
        ################################

        p = date_float

        self.assertEqual(p.parse_string('01.').as_list()[0][0], 'DAY')
        self.assertFalse(isinstance(p.parse_string('01.').as_list()[0][1],
                                    numbers.Integral))

        # Success
        for d in range(1, 32):
            tests = [str(d) + '.', '%2d.' % d, '%02d.' % d, '%2d.x' % d, '%02d.x' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

            tests = [str(d)+'.5', '%2d.5' % d, '%02d.5' % d, '%2d.5x' % d, '%02d.5x' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d + 0.5)

        # Failure
        for d in range(1, 9):
            tests = [' ' + str(d) + '1.', ' ' + str(d) + '1.', '0' + str(d) + '1.']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(10, 32):
            tests = [str(d) + '1.', '0' + str(d) + '1.']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '0.')
        self.assertRaises(ParseException, p.parse_string, ' 0.')
        self.assertRaises(ParseException, p.parse_string, '32.')
        self.assertRaises(ParseException, p.parse_string, '00.')
        self.assertRaises(ParseException, p.parse_string, ' 01.')
        self.assertRaises(ParseException, p.parse_string, '001.')

    ####################################################################
    # doy
    ####################################################################

    def test_doy(self):

        from julian.date_pyparser import doy, doy_3digit, doy_float, doy_3digit_float

        ################################
        # doy_3digit
        ################################

        p = doy_3digit

        self.assertEqual(p.parse_string('001').as_list()[0][0], 'DAY')

        # Success
        for d in range(1, 367):
            tests = ['%03d' % d, '%03dx' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

        # Failure
        for d in range(1, 100):
            tests = [str(d), '%2d'%d, '%3d'%d, '%02d'%d]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(100, 367):
            tests = [str(d) + '1', ' ' + str(d), '0' + str(d)]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '000')
        self.assertRaises(ParseException, p.parse_string, '367')

        ################################
        # doy_3digit_float
        ################################

        p = doy_3digit_float

        self.assertEqual(p.parse_string('001.').as_list()[0][0], 'DAY')
        self.assertFalse(isinstance(p.parse_string('001.').as_list()[0][1],
                                    numbers.Integral))

        # Success
        for d in range(1, 367):
            tests = ['%03d.' % d, '%03d.x' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

            tests = ['%03d.5' % d, '%03d.5x' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d + 0.5)

        # Failure
        for d in range(1, 100):
            tests = [str(d) + '.', '%2d.'%d, '%3d.'%d, '%02d.'%d]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(100, 367):
            tests = [str(d) + '1.', ' ' + str(d) + '.', '0' + str(d) + '.']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '000.')
        self.assertRaises(ParseException, p.parse_string, '367.')

        ################################
        # doy
        ################################

        p = doy

        self.assertEqual(p.parse_string('001').as_list()[0][0], 'DAY')

        # Success
        for d in range(1, 367):
            tests = [str(d), '%3d' % d, '%03d' % d, '%3dx' % d, '%03dx' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

        # Failure
        for d in range(1, 10):
            tests = ['%2d' % d, '%02d' % d]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(100, 367):
            tests = [str(d) + '1', ' ' + str(d), '0' + str(d)]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '000')
        self.assertRaises(ParseException, p.parse_string, '367')

        ################################
        # doy_float
        ################################

        p = doy_float

        self.assertEqual(p.parse_string('001.').as_list()[0][0], 'DAY')
        self.assertFalse(isinstance(p.parse_string('001.').as_list()[0][1],
                                    numbers.Integral))

        # Success
        for d in range(1, 367):
            tests = [str(d) + '.', '%3d.' % d, '%03d.' % d, '%3d.x' % d, '%03d.x' % d]
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], d)

        # Failure
        for d in range(1, 10):
            tests = ['%2d.' % d, '%02d.' % d]
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        for d in range(100, 367):
            tests = [str(d) + '1.', ' ' + str(d) + '.', '0' + str(d) + '.']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

        self.assertRaises(ParseException, p.parse_string, '000.')
        self.assertRaises(ParseException, p.parse_string, '367.')

    ####################################################################
    # weekday
    ####################################################################

    def test_weekday(self):

        from julian.date_pyparser import weekday

        NAMES = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY',
                 'SATURDAY']

        p = weekday
        self.assertEqual(p.parse_string('SuN').as_list()[0][0], 'WEEKDAY')

        # Success
        for name in NAMES:
            tests = [name, name.lower(), name.capitalize(),
                     name[:3], name[:3].capitalize(),
                     name[:3] + '.', name[:3].capitalize() + '.',
                     name + ',', name[:3] + '.x', name[:3] + '.1']
            for test in tests:
                self.assertEqual(p.parse_string(test).as_list()[0][1], name[:3])

        # Failure
        for name in NAMES:
            tests = [' ' + name, name + 'x', name[:4], name[:3] + 'x']
            for test in tests:
                self.assertRaises(ParseException, p.parse_string, test)

    ####################################################################
    # ISO_DATE_PYPARSERS
    ####################################################################

    def test_ISO_DATE_PYPARSERS(self):

        from julian.date_pyparser import ISO_DATE_PYPARSERS

        for extended in (0,1):
          for floating in (0,1):
            for doy in (0,1):
                self.my_iso_date_tester(ISO_DATE_PYPARSERS[extended,floating,doy],
                                        doy=bool(doy), floating=bool(floating),
                                        extended=bool(extended))

    def my_iso_date_tester(self, parser, *, doy=False, floating=False, extended=False,
                                 padding=False, embedded=False, failure=False):

        # 0 = valid; invalid=5
        YEARS = []
        for y in (1900,1999,2000,2099,3000,9999,100,10,1,0):
            YEARS.append((0, '%04d' % y, y))
        for y in (0,49,50,99):
            YEARS.append((0, '%02d' % y, 2000 + y - 100 * (y//50)))

        if extended:
            for ystr in ('+20001', '-20001', '+0010', '-0099'):
                YEARS.append((1, ystr, int(ystr)))
            YEARS.append((9, '+10', 10))

        MONTHS = []
        for m in (1,9,10,12):
            MONTHS.append((0, '%02d' % m, m))
        for m in (1,9):
            MONTHS.append((5, '%2d' % m, m))
        for m in (0,13):
            MONTHS.append((5, '%02d' % m, m))

        DATES = []
        for d in (1,9,10,20,29,30,31):
            DATES.append((0, '%02d' % d, d))
        for d in (1,9):
            DATES.append((5, '%2d' % d, d))
        for d in (0,32,40):
            DATES.append((5, '%02d' % d, d))

        DOYS = []
        for d in (1,9,10,99,100,200,300,359,360,366):
            DOYS.append((0, '%03d' % d, d))
            if d < 100:
                DOYS.append((5, '%3d' % d, d))
        for d in (0, 367, 370, 400):
            DOYS.append((5, '%3d' % d, d))
        DOYS.append((5, '000', 0))

        if floating:
            saved = DATES.copy()
            for dstat, dword, dval in saved:
                DATES.append((dstat, dword + '.5', dval + 0.5))

            saved = DOYS.copy()
            for dstat, dword, dval in saved:
                DOYS.append((dstat, dword + '.5', dval + 0.5))

        if padding:
            before = '  '
            after = '  '
        else:
            before = ''
            after = ''

        if embedded:
            after = ' xxx'

        count = 0
        for sep in ('-', ''):
          for ystat, yword, yval in YEARS:
            for mstat, mword, mval in MONTHS:
              for dstat, dword, dval in DATES:
                test = before + yword + sep + mword + sep + dword + after
                status = ystat + mstat + dstat + (0 if sep else 1)
                expect_failure = status > 1 or failure

                count += 1
                msg = (f'**** ISO PYPARSER test {count} expected %s: "{test}"; '
                       f'doy={doy}, floating={floating}, extended={extended}, '
                       f'padding={padding}, embedded={embedded}')

                if expect_failure:
                    self._confirm_failure(parser, test, msg=msg % 'FAILURE')
                else:
                    self._confirm_success(parser, test, msg=msg % 'SUCCESS',
                                          values=[('YEAR', yval), ('MONTH', mval),
                                                  ('DAY', dval)])

        if doy:
          for sep in ('-', ''):
            for ystat, yword, yval in YEARS:
              for dstat, dword, dval in DOYS:
                test = before + yword + sep + dword + after
                status = ystat + dstat + (0 if sep else 1)
                expect_failure = status > 1 or failure

                count += 1
                msg = (f'**** ISO PYPARSER test {count} expected %s: "{test}"; '
                       f'doy={doy}, floating={floating}, extended={extended}, '
                       f'padding={padding}, embedded={embedded}')

                if expect_failure:
                    self._confirm_failure(parser, test, msg=msg % 'FAILURE')
                else:
                    self._confirm_success(parser, test, msg=msg % 'SUCCESS',
                                          values=[('YEAR', yval), ('DAY', dval)])

    ####################################################################
    # YD_PYPARSERS
    ####################################################################

    def test_YD_PYPARSERS(self):

        from julian.date_pyparser import YD_PYPARSERS

        self.my_yd_tester(YD_PYPARSERS[0,0,0], YD_PYPARSERS[0,0,1], floating=False)
        self.my_yd_tester(YD_PYPARSERS[0,1,0], YD_PYPARSERS[0,1,1], floating=True)


    def my_yd_tester(self, parser_loose, parser_strict, *, floating=False, extended=False,
                           padding=False, embedded=False, failure=False):

        # 0 = strict; 1 = loose; invalid=9
        YEARS = []
        for y in (1900,1999,2000,2099,3000,9999,100,10,1,0):
            YEARS.append((2*(1 - int(1000 <= y <= 2999)), '%04d' % y, y))
        for y in (0,49,50,99):
            YEARS.append((2, '%02d' % y, 2000 + y - 100 * (y//50)))

        if extended:
            for ystr in ('+20001', '-20001', '+0010', '-0099'):
                YEARS.append((1, ystr, int(ystr)))
            YEARS.append((9, '+10', 10))

        DOYS = []
        for d in (1,9,10,99,100,200,300,359,360,366):
            DOYS.append((0, '%03d' % d, d))
            if d < 100:
                DOYS.append((2, str(d), d))
        for d in (0, 367, 370, 400):
            DOYS.append((9, str(d), d))
        DOYS.append((9, '000', 0))

        PUNC = [(0, '/'), (2, ' '), (2, '.')]

        if padding:
            before = '  '
            after = '  '
        else:
            before = ''
            after = ''

        if embedded:
            after = ' xxx'

        count = 0
        for ystat, yword, yval in YEARS:
          for pstat, pword in PUNC:
            for dstat, dword, dval in DOYS:
                test = before + yword + pword + dword + after
                status = ystat + pstat + dstat
                if len(test.split('.')) > 2:    # pragma: no cover
                    status = 9

                if status >= 9 or failure:
                    success_parsers = ()
                    failure_parsers = (parser_loose, parser_strict)
                elif status <= 1:
                    success_parsers = (parser_loose, parser_strict)
                    failure_parsers = ()
                else:
                    success_parsers = (parser_loose,)
                    failure_parsers = (parser_strict,)

                msg = (f'**** YD PYPARSER test %d expected %s: "{test}"; '
                       f'strict=%s, floating={floating}, '
                       f'extended={extended}, '
                       f'padding={padding}, embedded={embedded}')

                for p in success_parsers:
                    count += 1
                    strict = 'True' if p is parser_strict else 'False'
                    self._confirm_success(p, test, msg=msg % (count, 'SUCCESS', strict),
                                          values=[('YEAR', yval), ('DAY', dval)])

                for p in failure_parsers:
                    count += 1
                    strict = 'True' if p is parser_strict else 'False'
                    self._confirm_failure(p, test, msg=msg % (count, 'FAILURE', strict))

        # Compressed
        for case in [('2000001', 2000,   1),
                     ('1999365', 1999, 365),
                     ('0000001',    0,   1),
                     (  '00001', 2000,   1),
                     (  '50100', 1950, 100)]:
            test, y, d = case
            test = before + test + after
            msg = 'Failure on ' + repr(test)
            try:
                pairs = parser_loose.parse_string(test).as_list()
            except Exception as e:      # pragma: no cover
                self.assertTrue(False, type(e).__name__ + ' on ' + repr(test) + ': '
                                       + str(e))
            else:
                parse_dict = {pair[0]:pair[1] for pair in pairs}
                self.assertEqual(parse_dict['YEAR'], y, msg)
                self.assertEqual(parse_dict['DAY'], d, msg)

    ####################################################################
    # DATE_PYPARSERS
    ####################################################################

    def test_DATE_PYPARSERS(self):

        from julian.date_pyparser import DATE_PYPARSERS

        for key in ('YMD', 'MDY', 'DMY'):
          for ext in (0,1):
            for floating in (0,1):
                self.my_date_tester(DATE_PYPARSERS[key][ext,floating,0] + StringEnd(),
                                    DATE_PYPARSERS[key][ext,floating,1] + StringEnd(),
                                    order=key, weekdays=False, floating=bool(floating),
                                    extended=bool(ext))

    def my_date_tester(self, parser_loose, parser_strict, order, *, weekdays=False,
                             floating=False, extended=False,
                             padding=False, embedded=False, failure=False):

        STATUS = {
            True : 'FAILURE',
            False: 'SUCCESS',
        }

        # 0 = strict; 1 = loose; invalid=5
        YEARS  = [(0, '2000', 2000), (0, '3000', 3000),
                  (0, '00', 2000), (0, '49', 2049), (0, '50', 1950),
                  (9, '300', 0)]

        if extended:
            YEARS += [('signed', '+20001', 20001), ('signed', '-0011', -11),
                      ('suffix', '44 BC', -43), ('prefix', 'AD 10', 10)]

        MONTHS = [(0, 'jan', 1), (0, 'DEC.', 12),
                  (0, '02', 2), (0, '12', 12), (0, '1' , 1)]

        DATES  = [(0, '01', 1), (0, '31', 31), (0, '01.5', 1.5),
                  (0, '1', 1), (0, ' 1', 1), (0, '1.5', 1.5),
                  (9, '00', 0), (9, '32', 0)]

        WEEKDAYS = ['', 'MON ', 'TUE. ', 'Thu,', 'fri.,']
        if not weekdays:
            WEEKDAYS = ['']

        PUNC = {        # index is floating = True or False
            False: [(0, '-'), (0, '/'), (0, '.'), (0, ' ')],
            True:  [(0, '-'), (0, '/'), (5, '.'), (0, ' ')],
        }

        if padding:
            before = '  '
            after = '  '
        else:
            before = ''
            after = ''

        if embedded:
            after = ' xxx'

        count = 0
        for ystat_, yword, yval in YEARS:
          for mstat, mword, mval in MONTHS:
            for dstat, dword, dval in DATES:
              has_decimal = '.5' in dword
              if has_decimal and not floating:
                continue

              for fk, fmt in enumerate([f'{yword}%s{mword}%s{dword}',
                                        f'{mword}%s{dword}%s{yword}',
                                        f'{dword}%s{mword}%s{yword}']):
                for pstat, punc in PUNC[has_decimal]:
                  test0 = fmt % (punc, punc)
                  if '..' in test0:
                    continue

                  if ystat_ == 'signed':
                      ystat = 0 if fk == 0 or punc == ' ' else 9
                  elif ystat_ == 'suffix':
                      ystat = 0 if fk > 0 else 9
                  elif ystat_ == 'prefix':
                      ystat = 0 if fk > 0 and punc == ' ' else 9
                  else:
                      ystat = ystat_

                  status = ystat + mstat + dstat + pstat

                  # Cases where the separator is white require a strict month
                  if punc == ' ' and mword.isnumeric():
                    status += 1

                  for weekday in WEEKDAYS:
                    if punc == '.' and '.' in dword:
                        continue                    # no period separators in floats

                    test = before + weekday + test0 + after

                    if status > 4 or failure:
                        success_parsers = ()
                        failure_parsers = (parser_loose, parser_strict)
                    elif status == 0:
                        success_parsers = (parser_loose, parser_strict)
                        failure_parsers = ()
                    else:
                        success_parsers = (parser_loose,)
                        failure_parsers = (parser_strict,)

                    for p in success_parsers:
                        count += 1
                        msg = (f'**** {order} PYPARSER test {count} expected SUCCESS: '
                               f'"{test}"; strict={p is parser_strict}, '
                               f'weekdays={weekdays}, floating={floating}, '
                               f'extended={extended}, '
                               f'padding={padding}, embedded={embedded}')

                        parse_dict = self._confirm_success(p, test, msg=msg,
                                                           values=[('YEAR', yval)])
                        if dval == 1 and mword in ('02', '12'):
                            # Check ambiguous orders below
                            self.assertIn(parse_dict['MONTH'], (dval, mval), msg=msg)
                            self.assertIn(parse_dict['DAY'], (dval, mval), msg=msg)
                        else:
                            self.assertEqual(parse_dict['MONTH'], mval, msg=msg)
                            self.assertEqual(parse_dict['DAY'], dval, msg=msg)

                    for p in failure_parsers:
                        count += 1
                        msg = (f'**** {order} PYPARSER test {count} expected FAILURE: '
                               f'"{test}"; strict={p is parser_strict}, '
                               f'weekdays={weekdays}, floating={floating}, '
                               f'extended={extended}, '
                               f'padding={padding}, embedded={embedded}')

                        self._confirm_failure(p, test, msg=msg)

        # Compressed
        parser = parser_loose
        for case in [('20000101', 2000,  1,  1),
                     ('19991231', 1999, 12, 31),
                     ('00000101',    0,  1,  1),
                     (  '000101', 2000,  1,  1),
                     (  '500630', 1950,  6, 30)]:
            test, y, m, d = case
            test = before + test + after
            try:
                pairs = parser_loose.parse_string(test).as_list()
            except Exception as e:      # pragma: no cover
                self.assertTrue(False, type(e).__name__ + ' on ' + repr(test) + ': '
                                       + str(e))
            else:
                parse_dict = {pair[0]:pair[1] for pair in pairs}
                self.assertEqual(parse_dict['YEAR'], y)
                self.assertEqual(parse_dict['MONTH'], m)
                self.assertEqual(parse_dict['DAY'], d)

        # Ordering
        for case in [('YMD', '05/06/07', 2005, 6,  7),
                     ('MDY', '05/06/07', 2007, 5,  6),
                     ('DMY', '05/06/07', 2007, 6,  5),
                     ('YMD', '05/13/07', 2007, 5, 13),
                     ('MDY', '13/06/07', 2013, 6,  7),
                     ('DMY', '05/13/07', 2007, 5, 13)]:
            key, test, y, m, d = case
            test = before + test + after
            if key == order:
                for p in (parser_loose, parser_strict):
                    try:
                        pairs = p.parse_string(test).as_list()
                    except Exception as e:      # pragma: no cover
                        self.assertTrue(False, type(e).__name__ + ' on ' + repr(test)
                                               + ': ' + str(e))
                    else:
                        parse_dict = {pair[0]:pair[1] for pair in pairs}
                        self.assertEqual(parse_dict['YEAR'], y)
                        self.assertEqual(parse_dict['MONTH'], m)
                        self.assertEqual(parse_dict['DAY'], d)

    ####################################################################
    # date_pyparser function
    ####################################################################

    def test_date_pyparser_dates(self):

        for padding in (True,):
          for embedded in (True,):
            for floating in (False, True):
              for order, doy in [('YMD', False), ('DMY', True)]:
                                            # other combos tested by test_DATE_PYPARSERS
                for weekdays in (False, True):
                    parsers = []
                    for strict in (False, True):
                        parser = date_pyparser(order, strict=strict, doy=doy,
                                               weekdays=weekdays, floating=floating,
                                               extended=True,
                                               padding=padding, embedded=embedded)
                        parsers.append(parser)

                    self.my_date_tester(parsers[0], parsers[1], order=order,
                                        weekdays=weekdays, floating=floating,
                                        extended=True,
                                        padding=padding, embedded=embedded)

                    if doy:
                        self.my_yd_tester(parsers[0], parsers[1], floating=floating,
                                          extended=True,
                                          padding=padding, embedded=embedded)

        # Quick tests with padding != embedded
        for padding in (True, False):
            parser_loose = date_pyparser(order='YMD', strict=False, doy=False,
                                         weekdays=False, floating=False,
                                         padding=padding, embedded=(not padding))
            parser_strict = date_pyparser(order='YMD', strict=True, doy=False,
                                          weekdays=False, floating=False,
                                          padding=padding, embedded=(not padding))
            self.my_date_tester(parser_loose, parser_strict, order='YMD',
                                weekdays=False, floating=False,
                                padding=padding, embedded=(not padding))

            parser_loose = date_pyparser(order='YMD', strict=False, doy=True,
                                         weekdays=False, floating=False,
                                         padding=padding, embedded=(not padding))
            parser_strict = date_pyparser(order='YMD', strict=True, doy=True,
                                          weekdays=False, floating=False,
                                          padding=padding, embedded=(not padding))
            self.my_yd_tester(parser_loose, parser_strict,
                              padding=padding, embedded=(not padding))


    def test_date_pyparser_mjd(self):

        from tests.test_mjd_pyparser import Test_mjd_pyparser

        for padding in (True,):
          for embedded in (True,):
            for floating in (False, True):
              parser = date_pyparser(mjd=True, floating=floating, padding=padding,
                                     embedded=embedded)
              Test_mjd_pyparser.my_mjd_tester(self, parser, floating=floating,
                                              timesys=floating, padding=padding,
                                              embedded=embedded)


    def test_date_pyparser_iso_only(self):

        for padding in (True,):
          for embedded in (True,):
            for floating in (False, True):
              for doy in (False, True):
                for extended in (False, True):
                    parser = date_pyparser(iso_only=True, doy=doy, floating=floating,
                                           extended=extended,
                                           padding=padding, embedded=embedded)

                    self.my_iso_date_tester(parser, doy=doy, floating=floating,
                                            extended=extended,
                                            padding=padding, embedded=embedded)

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
