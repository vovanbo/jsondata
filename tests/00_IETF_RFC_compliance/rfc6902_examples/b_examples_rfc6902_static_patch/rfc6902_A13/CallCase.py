# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os
import sys

import json,jsonschema
jval = None

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
    from jsondata.JSONPatch import JSONPatch,JSONPatchItem,JSONPatchItemRaw,JSONPatchItemException
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

        ref = repr(configdata)
        ref = """{u'foo': u'bar'}"""
        assert ref == repr(configdata)

    def testCase001(self):
        """Assemble patch list, Invalid JSON Patch Document
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        
        try:
            jsonpatchlist += JSONPatchItemRaw("""{ "op": "add", "path": "/baz", "value": "qux", "op": "remove" }""")
        except JSONPatchItemException as e:
            pass

    def testCase002(self):
        """Assemble patch list, Invalid JSON Patch Document
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        
        try:
            jsonpatchlist += JSONPatchItemRaw("""{ "op": "add", "path": "/baz", "value": "qux", "value": "qux" }""")
        except JSONPatchItemException as e:
            pass

    def testCase003(self):
        """Assemble patch list, Invalid JSON Patch Document
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        
        try:
            jsonpatchlist += JSONPatchItemRaw("""{ "op": "add", "path": "/baz", "value": "qux", "path": "/baz" }""")
        except JSONPatchItemException as e:
            pass



#
#######################
#
if __name__ == '__main__':
    unittest.main()
