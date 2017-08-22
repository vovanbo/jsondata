"""Append list element.
"""


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

from jsondata.data import JSONData

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_add.
    """


    def testCase112(self):
        n3 = { 'A': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
        n4 = { 'B': {'a0': { 'b0': { 'c0': 3 }, 'b1': {'c0': 4}, 'b2': {'c0': 5} }}}
        sl4 = [ n3, n4, ]

        p0 = JSONData.get_pointer_path(n3['A']['a0']['b0'], sl4)
        resx = [[0,'A','a0','b0']]
        assert p0 == resx
        pass

if __name__ == '__main__':
    unittest.main()
