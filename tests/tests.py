import doctest
from unittest import TestSuite

import utils

def test_suite():
    return TestSuite([
        doctest.DocTestSuite(utils)
    ])
