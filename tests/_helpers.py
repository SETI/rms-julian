##########################################################################################
# tests/_helpers.py: Shared test helper functions for the julian test suite.
##########################################################################################

import warnings

import pytest
from pyparsing import ParseException


def confirm_failure(parser, test, msg):
    """Confirm that parsing the test string with the given parser fails or only
    partially matches."""

    try:
        pairs = parser.parse_string(test).as_list()

    except ParseException:
        with pytest.raises(ParseException):
            parser.parse_string(test)

    except Exception as e:  # pragma: no cover
        warnings.warn(msg + f'; Incorrect exception {type(e)}: {e}')
        with pytest.raises(Exception):
            parser.parse_string(test)

    else:
        parse_dict = {pair[0]: pair[1] for pair in pairs}
        msg += f'; {parse_dict}'
        remainder = test[parse_dict['~']:].lstrip()
        assert remainder not in ('', 'xxx'), msg


def confirm_success(parser, test, msg, values=()):
    """Confirm that parsing succeeds and check expected values. Returns
    parse_dict."""

    error = None
    try:
        pairs = parser.parse_string(test).as_list()
    except Exception as e:  # pragma: no cover
        error = e

    assert error is None, msg

    parse_dict = {pair[0]: pair[1] for pair in pairs}
    msg += f'; {parse_dict}'

    for name, value in values:
        assert name in parse_dict, msg
        assert parse_dict[name] == value, msg

    remainder = test[parse_dict['~']:].lstrip()
    assert remainder in ('', 'xxx'), msg

    return parse_dict

##########################################################################################
