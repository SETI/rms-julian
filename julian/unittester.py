##########################################################################################
# julian/unittester.py
##########################################################################################

import unittest

from julian.tests.test_calendar          import *
from julian.tests.test_date_parser       import *
from julian.tests.test_date_pyparser     import *
from julian.tests.test_datetime_parser   import *
from julian.tests.test_datetime_pyparser import *
from julian.tests.test_deltat            import *
from julian.tests.test_formatter         import *
from julian.tests.test_init              import *
from julian.tests.test_iso_parser        import *
from julian.tests.test_leap_seconds      import *
from julian.tests.test_mjd_jd            import *
from julian.tests.test_mjd_pyparser      import *
from julian.tests.test_time_of_day       import *
from julian.tests.test_time_parser       import *
from julian.tests.test_time_pyparser     import *
from julian.tests.test_utc_tai_tdb       import *
from julian.tests.test_utils             import *
from julian.tests.v1_tests               import *

############################################
# Execute from command line...
############################################

if __name__ == '__main__':
    unittest.main(verbosity=2)

##########################################################################################
