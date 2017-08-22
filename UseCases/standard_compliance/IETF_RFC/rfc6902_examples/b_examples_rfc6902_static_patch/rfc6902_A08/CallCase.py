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

        kwargs = {}
        kwargs['data_file'] = os.path.dirname(__file__)+os.sep+'data.json'
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)

        ref = repr(configdata)
        ref = """{u'foo': [u'a', 2, u'c'], u'baz': u'qux'}"""
        assert ref == repr(configdata)

    def testCase001(self):
        """Assemble patch list
        """
        global configdata
        global appname
        global jsonpatchlist

        #
        # assemble patches
        jsonpatchlist  = JSONPatch()
        jsonpatchlist += JSONPatchItem("replace", "/baz", "boo")
        jsonpatchlist += JSONPatchItem("test", "/foo/1", 2)
        ref=repr(jsonpatchlist)
        ref = """[{u'op': u'replace', u'path': u'/baz', u'value': u'boo'}, {u'op': u'test', u'path': u'/foo/1', u'value': 2}]"""
        assert ref == repr(jsonpatchlist) # the complete patch list

    def testCase002(self):
        """Apply patch list
        """
        global configdata
        global appname
        global jsonpatchlist

        cnt,failed = jsonpatchlist.apply(configdata) # apply all patches
        ref=repr(configdata)
        ref = """{u'foo': [u'a', 2, u'c'], u'baz': u'boo'}"""
        assert cnt == 2 # number of patch items
        assert failed == [] # list of failed patch items
        assert ref == repr(configdata) # the final result of cumulated patches


#
#######################
#
if __name__ == '__main__':
    unittest.main()
