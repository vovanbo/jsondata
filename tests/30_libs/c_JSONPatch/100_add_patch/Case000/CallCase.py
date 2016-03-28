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
import jsonschema


jval = None

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

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

    def testCase003(self):
        """Create a patch task list.
        """
        global configdata
        global appname

        global jsonpatchlist
        
        jsonpatchlist = JSONPatch()
        for i in range(0,10):
            jsonpatchlist += JSONPatchItem("add", "/a"+unicode(i), "v"+unicode(i))

        #ref = repr(jsonpatchlist)
        #print ref
        ref = """[{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a6', u'value': u'v6'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}, {u'op': u'add', u'path': u'/a8', u'value': u'v8'}, {u'op': u'add', u'path': u'/a9', u'value': u'v9'}]"""
        assert ref == repr(jsonpatchlist)

    def testCase004(self):
        """Apply former created patch task list.
        """
        global configdata
        global appname

        n,err = jsonpatchlist.apply(configdata)
        #print repr(configdata)
        ref = """{u'a1': u'v1', u'a0': u'v0', u'a3': u'v3', u'a2': u'v2', u'a5': u'v5', u'a4': u'v4', u'a7': u'v7', u'a6': u'v6', u'a9': u'v9', u'a8': u'v8', u'foo': u'bar'}"""
        
        assert n == 10
        assert err == []
        assert ref == repr(configdata)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
