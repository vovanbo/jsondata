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


 
    def testCase110(self):
        n3 = { 'A': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
        n4 = { 'B': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
        sl4 = [ n3, n4, ]

        p0 = JSONData.getPointerPath(n4,sl4)
        resx = [[1]]
        assert p0 == resx
        pass

if __name__ == '__main__':
    unittest.main()
