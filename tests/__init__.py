##########################################################################################
# julian/tests/__init__.py
##########################################################################################

import unittest

from tests.test_calendar          import *
from tests.test_date_parsers      import *
from tests.test_date_pyparser     import *
from tests.test_datetime_parsers  import *
from tests.test_datetime_pyparser import *
from tests.test_deltat            import *
from tests.test_formatters        import *
from tests.test_iso_parsers       import *
from tests.test_leap_seconds      import *
from tests.test_mjd_jd            import *
from tests.test_mjd_pyparser      import *
from tests.test_time_of_day       import *
from tests.test_time_parsers      import *
from tests.test_time_pyparser     import *
from tests.test_utc_tai_tdb_tt    import *
from tests.test_utils             import *
from tests.test_v1                import *

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
