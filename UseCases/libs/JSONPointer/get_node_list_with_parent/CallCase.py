# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""


import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson

try:
    from jsondata.pointer import JSONPointer
    from jsondata.data import JSONData
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n")

#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase010(self):
        
        data = [ [ [ 2 ] ] ]
        target = { 'A': { 'A' : [3] } }
        D = JSONData(data)
        n = JSONPointer("/0/0/0")
        n = n.get_node(D.data,True)
        D.branch_add(target['A']['A'],None,n)

        rdata={'A': {'A': [2]}}
        assert target == rdata
        pass


if __name__ == '__main__':
    unittest.main()
