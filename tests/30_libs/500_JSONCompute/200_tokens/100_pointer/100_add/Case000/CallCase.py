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
        """Check add pointers.
        """
 
        a = JSONPointer("/stock/total")
        b = JSONPointer("/locations/location/local")
        c = JSONPointer("/locations/location/products")
        
        c0 = c + 0 + 'quatity'
        c0x = '/locations/location/products/0/quatity'
        assert c0 == c0x
        
        c1 = c + 1 + 'quatity'
        c1x = '/locations/location/products/1/quatity'
        assert c1 == c1x

        c2 = c + 2 + 'quatity'
        c2x = '/locations/location/products/2/quatity'
        assert c2 == c2x
        

    def testCase011(self):
        """Check add pointers in loop.
        """

        a = JSONPointer("/stock/total")
        b = JSONPointer("/locations/location/products")
        
        C = [] 
        for i in range(0,3):
            C.append(str(b + i + 'quatity'))

        Cx = [
              '/locations/location/products/0/quatity',
              '/locations/location/products/1/quatity',
              '/locations/location/products/2/quatity',
        ]

        assert C == Cx



#
#######################
#
if __name__ == '__main__':
    unittest.main()
