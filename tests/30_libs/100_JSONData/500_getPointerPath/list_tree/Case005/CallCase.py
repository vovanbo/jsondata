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
_APPNAME = "jsondatacheck"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_add.
    """
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase100(self):
        
        n3 = [ [ [ [ 2 ], [ [ 3 ] ], [ [ 4 ] ] ] ] ]
        n4 = [ [ [ [ 3 ], [ [ 4 ] ], [ [ 5 ] ] ] ] ]
        n6 = [ [ [ [ n3, n4 ] ] ] ]
        sl6 = [ n3, n6, n4, ]
        
        a = n4[0][0][2]
        assert n4[0][0][2] == [[5]]

        p0 = JSONData.getPointerPath(n4[0][0][2],n4)
        resx = [[0, 0, 2]]
        assert p0 == resx

        
        p0 = JSONData.getPointerPath(n4[0][0][2],sl6)
        resx = [[1, 0, 0, 0, 1, 0, 0, 2]]
        assert p0 == resx

if __name__ == '__main__':
    unittest.main()
