##########################################################################################
# julian/utils.py
##########################################################################################

import numbers
import numpy as np


def _int(arg):
    """Convert to int; works for scalar, array, or array-like. Floating-point numbers are
    always rounded downward.
    """

    if isinstance(arg, numbers.Integral):
        return int(arg)

    if isinstance(arg, numbers.Real):
        return int(arg // 1.)

    if not isinstance(arg, np.ndarray):
        arg = np.array(arg)

    if not arg.shape:
        return _int(arg[()])

    if arg.dtype.kind in 'ui':
        return arg

    return (arg // 1.).astype('int64')


def _float(arg):
    """Convert to floating-point; works for scalar, array, or array-like."""

    if isinstance(arg, numbers.Real):
        return float(arg)

    if isinstance(arg, np.ndarray) and not arg.shape:
        return float(arg[()])

    return np.asfarray(arg)


def _number(arg):
    """Convert to array if array-like, but preserve data type."""

    if isinstance(arg, numbers.Real):
        return arg

    if isinstance(arg, np.ndarray) and not arg.shape:
        return arg[()]

    return np.array(arg)


def _is_int(arg):
    """True if this value or this array-like contains only integers."""

    if isinstance(arg, numbers.Integral):
        return True

    if isinstance(arg, numbers.Real):
        return False

    if not isinstance(arg, np.ndarray):
        arg = np.array(arg)

    return arg.dtype.kind in 'ui'


def _is_float(arg):
    """True if this value or this array-like contains floating-point values."""

    if isinstance(arg, numbers.Integral):
        return False

    if isinstance(arg, numbers.Real):
        return True

    if not isinstance(arg, np.ndarray):
        arg = np.array(arg)

    return arg.dtype.kind == 'f'

##########################################################################################
