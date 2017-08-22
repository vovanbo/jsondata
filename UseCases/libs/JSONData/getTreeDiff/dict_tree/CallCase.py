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
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'a': { 'b': { 'c': 2 }}}
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == True
        pass

    def testCase501(self):
        """Diff."""
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'A': { 'b': { 'c': 2 }}}
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass
 
    def testCase502(self):
        """Diff."""
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'a': { 'B': { 'c': 2 }}}
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase503(self):
        """Diff."""
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'a': { 'b': { 'C': 2 }}}
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase504(self):
        """Diff."""
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'A': { 'B': { 'C': 3 }}}
        ret = JSONData.get_tree_diff(n0, n1)
        assert ret == False
        pass

    def testCase600(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'A': { 'B': { 'C': 3 }}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'n1': {'A': {'B': {'C': 3}}}, 'n0[a]': {'b': {'c': 2}}, 'dl': 0}]
        pass

    def testCase601(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'a': { 'B': { 'C': 3 }}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'dl': 1, 'n0[a][b]': {'c': 2}, 'n1[a]': {'B': {'C': 3}}}]
        pass

    def testCase602(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}}
        n1 = { 'a': { 'b': { 'C': 3 }}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'dl': 2, 'n0[a][b][c]': 2, 'n1[a][b]': {'C': 3}}]    
        pass


    def testCase710(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}, 'x': 0}
        n1 = { 'A': { 'B': { 'C': 3 }}, 'y': 1}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'n1': {'A': {'B': {'C': 3}}, 'y': 1}, 'n0[a]': {'b': {'c': 2}}, 'dl': 0}]   
        pass

    def testCase720(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}, 'x': {'y': 1}}
        n1 = { 'a': { 'B': { 'C': 3 }}, 'x': {'y': 2}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs)
        assert ret == False

        assert mydiffs == [{'dl': 1, 'n0[a][b]': {'c': 2}, 'n1[a]': {'B': {'C': 3}}}]    
        pass

    def testCase800(self):
        """Diff."""
        mydiffs = []
        n0 = { 'x': {'y': 1}}
        n1 = { 'x': {'y': 2}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'dl': 1, 'n1[x][y]': 2, 'n0[x][y]': 1}]         
        pass

    def testCase810(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}, 'x': 0, 'z': 3, 'w': {'v': 1} }
        n1 = { 'A': { 'B': { 'C': 3 }}, 'y': 1, 'z': 4, 'w': {'v': 2} }
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs ==  [{'n1': {'A': {'B': {'C': 3}}, 'y': 1, 'z': 4, 'w': {'v': 2}}, 'n0[a]': {'b': {'c': 2}}, 'dl': 0}, {'n1': {'A': {'B': {'C': 3}}, 'y': 1, 'z': 4, 'w': {'v': 2}}, 'dl': 0, 'n0[x]': 0}, {'dl': 0, 'n1[z]': 4, 'n0[z]': 3}, {'n1[w][v]': 2, 'n0[w][v]': 1, 'dl': 1}]         
        pass

    def testCase820(self):
        """Diff."""
        mydiffs = []
        n0 = { 'a': { 'b': { 'c': 2 }}, 'x': {'y': 1}}
        n1 = { 'a': { 'B': { 'C': 3 }}, 'x': {'y': 2}}
        ret = JSONData.get_tree_diff(n0, n1, mydiffs, True)
        assert ret == False

        assert mydiffs == [{'dl': 1, 'n0[a][b]': {'c': 2}, 'n1[a]': {'B': {'C': 3}}}, {'dl': 1, 'n1[x][y]': 2, 'n0[x][y]': 1}]         
        pass
 
if __name__ == '__main__':
    unittest.main()
