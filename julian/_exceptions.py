##########################################################################################
# julian/_exceptions.py
##########################################################################################
"""
==========
Exceptions
==========
"""

class JulianParseException(ValueError):
    """A subclass of ValueError, raised when a string cannot be parsed."""
    pass

class JulianValidateFailure(ValueError):
    """A subclass of ValueError, raised when a numeric value is invalid."""
    pass

##########################################################################################
