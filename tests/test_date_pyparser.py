##########################################################################################
# julian/test_date_pyparser.py
##########################################################################################

import numbers

import pytest
from pyparsing import ParseException, StringEnd

from julian.date_pyparser import date_pyparser
from tests._helpers import confirm_failure, confirm_success


##########################################################################################
# Helper test functions
##########################################################################################

def iso_date_tester(parser, *, doy=False, floating=False, extended=False,
                    padding=False, embedded=False, failure=False):

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
                confirm_failure(parser, test, msg=msg % 'FAILURE')
            else:
                confirm_success(parser, test, msg=msg % 'SUCCESS',
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
                confirm_failure(parser, test, msg=msg % 'FAILURE')
            else:
                confirm_success(parser, test, msg=msg % 'SUCCESS',
                                values=[('YEAR', yval), ('DAY', dval)])


def yd_tester(parser_loose, parser_strict, *, floating=False, extended=False,
              padding=False, embedded=False, failure=False):

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
                confirm_success(p, test, msg=msg % (count, 'SUCCESS', strict),
                                values=[('YEAR', yval), ('DAY', dval)])

            for p in failure_parsers:
                count += 1
                strict = 'True' if p is parser_strict else 'False'
                confirm_failure(p, test, msg=msg % (count, 'FAILURE', strict))

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
            assert False, type(e).__name__ + ' on ' + repr(test) + ': ' + str(e)
        else:
            parse_dict = {pair[0]:pair[1] for pair in pairs}
            assert parse_dict['YEAR'] == y, msg
            assert parse_dict['DAY'] == d, msg


def date_tester(parser_loose, parser_strict, order, *, weekdays=False,
                floating=False, extended=False,
                padding=False, embedded=False, failure=False,
                _fmt_range=None, _skip_extras=False):
    """Test date parsing with given parameters.

    _fmt_range: if set, only test these format indices (0=YMD, 1=MDY, 2=DMY)
    _skip_extras: if True, skip compressed and ordering tests
    """

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

    PUNC = {
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

          all_fmts = [(0, f'{yword}%s{mword}%s{dword}'),
                      (1, f'{mword}%s{dword}%s{yword}'),
                      (2, f'{dword}%s{mword}%s{yword}')]

          if _fmt_range is not None:
              fmts = [all_fmts[i] for i in _fmt_range]
          else:
              fmts = all_fmts

          for fk, fmt in fmts:
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

              if punc == ' ' and mword.isnumeric():
                status += 1

              for weekday in WEEKDAYS:
                if punc == '.' and '.' in dword:
                    continue

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

                    parse_dict = confirm_success(p, test, msg=msg,
                                                 values=[('YEAR', yval)])
                    if dval == 1 and mword in ('02', '12'):
                        assert parse_dict['MONTH'] in (dval, mval), msg
                        assert parse_dict['DAY'] in (dval, mval), msg
                    else:
                        assert parse_dict['MONTH'] == mval, msg
                        assert parse_dict['DAY'] == dval, msg

                for p in failure_parsers:
                    count += 1
                    msg = (f'**** {order} PYPARSER test {count} expected FAILURE: '
                           f'"{test}"; strict={p is parser_strict}, '
                           f'weekdays={weekdays}, floating={floating}, '
                           f'extended={extended}, '
                           f'padding={padding}, embedded={embedded}')

                    confirm_failure(p, test, msg=msg)

    if _skip_extras:
        return

    # Compressed
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
            assert False, type(e).__name__ + ' on ' + repr(test) + ': ' + str(e)
        else:
            parse_dict = {pair[0]:pair[1] for pair in pairs}
            assert parse_dict['YEAR'] == y
            assert parse_dict['MONTH'] == m
            assert parse_dict['DAY'] == d

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
                    assert False, (type(e).__name__ + ' on ' + repr(test)
                                   + ': ' + str(e))
                else:
                    parse_dict = {pair[0]:pair[1] for pair in pairs}
                    assert parse_dict['YEAR'] == y
                    assert parse_dict['MONTH'] == m
                    assert parse_dict['DAY'] == d


def _make_date_parsers(order, doy, weekdays, floating):
    parsers = []
    for strict in (False, True):
        parser = date_pyparser(order, strict=strict, doy=doy,
                               weekdays=weekdays, floating=floating,
                               extended=True, padding=True, embedded=True)
        parsers.append(parser)
    return parsers


##########################################################################################
# Simple unit tests
##########################################################################################

def test_year():

    from julian.date_pyparser import year, year_strict

    ################################
    # year_strict
    ################################

    p = year_strict

    # Success
    assert p.parse_string('1000')[0][0] == 'YEAR'
    assert p.parse_string('1000')[0][1] == 1000
    assert p.parse_string('2000')[0][1] == 2000
    assert p.parse_string('2000a ')[0][1] == 2000
    assert p.parse_string('20000 ')[0][1] == 2000
    assert p.parse_string('17760704')[0][1] == 1776

    # Failure
    with pytest.raises(ParseException): p.parse_string('00')
    with pytest.raises(ParseException): p.parse_string('50')
    with pytest.raises(ParseException): p.parse_string('3000')
    with pytest.raises(ParseException): p.parse_string('0300')
    with pytest.raises(ParseException): p.parse_string(' 2000')
    with pytest.raises(ParseException): p.parse_string('   00')
    with pytest.raises(ParseException): p.parse_string(' ')
    with pytest.raises(ParseException): p.parse_string('a')
    with pytest.raises(ParseException): p.parse_string('0')
    with pytest.raises(ParseException): p.parse_string('000')

    ################################
    # year
    ################################

    p = year

    # Success
    assert p.parse_string('1000')[0][0] == 'YEAR'
    assert p.parse_string('1000')[0][1] == 1000
    assert p.parse_string('2000')[0][1] == 2000
    assert p.parse_string('00')[0][1] == 2000
    assert p.parse_string('50')[0][1] == 1950
    assert p.parse_string('49')[0][1] == 2049
    assert p.parse_string('2000a ')[0][1] == 2000
    assert p.parse_string('20000 ')[0][1] == 2000
    assert p.parse_string('17760704')[0][1] == 1776
    assert p.parse_string('3000')[0][1] == 3000
    assert p.parse_string('0300')[0][1] == 300
    assert p.parse_string('0000')[0][1] == 0
    assert p.parse_string('100')[0][1] == 2010

    # Failure
    with pytest.raises(ParseException): p.parse_string(' 300')
    with pytest.raises(ParseException): p.parse_string('  30')
    with pytest.raises(ParseException): p.parse_string(' 2000')
    with pytest.raises(ParseException): p.parse_string(' ')
    with pytest.raises(ParseException): p.parse_string('a')
    with pytest.raises(ParseException): p.parse_string('0')


def test_month():

    from julian.date_pyparser import month_2digit, numeric_month, month, month_strict

    NAMES = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL','MAY', 'JUNE',
             'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

    ################################
    # month_2digit
    ################################

    p = month_2digit + StringEnd()

    assert p.parse_string('01').as_list()[0][0] == 'MONTH'

    for m in range(1, 13):
        tests = ['%02d' % m]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == m

    for m in range(1, 9):
        tests = [str(m), ' ' + str(m), '0' + str(m) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for m in range(10, 13):
        tests = [' ' + str(m), '0' + str(m), str(m) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('0')
    with pytest.raises(ParseException): p.parse_string(' 0')
    with pytest.raises(ParseException): p.parse_string('13')
    with pytest.raises(ParseException): p.parse_string('00')
    with pytest.raises(ParseException): p.parse_string(' 01')
    with pytest.raises(ParseException): p.parse_string('001')

    ################################
    # numeric_month
    ################################

    p = numeric_month
    pp = p + StringEnd()

    assert p.parse_string('01').as_list()[0][0] == 'MONTH'

    for m in range(1, 13):
        tests = [str(m), '%2d' % m, '%02d' % m, str(m) + 'x', '%2dx' % m, '%02dx' % m]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == m

    for m in range(1, 9):
        tests = [' ' + str(m) + '1', '0' + str(m) + '1']
        for test in tests:
            with pytest.raises(ParseException): pp.parse_string(test)

    with pytest.raises(ParseException): pp.parse_string('0')
    with pytest.raises(ParseException): pp.parse_string(' 0')
    with pytest.raises(ParseException): pp.parse_string('13')
    with pytest.raises(ParseException): pp.parse_string('00')
    with pytest.raises(ParseException): pp.parse_string(' 01')
    with pytest.raises(ParseException): pp.parse_string('001')

    ################################
    # month
    ################################

    p = month
    pp = p + StringEnd()

    assert p.parse_string('JAN').as_list()[0][0] == 'MONTH'

    for m in range(1, 13):
        tests = [str(m), '%2d'%m, '%02d'%m, str(m) + 'x', '%2dx'%m, '%02dx'%m,
                 NAMES[m-1], NAMES[m-1].lower(), NAMES[m-1].capitalize(),
                 NAMES[m-1][:3], NAMES[m-1][:3].capitalize(),
                 NAMES[m-1][:3] + '.', NAMES[m-1][:3].capitalize() + '.',
                 NAMES[m-1] + ',', NAMES[m-1][:3] + '.x', NAMES[m-1][:3] + '.1']
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == m

    for m in range(1, 9):
        tests = [' ' + str(m) + '1', '0' + str(m) + '1',
                 NAMES[m-1] + 'x', NAMES[m-1][:3] + 'x']
        for test in tests:
            with pytest.raises(ParseException): pp.parse_string(test)

    with pytest.raises(ParseException): pp.parse_string('xxx')
    with pytest.raises(ParseException): pp.parse_string('JANU')
    with pytest.raises(ParseException): pp.parse_string(' 0')
    with pytest.raises(ParseException): pp.parse_string('13')
    with pytest.raises(ParseException): pp.parse_string('00')
    with pytest.raises(ParseException): pp.parse_string(' 01')
    with pytest.raises(ParseException): pp.parse_string('001')

    ################################
    # month_strict
    ################################

    p = month_strict

    assert p.parse_string('JAN').as_list()[0][0] == 'MONTH'

    for m in range(1, 13):
        tests = [NAMES[m-1], NAMES[m-1].lower(), NAMES[m-1].capitalize(),
                 NAMES[m-1][:3], NAMES[m-1][:3].capitalize(),
                 NAMES[m-1][:3] + '.', NAMES[m-1][:3].capitalize() + '.',
                 NAMES[m-1] + ',', NAMES[m-1][:3] + '.x', NAMES[m-1][:3] + '.1']
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == m

    for m in range(1, 9):
        tests = [str(m), '%2d'%m, '%02d'%m, str(m) + 'x', '%2dx'%m, '%02dx'%m,
                 ' ' + str(m) + '1', '0' + str(m) + '1',
                 NAMES[m-1] + 'x', NAMES[m-1][:3] + 'x']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('xxx')
    with pytest.raises(ParseException): p.parse_string('JANU')
    with pytest.raises(ParseException): p.parse_string(' 0')
    with pytest.raises(ParseException): p.parse_string('13')
    with pytest.raises(ParseException): p.parse_string('00')
    with pytest.raises(ParseException): p.parse_string(' 01')
    with pytest.raises(ParseException): p.parse_string('001')


def test_date():

    from julian.date_pyparser import date, date_2digit, date_float

    ################################
    # date_2digit
    ################################

    p = date_2digit

    assert p.parse_string('01').as_list()[0][0] == 'DAY'

    for d in range(1, 32):
        tests = ['%02d' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

    for d in range(1, 9):
        tests = [str(d), ' ' + str(d), '0' + str(d) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(10, 32):
        tests = [' ' + str(d), '0' + str(d), str(d) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('0')
    with pytest.raises(ParseException): p.parse_string(' 0')
    with pytest.raises(ParseException): p.parse_string('32')
    with pytest.raises(ParseException): p.parse_string('00')
    with pytest.raises(ParseException): p.parse_string(' 01')
    with pytest.raises(ParseException): p.parse_string('001')

    ################################
    # date
    ################################

    p = date

    assert p.parse_string('01').as_list()[0][0] == 'DAY'

    for d in range(1, 32):
        tests = [str(d), '%2d' % d, '%02d' % d, str(d) + 'a', '%2dx' % d, '%02dx' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

    for d in range(1, 9):
        tests = [' ' + str(d) + '1', '0' + str(d) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(10, 32):
        tests = [str(d) + '1', '0' + str(d) + '1']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('0')
    with pytest.raises(ParseException): p.parse_string(' 0')
    with pytest.raises(ParseException): p.parse_string('32')
    with pytest.raises(ParseException): p.parse_string('00')
    with pytest.raises(ParseException): p.parse_string(' 01')
    with pytest.raises(ParseException): p.parse_string('001')

    ################################
    # date_float
    ################################

    p = date_float

    assert p.parse_string('01.').as_list()[0][0] == 'DAY'
    assert not isinstance(p.parse_string('01.').as_list()[0][1], numbers.Integral)

    for d in range(1, 32):
        tests = [str(d) + '.', '%2d.' % d, '%02d.' % d, '%2d.x' % d, '%02d.x' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

        tests = [str(d)+'.5', '%2d.5' % d, '%02d.5' % d, '%2d.5x' % d, '%02d.5x' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d + 0.5

    for d in range(1, 9):
        tests = [' ' + str(d) + '1.', ' ' + str(d) + '1.', '0' + str(d) + '1.']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(10, 32):
        tests = [str(d) + '1.', '0' + str(d) + '1.']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('0.')
    with pytest.raises(ParseException): p.parse_string(' 0.')
    with pytest.raises(ParseException): p.parse_string('32.')
    with pytest.raises(ParseException): p.parse_string('00.')
    with pytest.raises(ParseException): p.parse_string(' 01.')
    with pytest.raises(ParseException): p.parse_string('001.')


def test_doy():

    from julian.date_pyparser import doy, doy_3digit, doy_float, doy_3digit_float

    ################################
    # doy_3digit
    ################################

    p = doy_3digit

    assert p.parse_string('001').as_list()[0][0] == 'DAY'

    for d in range(1, 367):
        tests = ['%03d' % d, '%03dx' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

    for d in range(1, 100):
        tests = [str(d), '%2d'%d, '%3d'%d, '%02d'%d]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(100, 367):
        tests = [str(d) + '1', ' ' + str(d), '0' + str(d)]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('000')
    with pytest.raises(ParseException): p.parse_string('367')

    ################################
    # doy_3digit_float
    ################################

    p = doy_3digit_float

    assert p.parse_string('001.').as_list()[0][0] == 'DAY'
    assert not isinstance(p.parse_string('001.').as_list()[0][1], numbers.Integral)

    for d in range(1, 367):
        tests = ['%03d.' % d, '%03d.x' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

        tests = ['%03d.5' % d, '%03d.5x' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d + 0.5

    for d in range(1, 100):
        tests = [str(d) + '.', '%2d.'%d, '%3d.'%d, '%02d.'%d]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(100, 367):
        tests = [str(d) + '1.', ' ' + str(d) + '.', '0' + str(d) + '.']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('000.')
    with pytest.raises(ParseException): p.parse_string('367.')

    ################################
    # doy
    ################################

    p = doy

    assert p.parse_string('001').as_list()[0][0] == 'DAY'

    for d in range(1, 367):
        tests = [str(d), '%3d' % d, '%03d' % d, '%3dx' % d, '%03dx' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

    for d in range(1, 10):
        tests = ['%2d' % d, '%02d' % d]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(100, 367):
        tests = [str(d) + '1', ' ' + str(d), '0' + str(d)]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('000')
    with pytest.raises(ParseException): p.parse_string('367')

    ################################
    # doy_float
    ################################

    p = doy_float

    assert p.parse_string('001.').as_list()[0][0] == 'DAY'
    assert not isinstance(p.parse_string('001.').as_list()[0][1], numbers.Integral)

    for d in range(1, 367):
        tests = [str(d) + '.', '%3d.' % d, '%03d.' % d, '%3d.x' % d, '%03d.x' % d]
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == d

    for d in range(1, 10):
        tests = ['%2d.' % d, '%02d.' % d]
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    for d in range(100, 367):
        tests = [str(d) + '1.', ' ' + str(d) + '.', '0' + str(d) + '.']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)

    with pytest.raises(ParseException): p.parse_string('000.')
    with pytest.raises(ParseException): p.parse_string('367.')


def test_weekday():

    from julian.date_pyparser import weekday

    NAMES = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY',
             'SATURDAY']

    p = weekday
    assert p.parse_string('SuN').as_list()[0][0] == 'WEEKDAY'

    for name in NAMES:
        tests = [name, name.lower(), name.capitalize(),
                 name[:3], name[:3].capitalize(),
                 name[:3] + '.', name[:3].capitalize() + '.',
                 name + ',', name[:3] + '.x', name[:3] + '.1']
        for test in tests:
            assert p.parse_string(test).as_list()[0][1] == name[:3]

    for name in NAMES:
        tests = [' ' + name, name + 'x', name[:4], name[:3] + 'x']
        for test in tests:
            with pytest.raises(ParseException): p.parse_string(test)


##########################################################################################
# Parametrized tests for ISO_DATE_PYPARSERS
##########################################################################################

@pytest.mark.parametrize('extended,floating,doy_flag', [
    (ext, flt, d)
    for ext in (0, 1) for flt in (0, 1) for d in (0, 1)
])
def test_ISO_DATE_PYPARSERS(extended, floating, doy_flag):
    from julian.date_pyparser import ISO_DATE_PYPARSERS
    iso_date_tester(ISO_DATE_PYPARSERS[extended, floating, doy_flag],
                    doy=bool(doy_flag), floating=bool(floating),
                    extended=bool(extended))


##########################################################################################
# Parametrized tests for YD_PYPARSERS
##########################################################################################

@pytest.mark.parametrize('floating', [False, True])
def test_YD_PYPARSERS(floating):
    from julian.date_pyparser import YD_PYPARSERS
    yd_tester(YD_PYPARSERS[0, int(floating), 0], YD_PYPARSERS[0, int(floating), 1],
              floating=floating)


##########################################################################################
# Parametrized tests for DATE_PYPARSERS
##########################################################################################

@pytest.mark.parametrize('key,ext,floating', [
    (k, e, f)
    for k in ('YMD', 'MDY', 'DMY') for e in (0, 1) for f in (0, 1)
])
def test_DATE_PYPARSERS(key, ext, floating):
    from julian.date_pyparser import DATE_PYPARSERS
    date_tester(DATE_PYPARSERS[key][ext, floating, 0] + StringEnd(),
                DATE_PYPARSERS[key][ext, floating, 1] + StringEnd(),
                order=key, weekdays=False, floating=bool(floating),
                extended=bool(ext))


##########################################################################################
# Parametrized tests for date_pyparser (main) - no weekdays
##########################################################################################

@pytest.mark.parametrize('floating,order,doy', [
    (False, 'YMD', False), (False, 'DMY', True),
    (True,  'YMD', False), (True,  'DMY', True),
])
def test_date_pyparser_dates(floating, order, doy):
    parsers = _make_date_parsers(order, doy, weekdays=False, floating=floating)
    date_tester(parsers[0], parsers[1], order=order,
                weekdays=False, floating=floating,
                extended=True, padding=True, embedded=True)
    if doy:
        yd_tester(parsers[0], parsers[1], floating=floating,
                  extended=True, padding=True, embedded=True)


##########################################################################################
# Parametrized tests for date_pyparser (main) - with weekdays, split by fmt_idx
##########################################################################################

@pytest.mark.parametrize('floating,order,doy,fmt_idx', [
    (fl, o, d, fi)
    for fl in (False, True) for o, d in [('YMD', False), ('DMY', True)]
    for fi in (0, 1, 2)
])
def test_date_pyparser_dates_weekdays(floating, order, doy, fmt_idx):
    parsers = _make_date_parsers(order, doy, weekdays=True, floating=floating)
    date_tester(parsers[0], parsers[1], order=order,
                weekdays=True, floating=floating,
                extended=True, padding=True, embedded=True,
                _fmt_range=[fmt_idx], _skip_extras=True)


@pytest.mark.parametrize('floating,order,doy', [
    (fl, o, d)
    for fl in (False, True) for o, d in [('YMD', False), ('DMY', True)]
])
def test_date_pyparser_dates_weekdays_extras(floating, order, doy):
    parsers = _make_date_parsers(order, doy, weekdays=True, floating=floating)
    date_tester(parsers[0], parsers[1], order=order,
                weekdays=True, floating=floating,
                extended=True, padding=True, embedded=True,
                _fmt_range=[], _skip_extras=False)
    if doy:
        yd_tester(parsers[0], parsers[1], floating=floating,
                  extended=True, padding=True, embedded=True)


##########################################################################################
# Parametrized tests for date_pyparser - quick tests (padding != embedded)
##########################################################################################

@pytest.mark.parametrize('padding', [True, False])
def test_date_pyparser_dates_quick(padding):
    parser_loose = date_pyparser(order='YMD', strict=False, doy=False,
                                 weekdays=False, floating=False,
                                 padding=padding, embedded=(not padding))
    parser_strict = date_pyparser(order='YMD', strict=True, doy=False,
                                  weekdays=False, floating=False,
                                  padding=padding, embedded=(not padding))
    date_tester(parser_loose, parser_strict, order='YMD',
                weekdays=False, floating=False,
                padding=padding, embedded=(not padding))

    parser_loose = date_pyparser(order='YMD', strict=False, doy=True,
                                 weekdays=False, floating=False,
                                 padding=padding, embedded=(not padding))
    parser_strict = date_pyparser(order='YMD', strict=True, doy=True,
                                  weekdays=False, floating=False,
                                  padding=padding, embedded=(not padding))
    yd_tester(parser_loose, parser_strict,
              padding=padding, embedded=(not padding))


##########################################################################################
# test_date_pyparser_mjd
##########################################################################################

@pytest.mark.parametrize('floating', [False, True])
def test_date_pyparser_mjd(floating):
    from tests.test_mjd_pyparser import mjd_tester

    parser = date_pyparser(mjd=True, floating=floating, padding=True, embedded=True)
    mjd_tester(parser, floating=floating, timesys=floating,
               padding=True, embedded=True)


##########################################################################################
# Parametrized tests for date_pyparser iso_only
##########################################################################################

@pytest.mark.parametrize('floating,doy,extended', [
    (fl, d, e)
    for fl in (False, True) for d in (False, True) for e in (False, True)
])
def test_date_pyparser_iso_only(floating, doy, extended):
    parser = date_pyparser(iso_only=True, doy=doy, floating=floating,
                           extended=extended, padding=True, embedded=True)
    iso_date_tester(parser, doy=doy, floating=floating,
                    extended=extended, padding=True, embedded=True)


##########################################################################################
