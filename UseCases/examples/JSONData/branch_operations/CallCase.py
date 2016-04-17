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

try:
    from jsondata.JSONData import JSONData
    from jsondata.JSONPointer import JSONPointer, JSONPointerException       
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """"Create the JSON Document."""
        global D

        # JSON document
        jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
        
        # JSON branch with array
        arr = { 'e': { 'lx': [] } }
        
        # Branch elements for array
        ai0 = { 'v0': 100}
        ai1 = { 'v1': 200}
        
        
        # JSON branch with object
        obj = { 'f': { 'ox': {} } }
        
        # Branch elements for object
        l0 = { 'o0': 10}
        l1 = { 'o1': 20}
        
        
        # JSON in-memory document
        D = JSONData(jdata)
        
        
        # Add a branch with an array
        D.branch_add(JSONPointer('/a/b'),'e',arr['e'])
        
        # Add a items to the new array
        D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai0)
        D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai1)
        
        
        # Add a branch with an object
        D.branch_add(JSONPointer('/a/b'),'f',obj['f'])
        
        # Add an item to the new object, from an object
        D.branch_add(JSONPointer('/a/b/f/ox'),'v0',ai0['v0'])
        
        # Add an item to the new object
        ai1v1 = ai1['v1']
        D.branch_add(JSONPointer('/a/b/f/ox'),'v1',ai1v1)

    def testCase001(self):
        """"Create a new branch and add items."""
    
        nodex = JSONPointer(['a','b']).get_node(D.data)
        ret = D.branch_create(nodex, ['g','x'], {})

        ret['x0'] = 22
        ret['x1'] = 33
        
        ret = D.branch_create(nodex, ['g','x','xlst'], [])

        ret.append('first')
        ret.append('second')

        rdata = {'a': {'b': {'c': 2, 'e': {'lx': [{'v0': 100}, {'v1': 200}]}, 'd': 3, u'g': {u'x': {'x0': 22, 'x1': 33, u'xlst': ['first', 'second']}}, 'f': {'ox': {'v0': 100, 'v1': 200}}}}}
        assert D.data == rdata

    def testCase010(self):
        """Print structured data."""
        print D

    def testCase020(self):
        """Print 'repr' data."""
        print repr(D)

    def testCase030(self):
        """Get the value of a node."""
        print D(JSONPointer(['a', 'b', 'c']))
        assert D(JSONPointer(['a', 'b', 'c'])) == 2 

    def testCase031(self):
        """Get the value of a node by path list."""
        print D(['a', 'b', 'c'])
        assert D(['a', 'b', 'c']) == 2 

    def testCase032(self):
        """Get the value of a node with a JSONPointer object by RFC6901 string."""
        print D(JSONPointer('/a/b/c'))
        assert D(JSONPointer('/a/b/c')) == 2 

    def testCase033(self):
        """Get the value of a node by RFC6901 string."""
        print D('/a/b/c')
        assert D('/a/b/c') == 2 

    def testCase034(self):
        """Get the value of a node from the node itself - variant 0."""
        n = JSONPointer('/a/b/c').get_node(D.data,True)
        print n['c']
        assert n['c'] == 2 

    def testCase035(self):
        """Get the value of a node from the node itself - variant 1."""
        n = JSONPointer('/a/b/c').get_node(D.data,True)
        px = D.getPointerPath(n, D.data)[0]
        px.append('c')
        print D(JSONPointer(px))
        assert D(JSONPointer(px)) == 2

    def testCase040(self):
        """Move a branch."""

        target = JSONPointer('/a/b/new')
        source = JSONPointer('/a/b/c')
        
        print D(source)
        n = D('/a/b')
        n['c'] = 77

        targetnode = target.get_node(D.data,True)
        sourcenode = source.get_node(D.data,True)

        D.branch_move(targetnode, 'new', sourcenode, 'c')

        # check new position
        assert D(target) == 77 
        
        # validate old position
        try:
            x = D('/a/b/c')
        except JSONPointerException as e:
            pass
        else:
            raise
        pass

    def testCase050(self):
        """Remove a branch."""

        target     = JSONPointer('/a/b/new')
        targetnode = target.get_node(D.data,True)

        # verify existence
        x = D('/a/b/new')
        assert x == 77

        # remove
        D.branch_remove(targetnode, 'new')

        # validate old position
        try:
            x = D('/a/b/new')
        except JSONPointerException as e:
            pass
        else:
            raise
        pass

    def testCase060(self):
        """Replace a branch."""

        # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
        targetnode = JSONPointer('/a/b/new').get_node(D.data,True)

        sourcenode = {'alternate': 4711 }

        ret = D.branch_replace(targetnode, 'f', sourcenode)
        assert ret == True
        
        # verify new
        x = D('/a/b/f/alternate')
        assert x == 4711

    def testCase070(self):
        """Test a branch - variant 0."""
        ret = D.branch_test(JSONPointer('/a/b/f/alternate').get_node_or_value(D.data), 4711)
        assert ret == True
        pass

    def testCase071(self):
        """Test a branch - variant 1."""
        ret = D.branch_test(JSONPointer('/a/b/f/alternate')(D.data), 4711)
        assert ret == True
        pass

    def testCase072(self):
        """Test a branch - variant 2."""
        p = JSONPointer('/a/b/f/alternate')
        ret = D.branch_test(p(D.data), 4711)
        assert ret == True
        pass

    def testCase080(self):
        """"Copy a new branch."""
        arr = { 'cpy': { 'cx': [ 2, 3, 4, ] } }

        # Copy a branch with an array
        D.branch_copy(JSONPointer('/a/b'),'cpy',arr['cpy'])

        assert D('/a/b/cpy') == arr['cpy']
        pass

if __name__ == '__main__':
    unittest.main()
