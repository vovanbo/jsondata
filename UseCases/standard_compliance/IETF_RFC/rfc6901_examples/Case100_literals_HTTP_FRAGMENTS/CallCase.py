# -*- coding: utf-8 -*-
"""Standards tests from RFC6901 for compliance of pointer syntax.

This case covers in particular the standard contained examples.
For fragments notation of RFC6901/RFC3986::

  #            // the whole document            
  #/foo        ["bar", "baz"]
  #/foo/0      "bar"
  #/           0
  #/a~1b       1
  #/c%25d      2
  #/e%5Ef      3
  #/g%7Ch      4
  #/i%5Cj      5
  #/k%22l      6
  #/%20        7
  #/m~0n       8

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
        kwargs['data_file'] = os.path.dirname(__file__)+os.sep+'rfc6901.json'
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)

    def testCase900(self):
        """JSONPointers: "#"
        """
        jp = JSONPointer('#')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """{u'': 0, u' ': 7, u'c%d': 2, u'a/b': 1, u'k"l': 6, u'm~n': 8, u'g|h': 4, u'e^f': 3, u'foo': [u'bar', u'baz'], u'i\\\\j': 5}"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase901(self):
        """JSONPointers: "#/foo"
        """
        jp = JSONPointer('#/foo')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """[u'bar', u'baz']"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase902(self):
        """JSONPointers: "#/foo/0"
        """
        jp = JSONPointer('#/foo/0')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """u'bar'"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase903(self):
        """JSONPointers: "#/"
        """
        jp = JSONPointer('#/')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """0"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase904(self):
        """JSONPointers: "#/a~1b"
        """
        jp = JSONPointer('#/a~1b')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """1"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase905(self):
        """JSONPointers: "#/c%25d"
        """
        jp = JSONPointer('#/c%25d')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """2"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase906(self):
        """JSONPointers: "#e%5Ef"
        """
        jp = JSONPointer('#e%5Ef')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """3"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase907(self):
        """JSONPointers: "#g%7Ch"
        """
        jp = JSONPointer('#g%7Ch')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """4"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase908(self):
        """JSONPointers: "#m~0n"
        """
        jp = JSONPointer('#m~0n')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """8"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase909(self):
        """JSONPointers: "#i%5Cj"
        """
        jp = JSONPointer('#i%5Cj')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """5"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase910(self):
        """JSONPointers: "#k%22l"
        """
        jp = JSONPointer('#k%22l')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """6"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc

    def testCase911(self):
        """JSONPointers: "#%20"
        """
        jp = JSONPointer('#%20')
        jdata=jp.get_node_or_value(configdata.data)
        jdoc = """7"""
        #print "<"+repr(jdata)+">"
        #print "<"+jdoc+">"

        assert  repr(jdata) == jdoc


#
#######################
#
if __name__ == '__main__':
    unittest.main()
