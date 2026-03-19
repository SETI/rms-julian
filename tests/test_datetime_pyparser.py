##########################################################################################
# julian/test_datetime_pyparser.py
##########################################################################################

import pytest

from pyparsing                import ParseException
from julian.datetime_pyparser import datetime_pyparser
from tests.test_mjd_pyparser  import mjd_tester


def test_datetime_pyparser():

    for iso_only in (True, False):
      for treq in (True, False):
        for timezones in (True, False):
          for date in ('2024-01-04', '2024-004', '24-01-04', '24-004',
                       '20240104', '2024004', '240104', '24004'):

            p = datetime_pyparser(iso_only=iso_only, treq=treq, timezones=timezones,
                                  doy=True)
            for time in ('12:34:56', '123456', '12:34:56.25', '123456.25', ''):
              if treq and not time:
                with pytest.raises(ParseException):
                    p.parse_string(date)
                continue

              for suffix in ('Z', '', '+08'):
                test = date + ('T' if time else '') + time + suffix
                if suffix and (not time or not timezones):
                    with pytest.raises(ParseException):
                        p.parse_string(test)
                    continue

                pairs = p.parse_string(test).as_list()
                parse_dict = {pair[0]:pair[1] for pair in pairs}
                if time:
                    assert parse_dict['HOUR'] == 12
                    assert parse_dict['MINUTE'] == 34
                    if '.25' in time:
                        assert parse_dict['SECOND'] == 56.25
                    else:
                        assert parse_dict['SECOND'] == 56

                assert parse_dict['YEAR'] == 2024
                assert parse_dict['DAY'] == 4
                if '004' not in date:
                    assert parse_dict['MONTH'] == 1

            p = datetime_pyparser(iso_only=iso_only, treq=False, floating=True,
                                  doy=True)
            test = date + '.25'
            pairs = p.parse_string(test).as_list()
            parse_dict = {pair[0]:pair[1] for pair in pairs}
            assert parse_dict['YEAR'] == 2024
            assert parse_dict['DAY'] == 4.25

            with pytest.raises(ParseException):
                p.parse_string(test + 'T00:00:00')

            p = datetime_pyparser(iso_only=iso_only, treq=False, floating=False,
                                  doy=True)
            with pytest.raises(ParseException):
                p.parse_string(test)
            with pytest.raises(ParseException):
                p.parse_string(test + 'T00:00:00')

            p = datetime_pyparser(iso_only=iso_only, treq=True, floating=True,
                                  doy=True)
            p = datetime_pyparser(iso_only=iso_only, treq=True, floating=True,
                                   doy=True)
            with pytest.raises(ParseException):
                p.parse_string(test + 'T00:00:00')

            for time, h, m in [('10.'     , 10. , None ),
                               ('10.5'    , 10.5, None ),
                               ('10:30.'  , 10  , 30.  ),
                               ('10:30.25', 10  , 30.25)]:
                test = '2000-01-01T' + time
                p = datetime_pyparser(iso_only=iso_only, treq=False, floating=True)
                pairs = p.parse_string(test).as_list()
                parse_dict = {pair[0]:pair[1] for pair in pairs}
                assert parse_dict['HOUR'] == h
                assert parse_dict.get('MINUTE', None) == m

                p = datetime_pyparser(iso_only=iso_only, treq=False, floating=False)
                with pytest.raises(ParseException):
                    p.parse_string(test)

    # Most general parser
    p = datetime_pyparser(treq=False, doy=True, mjd=True, weekdays=True,
                          extended=True, leapsecs=True, ampm=True, timezones=True,
                          floating=True, timesys=True, padding=True, embedded=False)

    for test in [' 2000.1.1, 13:00:00.000'  , '2000-JAN-01:13:00:00.00Z \r\n'   ,
                 ' 2000-JAN-01/13:00:00.00' , '00/JAN/01/13:00:00.00 GMT'       ,
                 ' 2000-01-01  13:00:00.000', ' 2000-01-01 // 13:00:00.000 UTC' ,
                 ' 2000-01-01/ 1:00:00 pm'  , ' 2000-01-01/ 1: 0: 0 pm'         ,
                 ' 00-01-01/13: 0: 0 PDT'   , '\t   +2000-001 13:00  '          ,
                 '+02000-jan-1 13:00-01'    , '20000101T13.0Z '                 ,
                 '00001T13.+12:45'          , 'Jan  1, 2000 1:00  pm  PDT '     ,
                 'January 1, AD 2000,13h'   , '000101 780.M   '                 ,
                 '01-01-00, 46800.00s'      , '01-01-00, 46800.00s tdt'         ,
                 '13:00:00.000 2000-01-01 ' , ' 13:00:00.00:2000-JAN-01'        ,
                 '13:00:00.00/2000-JAN-01'  , '1pm EST/00/JAN/01'               ,
                 '13:00:00.000Z 2000-01-01' , ' 13:00:00.000 // 2000-01-01 '    ,
                 ' 1:00:00 pm, 2000-01-01'  , '1: 0: 0 pm 2000-01-01 '          ,
                 ' 1: 0: 0 pm 00-01-01'     , '13:00 CHAS 01-01-00'             ,
                 '1 PM CHAS 01-01-00']:
        pairs = p.parse_string(test).as_list()
        parse_dict = {pair[0]:pair[1] for pair in pairs}
        assert parse_dict['YEAR'] == 2000
        assert parse_dict['DAY'] == 1
        assert parse_dict.get('MONTH', 1) == 1

        h = parse_dict.get('HOUR', 0)
        m = parse_dict.get('MINUTE', 0)
        s = parse_dict.get('SECOND', 0)
        assert s + 60*(m + 60*h) == 60*60*13

    # Test fractional date, optional time system
    assert p.parse_string('2000-01-01. UTC').as_list()[:8:2] == \
                [('YEAR', 2000), ('MONTH', 1), ('DAY', 1.0), ('TIMESYS', 'UTC')]
    assert p.parse_string('2000-01-01. ').as_list()[:6:2] == \
                [('YEAR', 2000), ('MONTH', 1), ('DAY', 1.0)]
    assert p.parse_string('2000-001. UTC').as_list()[:6:2] == \
                [('YEAR', 2000), ('DAY', 1.0), ('TIMESYS', 'UTC')]
    assert p.parse_string('2000-001.5').as_list()[:4:2] == \
                [('YEAR', 2000), ('DAY', 1.5)]

    # Test MJD/JD
    p = datetime_pyparser(mjd=True, timesys=True, padding=False, embedded=False)
    mjd_tester(p, floating=True, timesys=True,
               padding=False, embedded=False)

    for test, answer in [('MJD 12345.6 TAI', 'TAI'), ('JD 12345.6 TDT', 'TT'),
                         ('MJED 12345.6',    'TDB'), ('JTD 12345.6',    'TT')]:
        pairs = p.parse_string(test).as_list()
        parse_dict = {pair[0]:pair[1] for pair in pairs}
        assert parse_dict['TIMESYS'] == answer

    with pytest.raises(ParseException):
        p.parse_string('JED 12345.6 UTC')

    p = datetime_pyparser(mjd=True, timesys=False, padding=False, embedded=False)
    mjd_tester(p, floating=True, timesys=False,
               padding=False, embedded=False)

##########################################################################################
