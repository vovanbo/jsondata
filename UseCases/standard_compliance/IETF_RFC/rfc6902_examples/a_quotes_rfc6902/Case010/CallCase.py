# -*- coding: utf-8 -*-
"""Extensions for standards tests from RFC6901.

This case covers in particular extensions to the standard contained
examples. 

For JSON notation of RFC6901::

  { "": { "": ["doubleempty0", "doubleempty1"] } }

Pointer access::

  ""       { "": { "": ["doubleempty0", "doubleempty1"] } }
  "/"            { "": ["doubleempty0", "doubleempty1"] }
  "//"                 ["doubleempty0", "doubleempty1"]
  "//0"                 "doubleempty0"
  "//1"                                 "doubleempty1"

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
        kwargs['data_file'] = os.path.dirname(__file__)+os.sep+'rfc6901ext.json'
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """{u'': {u'': [u'doubleempty0', u'doubleempty1']}}"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase901(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """{u'': [u'doubleempty0', u'doubleempty1']}"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase902(self):
        """JSONPointers: "//"
        """
        jp = JSONPointer('//')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """[u'doubleempty0', u'doubleempty1']"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase903(self):
        """JSONPointers: "///0"
        """
        jp = JSONPointer('///0')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """u'doubleempty0'"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase904(self):
        """JSONPointers: "///1"
        """
        jp = JSONPointer('///1')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """u'doubleempty1'"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
