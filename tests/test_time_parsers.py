##########################################################################################
# julian/test_time_parsers.py
##########################################################################################

import unittest

from julian.time_parsers import (
    sec_from_string,
    secs_in_strings,
)

from julian._DEPRECATED import (
    time_in_string,
    times_in_string,
)

from julian._exceptions import JulianParseException as JPE
from julian._exceptions import JulianValidateFailure as JVF


class Test_time_parsers(unittest.TestCase):

    def runTest(self):

        import warnings
        from julian._warnings import JulianDeprecationWarning
        warnings.filterwarnings('ignore', category=JulianDeprecationWarning)

        # Note: test_time_pyparser.py has more extensive unit tests

        # sec_from_string
        self.assertEqual(sec_from_string('00:00:00.000'), 0.0)
        self.assertEqual(sec_from_string('00:00:00'), 0)
        self.assertEqual(sec_from_string('00:00:59.000'), 59.0)
        self.assertEqual(sec_from_string('00:00:59'), 59)

        self.assertIs(type(sec_from_string('00:00:00.000')), float)
        self.assertIs(type(sec_from_string('00:00:00')), int)
        self.assertIs(type(sec_from_string('00:00:59.000')), float)
        self.assertIs(type(sec_from_string('00:00:59')), int)

        # sec_from_string, leapsecs
        self.assertEqual(sec_from_string('23:59:60.000'), 86400.0)
        self.assertEqual(sec_from_string('23:59:69.000'), 86409.0)
        self.assertRaises(JPE, sec_from_string, '23:59:70.000')
        self.assertRaises(JPE, sec_from_string, '23:59:60', leapsecs=False)

        # sec_from_string, am/pm
        self.assertEqual(sec_from_string('12:00:00 am', ampm=True),     0)
        self.assertEqual(sec_from_string(' 1:00:00 am', ampm=True),  3600)
        self.assertEqual(sec_from_string('11:59:59 am', ampm=True), 43199)
        self.assertEqual(sec_from_string('12:00:00PM ', ampm=True), 43200)
        self.assertEqual(sec_from_string(' 1:00:00 pm', ampm=True), 43200 + 3600)
        self.assertEqual(sec_from_string('11:59:59 pm', ampm=True), 86399)
        self.assertEqual(sec_from_string('11:59:60 pm', ampm=True, leapsecs=True), 86400)
        self.assertRaises(JPE, sec_from_string, '11:59:60 pm', ampm=True, leapsecs=False)
        self.assertRaises(JPE, sec_from_string, '23:00:00 am', ampm=True)

        # sec_from_string, floating
        self.assertEqual(sec_from_string('12h',    floating=True), 43200)
        self.assertEqual(sec_from_string('1.5 h',  floating=True), 5400)
        self.assertEqual(sec_from_string('86399s', floating=True), 86399)
        self.assertEqual(sec_from_string('86400s', floating=True, leapsecs=True), 86400)
        self.assertEqual(sec_from_string('1:10.5', floating=True), 70.5 * 60)
        self.assertEqual(sec_from_string('60 M',   floating=True), 60 * 60)

        self.assertRaises(JPE, sec_from_string, '86400s', floating=True, leapsecs=False)

        # sec_from_string, timezones, am/pm, leapsecs
        self.assertEqual(sec_from_string('00:00 gmt',   timezones=True), (0, 0))
        self.assertEqual(sec_from_string('0:01 Z',      timezones=True), (60, 0))
        self.assertEqual(sec_from_string('16:00-08',    timezones=True), (0, 1))
        self.assertEqual(sec_from_string('16:00 PST',   timezones=True), (0, 1))
        self.assertEqual(sec_from_string('0:00 cet',    timezones=True), (86400 - 3600, -1))
        self.assertEqual(sec_from_string('0:00 cest',   timezones=True), (86400 - 7200, -1))
        self.assertEqual(sec_from_string('12:00am gmt', timezones=True), (0, 0))
        self.assertEqual(sec_from_string('1:00 am bst', timezones=True), (0, 0))
        self.assertEqual(sec_from_string('6:59:60 pm est', timezones=True, leapsecs=True),
                                         (86400, 0))

        self.assertRaises(JPE, sec_from_string, '10:59:59 pm', ampm=False)
        self.assertRaises(JPE, sec_from_string, '7:59:59 pm est', ampm=True,
                          timezones=False)
        self.assertRaises(JPE, sec_from_string, '6:59:60 pm est', ampm=True,
                          timezones=True, leapsecs=False)
        self.assertRaises(JVF, sec_from_string, '7:59:60 pm est', ampm=True,
                          timezones=True, leapsecs=True)

        # secs_in_strings
        self.assertEqual(secs_in_strings('t=00:00:00.000', first=True), 0.0)
        self.assertEqual(secs_in_strings(['...', 't=00:00:00.000'], first=True), 0.0)
        self.assertEqual(secs_in_strings(['...', 't=00:00:00.000']), [0.])
        self.assertEqual(secs_in_strings(['25:00', 't=00:00:00.000']), [0.])
        self.assertEqual(secs_in_strings('after midnight, 1:00 am bst or later',
                                         timezones=True),
                         [(0, 0)])
        self.assertEqual(secs_in_strings('after midnight, 1:00 am bst or later',
                                         timezones=True, substrings=True),
                         [(0, 0, '1:00 am bst')])

        #### DEPRECATED

        # Check time_in_string
        self.assertEqual(time_in_string('This is the time--00:00:00.000'), 0.0)
        self.assertEqual(time_in_string('Is this the time? 00:00:00=now'), 0)
        self.assertEqual(time_in_string('Time:00:00:59.000 is now'), 59.0)
        self.assertEqual(time_in_string('Time (00:00:59)'), 59)
        self.assertEqual(time_in_string('Time (00:00:60)'), 60)
        self.assertEqual(time_in_string('Time (00:00:99)'), None)
        self.assertEqual(time_in_string('whatever'), None)

        # Check time_in_string with leap seconds
        self.assertEqual(time_in_string('End time[23:59:60.000]'), 86400.0)
        self.assertEqual(time_in_string('End time is 23:59:69.000 and later'), 86409.0)
        self.assertEqual(time_in_string('Error 23:5z:00.000:0'), None)

        self.assertEqual(time_in_string('End time[23:59:60.000]', remainder=True)[1], ']')
        self.assertEqual(time_in_string('End time is 23:59:69.000 and later',
                                        remainder=True)[1], ' and later')

        # Check times_in_string with leap seconds
        self.assertEqual(times_in_string('End time[23:59:60.000]'), [86400.0])
        self.assertEqual(times_in_string('End time is 23:59:69.000 and later'), [86409.0])
        self.assertEqual(times_in_string('Error 23:5z:00.000:0'), [])

##########################################################################################
