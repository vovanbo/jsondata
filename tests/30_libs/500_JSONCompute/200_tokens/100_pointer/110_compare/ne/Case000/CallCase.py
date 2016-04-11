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

    def testCase014(self):
        """Check basics for required data.
        """
        assert JSONCompute([a]) != "/stock/total/0"

    def testCase015(self):
        """Check basics for required data.
        """
        assert JSONCompute([b]) != "/locations/location/local/0"

    def testCase016(self):
        """Check basics for required data.
        """
        assert JSONCompute([c]) != "/locations/location/products/0"

    def testCase017(self):
        """Check basics for required data.
        """
        assert JSONCompute([a]) >= "/stock/total/0"

    def testCase018(self):
        """Check basics for required data.
        """
        assert JSONCompute([b]) >= "/locations/location/local/0"

    def testCase019(self):
        """Check basics for required data.
        """
        assert JSONCompute([c]) >= "/locations/location/products/0"

    def testCase020(self):
        """Check basics for required data.
        """
        assert JSONCompute([a,'/0']) <= "/stock/total"

    def testCase021(self):
        """Check basics for required data.
        """
        assert JSONCompute([b,'/0']) <= "/locations/location/local"

    def testCase022(self):
        """Check basics for required data.
        """
        assert JSONCompute([c,'/0']) <= "/locations/location/products"


#
#######################
#
if __name__ == '__main__':
    unittest.main()
