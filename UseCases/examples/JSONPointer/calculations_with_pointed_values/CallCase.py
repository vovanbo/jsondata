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

        jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
        
        a = JSONPointer("/a/b/c")
        b = JSONPointer("/x/y")
        c = JSONPointer("/2/x/y/v")
        d = JSONPointer("/a/b/d")

        print a(jdata) + d(jdata)
        print JSONPointer(a(jdata) + d(jdata))

        assert ( a(jdata) + d(jdata) ) == 5
        assert ( JSONPointer(a(jdata) + d(jdata)) ) == """/5"""

    
if __name__ == '__main__':
    unittest.main()
