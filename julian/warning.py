##########################################################################################
# julian/warning.py
##########################################################################################

import warnings

class JulianDeprecationWarning(DeprecationWarning):
    pass

WARNING_MESSAGES = set()

def _warn(message):
    """Raise this DeprecationWarning message, but only once."""

    global WARNING_MESSAGES

    if message in WARNING_MESSAGES:
        return

    warnings.warn(message, category=JulianDeprecationWarning)
    WARNING_MESSAGES.add(message)

##########################################################################################
