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
        """Conversion"""
        comp = JSONCompute([0])
        assert comp.result == '/0' 

    def testCase011(self):
        """Conversion, one result only of multiple."""
        comp = JSONCompute([0,1])
        assert comp.result == '/1' 

    def testCase012(self):
        """Conversion,"""
        comp = JSONCompute([0,'+',1])
        assert comp.result == '/0/1' 

    def testCase013(self):
        """Conversion, erroneous because requires a list"""
        p = JSONPointer([0,1])
        comp = JSONCompute(p)       # must be a list of tokens(JSONPointer for now is known exception)!!!
        assert comp.result == '/1'  # actually has to be '/0/1'

    def testCase014(self):
        """Conversion of a JSONPointer"""
        p = JSONPointer([0,1])
        comp = JSONCompute([p])
        assert comp.result == '/0/1' 

if __name__ == '__main__':
    unittest.main()
