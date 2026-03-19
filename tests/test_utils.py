##########################################################################################
# julian/test_utils.py
##########################################################################################

import numpy as np

from julian._utils import (
    _float,
    _int,
    _is_float,
    _is_int,
    _number,
)


def test_utils_int():

    assert _int(3.14) == 3
    assert isinstance(_int(3.14), int)

    assert _int(-3.14) == -4
    assert isinstance(_int(-3.14), int)

    test = _int([3.14, -3.14])
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('int64')
    assert list(test) == [3, -4]

    test = _int(np.array([3.14, -3.14]))
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('int64')
    assert list(test) == [3, -4]

    test = _int(np.array(7))
    assert not isinstance(test, np.ndarray)
    assert isinstance(test, int)

    test = _int(np.array(7.))
    assert not isinstance(test, np.ndarray)
    assert isinstance(test, int)

    for dtype in ('int8', 'uint8', 'int16', 'uint16', 'uint64', 'float32', 'float64'):
        digits = np.arange(10, dtype=dtype)
        test = _int(digits)
        assert isinstance(test, np.ndarray)
        assert test.dtype == np.dtype('int64')

        test = _int(digits[0])
        assert isinstance(test, int)

def test_utils_float():

    assert _float(3) == 3.
    assert isinstance(_float(3), float)

    test = _float([3, -4])
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('float64')
    assert list(test) == [3., -4.]

    test = _float(np.array([3, -4]))
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('float64')
    assert list(test) == [3., -4.]

    test = _float(np.array(7))
    assert not isinstance(test, np.ndarray)
    assert isinstance(test, float)

    test = _float(np.array(7.))
    assert not isinstance(test, np.ndarray)
    assert isinstance(test, float)

    for dtype in ('int8', 'uint8', 'uint16', 'int32', 'uint64', 'float32', 'float64'):
        digits = np.arange(10, dtype=dtype)
        test = _float(digits)
        assert isinstance(test, np.ndarray)
        assert test.dtype == np.dtype('float64')

        test = _float(digits[0])
        assert isinstance(test, float)

def test_utils_number():

    assert _number(3.14) == 3.14
    assert isinstance(_number(3.14), float)

    assert _number(-3.14) == -3.14
    assert isinstance(_number(-3.14), float)

    test = _number([3.14, -3.14])
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('float64')
    assert list(test) == [3.14, -3.14]

    test = _number(np.array([3.14, -3.14]))
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('float64')
    assert list(test) == [3.14, -3.14]

    assert _number(3) == 3
    assert isinstance(_number(3), int)

    test = _number([3, -4])
    assert isinstance(test, np.ndarray)
    assert test.dtype == np.dtype('int64')
    assert list(test) == [3, -4]

    test = _number(np.array(7))
    assert isinstance(test, int)

    test = _number(np.array(7.))
    assert isinstance(test, float)

    for dtype in ('int8', 'uint8', 'uint16', 'int32', 'uint64', 'float32', 'float64'):
        digits = np.arange(10, dtype=dtype)
        test = _number(digits)
        assert isinstance(test, np.ndarray)
        if dtype[0] == 'f':
            assert test.dtype == np.dtype(dtype)
        else:
            assert test.dtype == np.dtype('int64')

        test = _number(digits[0])
        if dtype[0] == 'f':
            assert isinstance(test, float)
        else:
            assert isinstance(test, int)

def test_utils_is_int():

    assert _is_int(3)
    assert not _is_int(3.)

    assert _is_int([3,4])
    assert not _is_int([3,4.])

    assert _is_int(np.array([3,4]))
    assert not _is_int(np.array([3,4.]))

def test_utils_is_float():

    assert _is_float(3.)
    assert not _is_float(3)

    assert _is_float([3.,4])
    assert not _is_float([3,4])

    assert _is_float(np.array([3.,4]))
    assert not _is_float(np.array([3,4]))

##########################################################################################
