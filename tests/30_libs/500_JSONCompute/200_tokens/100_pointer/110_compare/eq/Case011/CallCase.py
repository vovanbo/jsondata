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
        """Check add pointers by compute.
        """

        comp = JSONCompute([])

        instack = [
            JSONPointer("/locations"),
            '+',
            ['location', 'products'],
            '+',
            0,
            '+',
            '/quantity'
        ]

        instack[4] = 0
        outstack = []
        comp.resolveSyn(instack, outstack)
        outstackX = [['locations', 'location', 'products', 0, 'quantity']]
        assert outstack == outstackX 


        instack[4] = 1
        outstack = []
        comp.resolveSyn(instack, outstack)
        outstackX = [['locations', 'location', 'products', 1, 'quantity']]
        assert outstack == outstackX 
        
        instack[4] = 2
        outstack = []
        comp.resolveSyn(instack, outstack)
        outstackX = [['locations', 'location', 'products', 2, 'quantity']]
        assert outstack == outstackX 


    def testCase011(self):
        """Check add pointers in loop.
        """

        comp = JSONCompute([])

        instack = [
            JSONPointer("/locations"),
            '+',
            ['location', 'products'],
            '+',
            0,
            '+',
            '/quantity'
        ]

        C = [] 
        for i in range(0,3):

            instack[4] = i
            outstack = []
            comp.resolveSyn(instack, outstack)
            C.append(outstack[0])

        Cx = [
            ['locations', 'location', 'products', 0, 'quantity'],
            ['locations', 'location', 'products', 1, 'quantity'],
            ['locations', 'location', 'products', 2, 'quantity'],
        ]
        assert C == Cx

    def testCase012(self):
        """Check add pointers in loop.
        """

        comp = JSONCompute([])

        instack = [
            JSONPointer("/locations"),
            '+',
            ['location', 'products'],
            '+',
            0,
            '+',
            '/quantity'
        ]

        C = [] 
        for i in range(0,3):

            instack[4] = i
            outstack = []
            comp.resolveSyn(instack, outstack)
            C.append(str( outstack[0]))

        Cx = [
            '/locations/location/products/0/quantity',
            '/locations/location/products/1/quantity',
            '/locations/location/products/2/quantity',
        ]
        assert C == Cx


#
#######################
#
if __name__ == '__main__':
    unittest.main()
