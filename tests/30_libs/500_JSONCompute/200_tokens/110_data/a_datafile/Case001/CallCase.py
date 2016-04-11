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
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem
    from jsondata.JSONPointer import JSONPointer
    from jsondata.JSONCompute import JSONCompute
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'datafile.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

    def testCase010(self):
        """Check basics for required data.
        """
        global a
        global b
        global c
        a = JSONPointer("/stock/total")
        b = JSONPointer("/locations/location/local")
        c = JSONPointer("/locations/location/products")

    def testCase100(self):
        """Check basics for required data.
        """
        A = [
            'data(',
            configdata,
            ')',
            a,
             
        ]
        assert JSONCompute([a]) == "/stock/total"
        assert JSONCompute([b]) == "/locations/location/local"
        assert JSONCompute([c]) == "/locations/location/products"

        assert JSONCompute([a]) != "/stock/total/0"
        assert JSONCompute([b]) != "/locations/location/local/0"
        assert JSONCompute([c]) != "/locations/location/products/0"

        assert JSONCompute([a]) >= "/stock/total/0"
        assert JSONCompute([b]) >= "/locations/location/local/0"
        assert JSONCompute([c]) >= "/locations/location/products/0"

        assert JSONCompute([a,'/0']) <= "/stock/total"
        assert JSONCompute([b,'/0']) <= "/locations/location/local"
        assert JSONCompute([c,'/0']) <= "/locations/location/products"

# b = JSONCompute(["/locations/location/local"])
#         c = JSONCompute(["/locations/location/products"])
#         
#         c0 = c + 0 + 'quatity'
#         c0x = '/locations/location/products/0/quatity'
#         assert c0 == c0x
#         
#         c1 = c + 1 + 'quatity'
#         c1x = '/locations/location/products/1/quatity'
#         assert c1 == c1x
# 
#         c2 = c + 2 + 'quatity'
#         c2x = '/locations/location/products/2/quatity'
#         assert c2 == c2x
#         
# 
#     def testCase011(self):
#         """Check add pointers in loop.
#         """
#         global configdata
#         global appname
# 
#         a = JSONPointer("/stock/total")
#         b = JSONPointer("/locations/location/products")
#         
#         C = [] 
#         for i in range(0,3):
#             C.append(str(b + i + 'quatity'))
# 
#         Cx = [
#               '/locations/location/products/0/quatity',
#               '/locations/location/products/1/quatity',
#               '/locations/location/products/2/quatity',
#         ]
# 
#         assert C == Cx



#
#######################
#
if __name__ == '__main__':
    unittest.main()
