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
import jsonschema


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
        """Check add pointers by compute.
        """
        a = JSONPointer("/a/b/c")
        b = JSONPointer("/x/y")
        c = JSONPointer("/a/b/c/2/x/y/v")
        
        for i in range(0,5):
            try:
                assert a + i + b > c
            except:
                if i == 2: # it is a pointer only operation, thus matching length counts
                    raise

    def testCase011(self):
        """Check add pointers by compute.
        """

        comp = JSONCompute([])

        a = JSONPointer("/a/b/c")
        b = JSONPointer("/x/y")
        c = JSONPointer("/a/b/c/2/x/y/v")

        instack = [
            a,
            '+',
            0,
            '+',
            b
        ]

        
        for i in range(0,5):
            try:
                assert a + i + b > c
            except:
                if i == 2: # it is a pointer only operation, thus matching length counts
                    raise

    def testCase012(self):
        """Check add pointers by compute.
        """

        instack = [
            JSONPointer("/a/b/c"),
            '+',
            0,
            '+',
            JSONPointer("/x/y"),
            '>',
            JSONPointer("/a/b/c/2/x/y/v")
        ]

        
        for i in range(0,5):
            try:
                instack[2]=i
                assert JSONCompute(instack).result == True
            except:
                if i == 2: # it is a pointer only operation, thus matching length counts
                    raise

if __name__ == '__main__':
    unittest.main()
