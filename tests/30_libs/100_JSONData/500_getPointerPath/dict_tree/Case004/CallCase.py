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
        n3 = { 'A': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
        n4 = { 'B': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
        n6 = { 'x0': { 'x1': { 'x2': n4 }} }
         
        sl6 = [ n3, n6, n4, ]
         
        p0 = JSONData.get_pointer_path(n4['B']['a0']['b2'], sl6)
        resx = [[1, 'x0', 'x1', 'x2', 'B', 'a0', 'b2']]
        assert p0 == resx

        p0 = JSONData.get_pointer_path(n4['B']['a0']['b2'], sl6, JSONData.FIRST)
        resx = [[1, 'x0', 'x1', 'x2', 'B', 'a0', 'b2']]
        assert p0 == resx


#     def testCase500(self):
#         """Equal."""
#         n0 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         n1 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         n2 = { 'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}
#         
#         n3 = { 'A': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
#         n4 = { 'B': {'a0': { 'b0': { 'c0': 2 }, 'b1': {'c0': 3}, 'b2': {'c0': 4} }}}
#         
#         n5 = { 'x': 12 }
# 
#         sl0 = [ n0, n1, n2, n3, n4, ]
#         sl1 = [ n0, n1, n2 ]
#         sl2 = [ n0, n2, n3, n4, ]
#         sl3 = [ n0, n3, n4, ]
#         sl4 = [ n3, n4, ]
#         sl5 = [ n5, ]
#         
#         res = []
#         
#         p0 = JSONData.get_pointer_path(n5,sl5)
#         resx = [[0]]
#         assert p0 == resx
#         pass


if __name__ == '__main__':
    unittest.main()
