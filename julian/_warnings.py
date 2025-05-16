##########################################################################################
# julian/_warnings.py
##########################################################################################
"""Warnings manager"""

import warnings


class JulianDeprecationWarning(DeprecationWarning):
    """Raised to alert the user that they are using a deprecated feature."""
    pass


_WARNING_MESSAGES = set()


def _warn(message):
    """Raise this DeprecationWarning message, but only once."""

    global _WARNING_MESSAGES

    if message in _WARNING_MESSAGES:
        return

    warnings.warn(message, category=JulianDeprecationWarning)
    _WARNING_MESSAGES.add(message)


def _reset_warnings():
    """Reset the list of warnings issued."""

    global _WARNING_MESSAGES

    _WARNING_MESSAGES = set()

##########################################################################################
