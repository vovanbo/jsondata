# -*- coding: utf-8 -*-
"""Standards tests from RFC7159, Chapter 13, Example 1
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
_APPNAME = "jsondatacheck"
appname = _APPNAME

configdata = None

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
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'rfc7159_13_01.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

    def testCase900(self):
        """Verify: rfc7159: Chapter 13, Example 1""
        """
        jdoc = """{u'Image': {u'Title': u'View from 15th Floor', u'IDs': [116, 943, 234, 38793], u'Height': 600, u'Width': 800, u'Animated': False, u'Thumbnail': {u'Url': u'http://www.example.com/image/481989943', u'Width': 100, u'Height': 125}}}"""
        #print "<"+repr(configdata.data)+">"
        #print "<"+jdoc+">"
        assert  repr(configdata.data) == jdoc

    def testCase901(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['Title'] == u'View from 15th Floor' 

    def testCase902(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['Height'] == 600 
        assert configdata.data['Image']['Width'] == 800 

    def testCase903(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['Animated'] == False 

    def testCase904(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert repr(configdata.data['Image']['IDs']) == '[116, 943, 234, 38793]'
        assert configdata.data['Image']['IDs'] == [116, 943, 234, 38793]

    def testCase905(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['IDs'][0] == 116
        assert configdata.data['Image']['IDs'][1] == 943
        assert configdata.data['Image']['IDs'][2] == 234
        assert configdata.data['Image']['IDs'][3] == 38793

    def testCase906(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert repr(configdata.data['Image']['Thumbnail']) == """{u'Url': u'http://www.example.com/image/481989943', u'Width': 100, u'Height': 125}""" 
        assert configdata.data['Image']['Thumbnail'] == {u'Url': u'http://www.example.com/image/481989943', u'Width': 100, u'Height': 125} 

    def testCase907(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['Thumbnail']['Url'] == u'http://www.example.com/image/481989943' 
        assert configdata.data['Image']['Thumbnail']['Width'] == 100 
        assert configdata.data['Image']['Thumbnail']['Height'] ==125

    def testCase908(self):
        """Access: rfc7159: Chapter 13, Example 1""
        """
        assert configdata.data['Image']['Title'] == u'View from 15th Floor' 
        assert configdata.data['Image']['IDs'][0] == 116
        assert configdata.data['Image']['IDs'][1] == 943
        assert configdata.data['Image']['IDs'][2] == 234
        assert configdata.data['Image']['IDs'][3] == 38793
        assert configdata.data['Image']['Height'] == 600 
        assert configdata.data['Image']['Width'] == 800 
        assert configdata.data['Image']['Animated'] == False 
        assert configdata.data['Image']['Thumbnail']['Url'] == u'http://www.example.com/image/481989943' 
        assert configdata.data['Image']['Thumbnail']['Width'] == 100 
        assert configdata.data['Image']['Thumbnail']['Height'] ==125
#
#######################
#
if __name__ == '__main__':
    unittest.main()
