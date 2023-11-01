################################################################################
# julian/test_init.py: make sure "import julian" includes everything it needs.
################################################################################

import julian
import pathlib
import unittest
import sys

# This is an excuse to import julian, because no other unit test does the full
# import. It's also useful for bookkeeping, confirming that we didn't forget to
# import something.

class Test_init(unittest.TestCase):

    def runTest(self):

        dir_names = set(dir(julian))

        # Get the list of Python files
        julian_root_dir = pathlib.Path(sys.modules['julian'].__file__).parent
        python_paths = list(julian_root_dir.glob('*.py'))

        # Make sure all files have been imported
        file_names = {p.name[:-3] for p in python_paths}
        missing = file_names - dir_names - {'__init__', 'unittester'}
        self.assertEqual(missing, set())

        # Identify each public, root-level function
        func_names = []
        for python_path in python_paths:
            with python_path.open(encoding='latin8') as f:
                recs = f.readlines()

            for rec in recs:
                if rec.startswith('def '):
                    func_name = rec[4:].partition('(')[0]
                    if func_name[0] != '_':
                        func_names.append(func_name)

        func_names = set(func_names)

        # Identify any functions that have not been imported
        extras = func_names - dir_names
        self.assertEqual(extras, set())

        # Anything left?
        leftovers = dir_names - file_names - func_names - {'tests'}
        leftovers = {n for n in leftovers if n[:2] != '__'}     # ignore dunders
        self.assertEqual(leftovers, {'JulianDeprecationWarning'})

##########################################################################################
