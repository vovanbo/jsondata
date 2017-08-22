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


    def testCase500(self):
        """Equal."""
        n0 = [ [ [ 2 ]]]
        n1 = [ [ [ 2 ]]]
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == True
        pass

    def testCase501(self):
        """Diff."""
        n0 = [ [ [ 2 ]]]
        n1 = [ 'x', [ [ 2 ]]]
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass
 
    def testCase502(self):
        """Diff."""
        n0 = [ [ [ 2 ]]]
        n1 = [ [ 'x', [ 2 ]]]
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase503(self):
        """Diff."""
        n0 = [ [ [ 2 ]]]
        n1 = [ [ [ 'x', 2 ]]]
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase504(self):
        """Diff."""
        n0 = [ [ [ 2 ]]]
        n1 = [ 'x', [ 'y', [ 'z', 2 ]]]
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase600(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ 'x', [ 'y', [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'n0': [[[2]]], 'n1': ['x', ['y', ['z', 3]]], 'dl': 0}]         
        pass

    def testCase601(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ [ 'y', [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'n1[0]': ['y', ['z', 3]], 'dl': 1, 'n0[0]': [[2]]}]        
        pass

    def testCase602(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ [ [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'dl': 2, 'n1[0][0]': ['z', 3], 'n0[0][0]': [2]}]
        pass

    def testCase700(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ 'x', [ 'y', [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n0': [[[2]]], 'n1': ['x', ['y', ['z', 3]]], 'dl': 0}]         
        pass

    def testCase701(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ [ 'y', [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n1[0]': ['y', ['z', 3]], 'dl': 1, 'n0[0]': [[2]]}]     
        pass

    def testCase702(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ [ [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'dl': 2, 'n1[0][0]': ['z', 3], 'n0[0][0]': [2]}]
        pass

    def testCase800(self):
        """Diff."""
        mydiffs = []
        n0 = [ [[0,1]] ]
        n1 = [ [[0,2]] ]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n0[0][0][1]': 1, 'dl': 2, 'n1[0][0][1]': 2}]     
        pass

    def testCase801(self):
        """Diff."""
        mydiffs = []
        n0 = [ [0,1] ]
        n1 = [ [0,2] ]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs ==  [{'dl': 1, 'n1[0][1]': 2, 'n0[0][1]': 1}]    
        pass

    def testCase802(self):
        """Diff."""
        mydiffs = []
        n0 = [ [[0,1]] ]
        n1 = [ [[0,2]] ]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n0[0][0][1]': 1, 'dl': 2, 'n1[0][0][1]': 2}]   
        pass

    def testCase810(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]], [3]]
        n1 = [ 'x', [ 'y', [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n1[0]': 'x', 'dl': 1, 'n0[0]': [[2]]}, {'n0[1]': [3], 'dl': 1, 'n1[1]': ['y', ['z', 3]]}]         
        pass

    def testCase820(self):
        """Diff."""
        mydiffs = []
        n0 = [ 0,  [3],  [[0,1]],  [ [ 2 ]          ] ]
        n1 = [ 1,  [1],  [[0,2]],  [ 'y', [ 'z', 3 ]] ]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'n1[0]': 1, 'dl': 0, 'n0[0]': 0}, {'dl': 1, 'n0[1][0]': 3, 'n1[1][0]': 1}, {'n1[2][0][1]': 2, 'dl': 2, 'n0[2][0][1]': 1}, {'dl': 1, 'n0[3]': [[2]], 'n1[3]': ['y', ['z', 3]]}]        
        pass

    def testCase830(self):
        """Diff."""
        mydiffs = []
        n0 = [ [ [ 2 ]]]
        n1 = [ [ [ 'z', 3 ]]]
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'dl': 2, 'n1[0][0]': ['z', 3], 'n0[0][0]': [2]}]
        pass

if __name__ == '__main__':
    unittest.main()
