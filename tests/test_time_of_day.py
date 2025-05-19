##########################################################################################
# julian/test_time_of_day.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian.time_of_day import (
    hms_from_sec,
    hms_microsec_from_sec,
    sec_from_hms,
)

from julian._exceptions import JulianValidateFailure as JVF

class Test_time_of_day(unittest.TestCase):

    def runTest(self):

        np.random.seed(1753)

        # Check hms_from_sec
        self.assertEqual(hms_from_sec(0), (0, 0, 0))
        self.assertIs(type(hms_from_sec(0)[0]), int)
        self.assertIs(type(hms_from_sec(0)[1]), int)
        self.assertIs(type(hms_from_sec(0)[2]), int)

        self.assertEqual(hms_from_sec(0.), (0, 0, 0))
        self.assertIs(type(hms_from_sec(0.)[0]), int)
        self.assertIs(type(hms_from_sec(0.)[1]), int)
        self.assertIs(type(hms_from_sec(0.)[2]), float)

        self.assertEqual(hms_from_sec(86400), (23, 59, 60))
        small = 2.**-20
        self.assertEqual(hms_from_sec(86410 - small), (23, 59, 70 - small))
        self.assertRaises(JVF, hms_from_sec, 86410, validate=True, leapsecs=True)
        self.assertRaises(JVF, hms_from_sec, 86400, validate=True, leapsecs=False)
        self.assertRaises(JVF, hms_from_sec, -1.e-30, validate=True)

        self.assertEqual(hms_from_sec(43200, validate=True,  leapsecs=True ), (12, 0, 0))
        self.assertEqual(hms_from_sec(43200, validate=True,  leapsecs=False), (12, 0, 0))
        self.assertEqual(hms_from_sec(43200, validate=False, leapsecs=True ), (12, 0, 0))
        self.assertEqual(hms_from_sec(43200, validate=False, leapsecs=False), (12, 0, 0))

        # Check sec_from_hms
        self.assertEqual(sec_from_hms(0, 0, 0), 0)
        self.assertIs(type(sec_from_hms(0, 0, 0)), int)
        self.assertIs(type(sec_from_hms(0, 0, 0.)), float)
        self.assertIs(type(sec_from_hms(0, 0., 0)), float)
        self.assertIs(type(sec_from_hms(0., 0, 0)), float)

        self.assertEqual(sec_from_hms(23, 59, 60), 86400)
        self.assertIs(type(sec_from_hms(23, 59, 60)), int)
        self.assertIs(type(sec_from_hms(23, 59, 60.)), float)
        self.assertIs(type(sec_from_hms(23, 59., 60)), float)
        self.assertIs(type(sec_from_hms(23., 59, 60)), float)

        # Array tests
        # This makes about 333,000 non-uniformly spaced transcendental numbers
        secs = 86410. * np.sqrt(np.arange(0., 1., 3.e-6))

        # Because HMS times carry extra precision, inversions should be exact
        (h,m,s) = hms_from_sec(secs)
        errors = (sec_from_hms(h,m,s) - secs)
        self.assertTrue(np.all(errors == 0.))

        # Test all seconds
        seclist = np.arange(0,86410)

        # Convert to hms and back
        (h, m, t) = hms_from_sec(seclist)
        test_seclist = sec_from_hms(h, m, t)

        self.assertTrue(np.all(test_seclist == seclist))

        # Check types
        self.assertTrue(isinstance(hms_from_sec(10)[-1], numbers.Integral))
        self.assertFalse(isinstance(hms_from_sec(10.)[-1], numbers.Integral))

        self.assertEqual(hms_from_sec([10,10])[-1].dtype.kind, 'i')
        self.assertEqual(hms_from_sec([10.,10])[-1].dtype.kind, 'f')

        self.assertTrue(isinstance(sec_from_hms(0, 0, 10), numbers.Integral))
        self.assertFalse(isinstance(sec_from_hms(0, 0, 10.), numbers.Integral))

        self.assertEqual(sec_from_hms(0, 0, [10,10]).dtype.kind, 'i')
        self.assertEqual(sec_from_hms(0, 0, [10.,10]).dtype.kind, 'f')

        # Check errors
        self.assertRaises(JVF, sec_from_hms, -1,  0,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms, 24,  0,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1, -1,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1, 60,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1,  1, -1, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1,  1, 60, validate=True)

        self.assertRaises(JVF, sec_from_hms, -0.001,  0,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms, 24.000,  0,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1, -0.001,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1, 60.000,  0, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1,  1, -0.001, validate=True)
        self.assertRaises(JVF, sec_from_hms,  1,  1, 60.000, validate=True)

        self.assertRaises(JVF, sec_from_hms, 23, 59, 70, validate=True, leapsecs=True)
        self.assertRaises(JVF, sec_from_hms, 23, 59, 60, validate=True, leapsecs=False)

        # ...but these should be fine
        _ = sec_from_hms(23, 59, 59, validate=True, leapsecs=True)
        _ = sec_from_hms(23, 59, 59, validate=True, leapsecs=False)

        # Check hms_microsec_from_sec
        self.assertEqual(hms_microsec_from_sec(0), (0, 0, 0, 0))
        self.assertIs(type(hms_microsec_from_sec(0)[0]), int)
        self.assertIs(type(hms_microsec_from_sec(0)[1]), int)
        self.assertIs(type(hms_microsec_from_sec(0)[2]), int)
        self.assertIs(type(hms_microsec_from_sec(0)[3]), int)

        self.assertEqual(hms_microsec_from_sec(0.), (0, 0, 0, 0))
        self.assertIs(type(hms_microsec_from_sec(0.)[0]), int)
        self.assertIs(type(hms_microsec_from_sec(0.)[1]), int)
        self.assertIs(type(hms_microsec_from_sec(0.)[2]), int)
        self.assertIs(type(hms_microsec_from_sec(0.)[3]), int)      # always integral

        # int array
        seconds = np.arange(86410)
        test = hms_microsec_from_sec(seconds)
        self.assertEqual(test[0].dtype, np.int64)
        self.assertEqual(test[1].dtype, np.int64)
        self.assertEqual(test[2].dtype, np.int64)
        self.assertEqual(test[3].dtype, np.int64)
        self.assertTrue(np.all(test[3] == 0))

        # floats
        self.assertEqual(hms_microsec_from_sec(1.2345678), (0, 0, 1, 234568))
        self.assertEqual(hms_microsec_from_sec(86409.9999995), (23, 59, 69, 999999))
        self.assertEqual(hms_microsec_from_sec(-0.0000004999), (0, 0, 0, 0))
        self.assertRaises(JVF, hms_microsec_from_sec, 86410, validate=True, leapsecs=True)
        self.assertRaises(JVF, hms_microsec_from_sec, 86409.99999950001, validate=True,
                          leapsecs=True)
        self.assertRaises(JVF, hms_microsec_from_sec, 86400, validate=True,
                          leapsecs=False)
        self.assertRaises(JVF, hms_microsec_from_sec, 86399.99999950001, validate=True,
                          leapsecs=False)
        self.assertRaises(JVF, hms_microsec_from_sec, -0.0000005, validate=True)

        # float arrays
        # This makes about 3300 non-uniformly spaced transcendental numbers
        seconds = 86410. * np.sqrt(np.arange(0., 1., 3.e-4))
        test = hms_microsec_from_sec(seconds)
        self.assertEqual(test[0].dtype, np.int64)
        self.assertEqual(test[1].dtype, np.int64)
        self.assertEqual(test[2].dtype, np.int64)
        self.assertEqual(test[3].dtype, np.int64)

        seconds = np.arange(86410) + 0.0000005
        self.assertTrue(np.all(hms_microsec_from_sec(seconds)[3]) == 0)

        seconds = 86410. * np.random.rand(100,100)
        diff = hms_microsec_from_sec(seconds)[3] - np.floor(1.e6 * (seconds%1.) + 0.5)
        self.assertTrue(np.all(diff == 0))

        # Check sec_from_hms() with microseconds
        self.assertEqual(sec_from_hms(0, 0, 0, 0), 0)
        self.assertIs(type(sec_from_hms(0, 0, 0, 0)), int)
        self.assertIs(type(sec_from_hms(0, 0, 0, 0.)), float)
        self.assertIs(type(sec_from_hms(0, 0, 0., 0)), float)
        self.assertIs(type(sec_from_hms(0, 0., 0, 0)), float)
        self.assertIs(type(sec_from_hms(0., 0, 0, 0)), float)

        microsec = np.arange(0, 1000000, 10).reshape(25, 4, -1)
        sec = sec_from_hms(0, 0, 0, microsec)
        self.assertTrue(np.all(microsec / 1.e6 == sec))
        self.assertEqual(sec.shape, microsec.shape)

        self.assertRaises(JVF, sec_from_hms, 0,  0,  0, -1, validate=True)
        self.assertRaises(JVF, sec_from_hms, 0,  0,  0, 1000000, validate=True)

##########################################################################################
