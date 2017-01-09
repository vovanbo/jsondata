# -*- coding: utf-8 -*-
"""Standards tests from RFC6901 for compliance of pointer syntax.

This case covers in particular the standard contained examples.
For JSON notation of RFC6901::

  ""           // the whole document
  "/foo"       ["bar", "baz"]
  "/foo/0"     "bar"
  "/"          0
  "/a~1b"      1
  "/c%d"       2
  "/e^f"       3
  "/g|h"       4
  "/i\\j"      5
  "/k\"l"      6
  "/ "         7
  "/m~0n"      8

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
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

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
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'rfc6901.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

    def testCase900(self):
        """JSONPointers: ""
        """
        jp = JSONPointer('')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """{u'': 0, u' ': 7, u'c%d': 2, u'a/b': 1, u'k"l': 6, u'm~n': 8, u'g|h': 4, u'e^f': 3, u'foo': [u'bar', u'baz'], u'i\\\\j': 5}"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase901(self):
        """JSONPointers: "/foo"
        """
        jp = JSONPointer('/foo')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """[u'bar', u'baz']"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase902(self):
        """JSONPointers: "/foo/0"
        """
        jp = JSONPointer('/foo/0')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """u'bar'"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase903(self):
        """JSONPointers: "/"
        """
        jp = JSONPointer('/')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """0"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase904(self):
        """JSONPointers: "/a~1b"
        """
        jp = JSONPointer('/a~1b')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """1"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase905(self):
        """JSONPointers: "/c%d"
        """
        jp = JSONPointer('/c%d')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """2"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase906(self):
        """JSONPointers: "e^f"
        """
        jp = JSONPointer('e^f')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """3"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase907(self):
        """JSONPointers: "g|h"
        """
        jp = JSONPointer('g|h')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """4"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase908(self):
        """JSONPointers: "m~0n"
        """
        jp = JSONPointer('m~0n')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """8"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
