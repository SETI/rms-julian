##########################################################################################
# julian/test_time_of_day.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian.time_of_day import (
    hms_from_sec,
    sec_from_hms,
)

from julian._exceptions import JulianValidateFailure as jvf

class Test_time_of_day(unittest.TestCase):

    def runTest(self):

        # Check hms_from_sec
        self.assertEqual(hms_from_sec(0), (0, 0, 0))
        self.assertEqual(hms_from_sec(86400), (23, 59, 60))
        small = 2.**-20
        self.assertEqual(hms_from_sec(86410 - small), (23, 59, 70 - small))
        self.assertRaises(jvf, hms_from_sec, 86410)
        self.assertRaises(jvf, hms_from_sec, -1.e-30)

        # Check sec_from_hms
        self.assertEqual(sec_from_hms(0, 0, 0), 0)
        self.assertEqual(sec_from_hms(23, 59, 60), 86400)

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
        self.assertRaises(jvf, sec_from_hms, -1,  0,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms, 24,  0,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1, -1,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1, 60,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1,  1, -1, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1,  1, 60, validate=True)

        self.assertRaises(jvf, sec_from_hms, -0.001,  0,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms, 24.000,  0,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1, -0.001,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1, 60.000,  0, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1,  1, -0.001, validate=True)
        self.assertRaises(jvf, sec_from_hms,  1,  1, 60.000, validate=True)

        self.assertRaises(jvf, sec_from_hms, 23, 59, 70, validate=True, leapsecs=True)
        self.assertRaises(jvf, sec_from_hms, 23, 59, 60, validate=True, leapsecs=False)

        # ...but these should be fine
        _ = sec_from_hms(23, 59, 59, validate=True, leapsecs=True)
        _ = sec_from_hms(23, 59, 59, validate=True, leapsecs=False)

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
