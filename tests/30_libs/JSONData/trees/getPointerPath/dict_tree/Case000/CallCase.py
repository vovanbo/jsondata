"""Append list element.
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call 
if 'ujson' in sys.argv:
    import ujson as myjson
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

from jsondata.JSONData import JSONData

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_add.
    """


    def testCase100(self):
        n5 = { 'x': 12 }
        sl5 = [ n5, ]
        
        p0 = JSONData.getPointerPath(n5,sl5)
        resx = [[0]]
        assert p0 == resx
        pass

if __name__ == '__main__':
    unittest.main()
