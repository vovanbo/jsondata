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
    from jsondata.patch import JSONPatch,JSONPatchItem
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
        ref = """{u'foo': u'bar', u'baz': u'qux'}"""
        assert ref == repr(configdata)

    def testCase001(self):
        global configdata
        global appname
        global jsonpatchlist

        jsonpatchlist = JSONPatch()
        patchfile = os.path.dirname(__file__)+os.sep+'patch.jsonp'
        jsonpatchlist.patch_import(patchfile)

        ref=repr(jsonpatchlist)
        ref = """[{u'op': u'replace', u'path': u'/baz', u'value': u'boo'}]"""
        assert ref == repr(jsonpatchlist)

    def testCase002(self):
        global configdata
        global appname
        global jsonpatchlist

        jsonpatchlist.apply(configdata)
        ref=repr(configdata)
        ref = """{u'foo': u'bar', u'baz': u'boo'}"""
        assert ref == repr(configdata)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
