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
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONData import MODE_SCHEMA_OFF
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem
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

    def testCase100(self):
        """Create a patch task list with 10 entries.
        """
        global jsonpatchlist
        
        jsonpatchlist = JSONPatch()
        for i in range(0,10):
            jsonpatchlist += JSONPatchItem("add", "/a"+unicode(i), "v"+unicode(i))

        ref = """[{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a6', u'value': u'v6'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}, {u'op': u'add', u'path': u'/a8', u'value': u'v8'}, {u'op': u'add', u'path': u'/a9', u'value': u'v9'}]"""
        assert ref == repr(jsonpatchlist)

        assert len(jsonpatchlist) == 10
        pass

    def testCase110(self):
        """Remove Entry 8.
        """
        global jsonpatchlist

        jsonpatchlist -= 8

        ref = """[{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a6', u'value': u'v6'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}, {u'op': u'add', u'path': u'/a9', u'value': u'v9'}]"""
        assert ref == repr(jsonpatchlist)

        assert len(jsonpatchlist) == 9
        pass

    def testCase111(self):
        """Remove Entry 8.
        """
        global jsonpatchlist

        jsonpatchlist -= 8

        ref = """[{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a6', u'value': u'v6'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}]"""
        assert ref == repr(jsonpatchlist)

        assert len(jsonpatchlist) == 8
        pass

    def testCase112(self):
        """Remove Entry 6.
        """
        global jsonpatchlist

        jsonpatchlist = jsonpatchlist - 6

        ref = [{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a1', u'value': u'v1'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}]
        assert ref == jsonpatchlist

        assert len(jsonpatchlist) == 7
        pass

    def testCase113(self):
        """Remove Entry 1.
        """
        global jsonpatchlist

        x = jsonpatchlist[1]

        jsonpatchlist -= x

        ref = [{u'op': u'add', u'path': u'/a0', u'value': u'v0'}, {u'op': u'add', u'path': u'/a2', u'value': u'v2'}, {u'op': u'add', u'path': u'/a3', u'value': u'v3'}, {u'op': u'add', u'path': u'/a4', u'value': u'v4'}, {u'op': u'add', u'path': u'/a5', u'value': u'v5'}, {u'op': u'add', u'path': u'/a7', u'value': u'v7'}]
        assert ref == jsonpatchlist

        assert len(jsonpatchlist) == 6
        pass

    def testCase200(self):
        """Apply item 0 and remove item 0.
        """
        global configdata
        global jsonpatchlist

        n,err = jsonpatchlist(configdata,0)
        ref = { "a0": "v0", "foo": "bar" }
        assert n == 1
        assert err == []
        assert ref == configdata

        jsonpatchlist -= 0
        pass
        
    def testCase201(self):
        """Apply list.
        """
        global configdata
        global jsonpatchlist

        n,err = jsonpatchlist(configdata)
        assert n == 5
        assert err == []
        ref = { "a0": "v0", "a3": "v3", "a2": "v2", "a5": "v5", "a4": "v4", "a7": "v7", "foo": "bar" }
        assert ref == configdata
        pass

    def testCase500(self):
        """Export patch task list.
        """
        global configdata
        global appname
        
        filepath = os.path.dirname(__file__)+os.sep+"export.jsonp"
        ret = jsonpatchlist.patch_export(filepath)
        assert ret

        implist = JSONPatch()
        imppatch = implist.patch_import(filepath)
        assert imppatch

        assert implist == jsonpatchlist.patch
        assert implist == jsonpatchlist
        pass

#
#######################
#
if __name__ == '__main__':
    unittest.main()
