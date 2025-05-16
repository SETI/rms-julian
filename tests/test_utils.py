##########################################################################################
# julian/test_utils.py
##########################################################################################

import numpy as np
import unittest

from julian._utils import (
    _float,
    _int,
    _is_float,
    _is_int,
    _number,
)


class Test_utils(unittest.TestCase):

    def test_utils_int(self):

        self.assertEqual(_int(3.14), 3)
        self.assertIsInstance(_int(3.14), int)

        self.assertEqual(_int(-3.14), -4)
        self.assertIsInstance(_int(3.14), int)

        test = _int([3.14, -3.14])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype, np.dtype('int64'))
        self.assertEqual(list(test), [3, -4])

        test = _int(np.array([3.14, -3.14]))
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype, np.dtype('int64'))
        self.assertEqual(list(test), [3, -4])

        test = _int(np.array(7))
        self.assertNotIsInstance(test, np.ndarray)
        self.assertIsInstance(test, int)

        test = _int(np.array(7.))
        self.assertNotIsInstance(test, np.ndarray)
        self.assertIsInstance(test, int)

        for dtype in ('int8', 'uint8', 'int16', 'uint16', 'uint64', 'float32', 'float64'):
            digits = np.arange(10, dtype=dtype)
            test = _int(digits)
            self.assertIsInstance(test, np.ndarray)
            self.assertEqual(test.dtype, np.dtype('int64'))

            test = _int(digits[0])
            self.assertIsInstance(test, int)

    def test_utils_float(self):

        self.assertEqual(_float(3), 3.)
        self.assertIsInstance(_float(3), float)

        test = _float([3, -4])
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype, np.dtype('float64'))
        self.assertEqual(list(test), [3., -4.])

        test = _float(np.array([3, -4]))
        self.assertTrue(isinstance(test, np.ndarray))
        self.assertEqual(test.dtype, np.dtype('float64'))
        self.assertEqual(list(test), [3., -4.])

        test = _float(np.array(7))
        self.assertNotIsInstance(test, np.ndarray)
        self.assertIsInstance(test, float)

        test = _float(np.array(7.))
        self.assertNotIsInstance(test, np.ndarray)
        self.assertIsInstance(test, float)

        for dtype in ('int8', 'uint8', 'uint16', 'int32', 'uint64', 'float32', 'float64'):
            digits = np.arange(10, dtype=dtype)
            test = _float(digits)
            self.assertIsInstance(test, np.ndarray)
            self.assertEqual(test.dtype, np.dtype('float64'))

            test = _float(digits[0])
            self.assertIsInstance(test, float)

    def test_utils_number(self):

        self.assertEqual(_number(3.14), 3.14)
        self.assertIsInstance(_number(3.14), float)

        self.assertEqual(_number(-3.14), -3.14)
        self.assertIsInstance(_number(3.14), float)

        test = _number([3.14, -3.14])
        self.assertIsInstance(test, np.ndarray)
        self.assertEqual(test.dtype, np.dtype('float64'))
        self.assertEqual(list(test), [3.14, -3.14])

        test = _number(np.array([3.14, -3.14]))
        self.assertIsInstance(test, np.ndarray)
        self.assertEqual(test.dtype, np.dtype('float64'))
        self.assertEqual(list(test), [3.14, -3.14])

        self.assertEqual(_number(3), 3)
        self.assertIsInstance(_number(3), int)

        test = _number([3, -4])
        self.assertIsInstance(test, np.ndarray)
        self.assertEqual(test.dtype, np.dtype('int64'))
        self.assertEqual(list(test), [3, -4])

        test = _number(np.array(7))
        self.assertIsInstance(test, int)

        test = _number(np.array(7.))
        self.assertIsInstance(test, float)

        for dtype in ('int8', 'uint8', 'uint16', 'int32', 'uint64', 'float32', 'float64'):
            digits = np.arange(10, dtype=dtype)
            test = _number(digits)
            self.assertIsInstance(test, np.ndarray)
            if dtype[0] == 'f':
                self.assertEqual(test.dtype, np.dtype(dtype))
            else:
                self.assertEqual(test.dtype, np.dtype('int64'))

            test = _number(digits[0])
            if dtype[0] == 'f':
                self.assertIsInstance(test, float)
            else:
                self.assertIsInstance(test, int)

    def test_utils_is_int(self):

        self.assertTrue(_is_int(3))
        self.assertFalse(_is_int(3.))

        self.assertTrue(_is_int([3,4]))
        self.assertFalse(_is_int([3,4.]))

        self.assertTrue(_is_int(np.array([3,4])))
        self.assertFalse(_is_int(np.array([3,4.])))

    def test_utils_is_float(self):

        self.assertTrue(_is_float(3.))
        self.assertFalse(_is_float(3))

        self.assertTrue(_is_float([3.,4]))
        self.assertFalse(_is_float([3,4]))

        self.assertTrue(_is_float(np.array([3.,4])))
        self.assertFalse(_is_float(np.array([3,4])))

##########################################################################################
