# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson


jval = None

try:
    from jsondata.JSONPointer import JSONPointer
    from jsondata.JSONCompute import JSONCompute
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase010(self):
        """Check basics for required data.
        """
        global a
        global b
        global c
        a = JSONPointer("/stock/total")
        b = JSONPointer("/locations/location/local")
        c = JSONPointer("/locations/location/products")

    def testCase011(self):
        """Check basics for required data.
        """
        assert JSONCompute([a]) == "/stock/total"

    def testCase012(self):
        """Check basics for required data.
        """
        assert JSONCompute([b]) == "/locations/location/local"

    def testCase013(self):
        """Check basics for required data.
        """
        assert JSONCompute([c]) == "/locations/location/products"

    def testCase021(self):
        """Check basics for required data.
        """
        try:
            assert JSONCompute([a,0]) == "/stock/total"
        except:
            pass
        else:
            assert 0 == 1


#
#######################
#
if __name__ == '__main__':
    unittest.main()
