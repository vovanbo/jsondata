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
import jsonschema


jval = None

try:
    from jsondata.pointer import JSONPointer
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n")
try:
    from jsondata.serializer import JSONDataSerializer as ConfigData
    from jsondata.serializer import MODE_SCHEMA_OFF
    from jsondata.patch import JSONPatch,JSONPatchItem,JSONPatchItemRaw
    from jsondata.pointer import JSONPointer
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n")

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'data.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

        ref = repr(configdata)
        ref = """{u'~1': 10, u'/': 9}"""
        assert ref == repr(configdata)

    def testCase001(self):
        """Assemble patch list, Adding to a Nonexistent Target
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        jsonpatchlist += JSONPatchItemRaw("""{"op": "test", "path": "/~01", "value": 10}""")
        ref=repr(jsonpatchlist)
        ref = """[{u'op': u'test', u'path': u'/~1', u'value': 10}]"""
        assert ref == repr(jsonpatchlist) # the complete patch list

    def testCase002(self):
        """Apply patch list, Adding to a Nonexistent Target
        """
        global configdata
        global appname
        global jsonpatchlist

        cnt,failed = jsonpatchlist.apply(configdata) # apply all patches
        assert cnt == 1 # number of patch items
        assert failed == [] # list of failed patch items

#
#######################
#
if __name__ == '__main__':
    unittest.main()
