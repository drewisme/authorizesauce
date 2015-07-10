#!/usr/bin/env python
import os
import sys
from unittest2 import TestLoader, TextTestRunner


if __name__ == '__main__':
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    authorize_dir = os.path.join(tests_dir, os.path.pardir)
    sys.path.append(authorize_dir)
    suite = TestLoader().discover(tests_dir)
    runner = TextTestRunner(verbosity=1)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
