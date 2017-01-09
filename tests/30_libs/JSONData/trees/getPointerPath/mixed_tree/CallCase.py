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


    def testCase500(self):
        """Equal."""
        n0 = { 'a': { 'b': { 'c': [2] }}}
        n1 = { 'a': { 'b': { 'c': [2] }}}
        ret = JSONData.getTreeDiff(n0, n1)
        assert ret == True
        pass

    def testCase501(self):
        """Diff."""
        n0 = { 'a': { 'b': { 'c': [2] }}}
        n1 = { 'A': { 'b': { 'c': [2] }}}
        ret = JSONData.getTreeDiff(n0, n1)
        assert ret == False
        pass
 
    def testCase502(self):
        """Diff."""
        n0 = { 'a': [{ 'b': { 'c': 2 }}]}
        n1 = { 'a': [{ 'B': { 'c': 2 }}]}
        ret = JSONData.getTreeDiff(n0, n1)
        assert ret == False
        pass

    def testCase503(self):
        """Diff."""
        n0 = { 'a': { 'b': [{ 'c': 2 }]}}
        n1 = { 'a': { 'b': [{ 'C': 2 }]}}
        ret = JSONData.getTreeDiff(n0, n1)
        assert ret == False
        pass
 
if __name__ == '__main__':
    unittest.main()
