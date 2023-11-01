##########################################################################################
# julian/test_mjd_pyparser.py
##########################################################################################

import unittest

from pyparsing import ParseException

class Test_mjd_pyparser(unittest.TestCase):


    def runTest(self):

        from julian.mjd_pyparser import mjd_pyparser

        for padding in (False, True):
          for embedded in (False, True):
            for floating, timesys in ((False, False), (True, False), (True, True)):
                parser = mjd_pyparser(floating=floating, timesys=timesys,
                                      padding=padding, embedded=embedded)
                self.my_mjd_tester(parser, floating=floating, timesys=timesys,
                                   padding=padding, embedded=embedded)

    def my_mjd_tester(self, parser, floating, timesys, padding=False, embedded=False):

        from tests.test_date_pyparser import Test_date_pyparser

        NUMBERS = []
        for n in ['12345', '-12345', '1']:
            NUMBERS.append((0, n, int(n)))
        for n in ['1234.5', '-1.5']:
            NUMBERS.append((0 if floating else 9, n, float(n)))
        NUMBERS.append((9, '1.2.5', 0))

        FMTS = []
        for f in ['MJD %s', '%s  mjd', '%s (MJD)']:
            FMTS.append((0, f, 'MJD', 'UTC'))
        if floating:
            for f in ['JD %s', '%s  jd', '%s (JD)']:
                FMTS.append((0, f, 'JD', 'UTC'))
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
                Test_date_pyparser._confirm_failure(self, parser, test,
                                                    msg=msg % 'FAILURE')
            else:
                Test_date_pyparser._confirm_success(self, parser, test,
                                                    msg=msg % 'SUCCESS',
                                                    values=[('YEAR', yval),
                                                            ('TIMESYS', sval),
                                                            ('DAY', nval)])

########################################
# Execute from the command line...
########################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
