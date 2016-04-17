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

        a = JSONPointer("/a/b/c")
        b = JSONPointer("/x/y")
        c = JSONPointer("/a/b/c/2/x/y/v")
        d = JSONPointer("/a/b/c/2/x/y")
        e = JSONPointer("/a/b/c/2/x")
    
        # loop with increment
        for i in range(0,4):
            print str(a + i + b) + " > " + str(c) + " = " + str(a + i + b > c )
        
        print
        print str(a + 2 + b) + " > " + str(d) + " = " + str(a + 2 + b > d )
        
        print
        print str(a + 2 + b) + " > " + str(e) + " = " + str(a + 2 + b > e )


        assert ( a + 0 + b > c ) == False
        assert ( a + 1 + b > c ) == False
        assert ( a + 2 + b > c ) == True
        assert ( a + 3 + b > c ) == False
        
        assert ( a + 2 + b > d ) == False
        assert ( a + 2 + b > e ) == False

   
    
if __name__ == '__main__':
    unittest.main()
