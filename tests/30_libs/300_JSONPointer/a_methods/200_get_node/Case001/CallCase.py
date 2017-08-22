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
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase100(self):
        data = {'a': {'b': {'c': 2}}}
        D = JSONData([])
        n = JSONPointer('').get_node(D.data)
        D.branch_add(n,'-',data)
#         D.branch_add(n,None,data)

        assert D.data == [data]
        pass


if __name__ == '__main__':
    unittest.main()
