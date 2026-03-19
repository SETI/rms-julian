##########################################################################################
# tests/test_mjd_pyparser.py
##########################################################################################

from tests._helpers import confirm_failure, confirm_success


def mjd_tester(parser, floating, timesys, padding=False, embedded=False):

    NUMBERS = []
    for n in ['12345', '-12345', '1']:
        NUMBERS.append((0, n, int(n)))
    for n in ['1234.5', '-1.5']:
        NUMBERS.append((0 if floating else 9, n, float(n)))
    NUMBERS.append((9, '1.2.5', 0))

    FMTS = []
    for f in ['MJD %s', '%s  mjd', '%s (MJD)']:
        FMTS.append((0, f, 'MJD', ''))
    if floating:
        for f in ['JD %s', '%s  jd', '%s (JD)']:
            FMTS.append((0, f, 'JD', ''))
    if timesys:
        for j,t in [('MJED', 'TDB'), ('JTD', 'TT')]:
            FMTS.append((0, f'{j.lower()} %s', j[:-2] + j[-1], t))
            FMTS.append((0, f'%s {j}',         j[:-2] + j[-1], t))
            FMTS.append((0, f'%s ({j})',       j[:-2] + j[-1], t))
    FMTS.append((9, 'JXD %s', '', ''))

    if padding:
        before = '  '
        after = '  '
    else:
        before = ''
        after = ''

    if embedded:
        after = ' xxx'

    count = 0
    for fstat, fmt, yval, sval in FMTS:
        for nstat, nword, nval in NUMBERS:
            test = before + fmt % nword + after
            status = fstat + nstat
            expect_failure = status > 0

            count += 1
            msg = (f'**** MJD PYPARSER test {count} expected %s: "{test}"; '
                   f'floating={floating}, timesys={timesys}, '
                   f'padding={padding}, embedded={embedded}')

        if expect_failure:
            confirm_failure(parser, test, msg=msg % 'FAILURE')
        else:
            success_msg = msg % 'SUCCESS'
            parse_dict = confirm_success(parser, test, msg=success_msg,
                                         values=[('YEAR', yval), ('DAY', nval)])
            assert parse_dict.get('TIMESYS', '') == sval, success_msg


def test_mjd_pyparser():

    from julian.mjd_pyparser import mjd_pyparser

    for padding in (False, True):
      for embedded in (False, True):
        for floating, timesys in ((False, False), (True, False), (True, True)):
            parser = mjd_pyparser(floating=floating, timesys=timesys,
                                  padding=padding, embedded=embedded)
            mjd_tester(parser, floating=floating, timesys=timesys,
                       padding=padding, embedded=embedded)

##########################################################################################
