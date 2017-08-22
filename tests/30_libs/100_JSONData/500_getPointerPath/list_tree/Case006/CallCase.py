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
        c0 = [ 4 ]
        
        n3 = [ [ [ 1,    [ [ 3 ] ],  [ c0 ] ] ] ]
        n4 = [ [ [ [ 3 ], [ c0 ],    [ c0 ] ] ] ]

        sl6 = [ n3, ]

        p0 = JSONData.get_pointer_path(n4[0][0][2][0], sl6, JSONData.ALL)
        resx = [
            [0, 0, 0, 2, 0], 
        ]
        
        assert p0 == resx


if __name__ == '__main__':
    unittest.main()
