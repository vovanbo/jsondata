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
    from jsondata.JSONData import JSONData
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        global jval
        global jdata
        
        jval = { 'value0':[ 11, 22, 33, ], 'value1':[ 100, 200, 300, ]}
        jdata = JSONData(jval)

    def testCase011(self):
        """Add and convert."""
        global result010

        val0 = jdata.getCanonical(JSONPointer(['value0',0]))
        assert val0 == 11

if __name__ == '__main__':
    unittest.main()
