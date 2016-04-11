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
    from jsondata.JSONPointer import JSONPointer
    from jsondata.JSONData import JSONData
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase010(self):

        data = {'a': {'b': {'c': 2}}}
        target = { 'A': { 'A' : 'x' } }
        D = JSONData(data)
        n = JSONPointer("/a/b/c")
        n = n.get_node(D.data,True)
        D.branch_add(target['A'],None,n)

        rdata={'A': {'c': 2}}
        assert target == rdata
        pass

if __name__ == '__main__':
    unittest.main()
