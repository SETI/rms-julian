##########################################################################################
# julian/test_utils.py
##########################################################################################

import numbers
import numpy as np
import unittest

from julian.utils import (
    _float,
    _int,
    _is_float,
    _is_int,
    _number,
)


class Test_utils(unittest.TestCase):

    def runTest(self):

        # _int
        self.assertEqual(_int(3.14), 3)
        self.assertTrue(isinstance(_int(3.14), numbers.Integral))

        self.assertEqual(_int(-3.14), -4)
        self.assertTrue(isinstance(_int(3.14), numbers.Integral))

        test = _int([3.14, -3.14])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype.kind, 'i')
        self.assertEqual(list(test), [3, -4])

        test = _int(np.array(7))
        self.assertFalse(isinstance(test, np.ndarray))

        test = _int(np.array(7.))
        self.assertFalse(isinstance(test, np.ndarray))

        # _float
        self.assertEqual(_float(3), 3.)
        self.assertFalse(isinstance(_float(3), numbers.Integral))

        test = _float([3, -4])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype.kind, 'f')
        self.assertEqual(list(test), [3., -4.])

        test = _float(np.array(7))
        self.assertFalse(isinstance(test, np.ndarray))
        self.assertFalse(isinstance(test, numbers.Integral))
        self.assertTrue(isinstance(test, numbers.Real))

        test = _float(np.array(7.))
        self.assertFalse(isinstance(test, np.ndarray))
        self.assertFalse(isinstance(test, numbers.Integral))
        self.assertTrue(isinstance(test, numbers.Real))

        # _number
        self.assertEqual(_number(3.14), 3.14)
        self.assertFalse(isinstance(_number(3.14), numbers.Integral))

        self.assertEqual(_number(-3.14), -3.14)
        self.assertFalse(isinstance(_number(3.14), numbers.Integral))

        test = _number([3.14, -3.14])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype.kind, 'f')
        self.assertEqual(list(test), [3.14, -3.14])

        self.assertEqual(_number(3), 3)
        self.assertTrue(isinstance(_number(3), numbers.Integral))

        test = _number([3, -4])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype.kind, 'i')
        self.assertEqual(list(test), [3, -4])

        test = _int(np.array(7))
        self.assertFalse(isinstance(test, np.ndarray))

        test = _int(np.array(7.))
        self.assertFalse(isinstance(test, np.ndarray))

        # _is_int
        self.assertTrue(_is_int(3))
        self.assertFalse(_is_int(3.))

        self.assertTrue(_is_int([3,4]))
        self.assertFalse(_is_int([3,4.]))

        # _is_float
        self.assertTrue(_is_float(3.))
        self.assertFalse(_is_float(3))

        self.assertTrue(_is_float([3.,4]))
        self.assertFalse(_is_float([3,4]))

########################################
# Executed from the command line
########################################

if __name__ == '__main__':
    unittest.main()

##########################################################################################
