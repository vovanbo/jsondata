"""Simple print schema read from 'sourcefile'.
"""
from __future__ import absolute_import

import unittest
import os, sys
from StringIO import StringIO

import json #,jsonschema
jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_DRAFT4

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

    #
    # Create by object
    #
    def testCase000(self):
        """Create a configuration object, load again by provided filelist.

        Load parameters:

        * appname = 'jsondatacheck'

        * kargs['filelist'] = ['testdata.json']

        * kargs['nodefaultpath'] = True

        * kargs['nosubdata'] = True

        * kargs['pathlist'] = os.path.dirname(__file__)

        * kargs['validator'] = ConfigData.MODE_SCHEMA_OFF

        """
        global jval
        global sval
        global configdata
        global appname

        kargs = {}
        kargs['filelist'] = ['testdata.json']
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4
        configdata = ConfigData(appname,**kargs)


    #
    # Data verification
    #

    def testCase910(self):
        """Check 'address' literally:
        -> configdata.data["address"]'.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

    def testCase911(self):
        """Check 'phoneNumber' literally:
        -> configdata.data["phoneNumber"]'.
        """
        global configdata

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase950(self):
        """Print into a string for assertion.
        """
        #global configdata

        oout = sys.stdout
        sys.stdout = StringIO()
        
        kargs = {'sourcefile':os.path.dirname(__file__)+os.sep+"testdata.jsd" }
        configdata.printSchema(False,**kargs)
        sout = sys.stdout.getvalue()
        sys.stdout = oout
        conf_out = """{"required": false, "_comment": "This is a comment to be dropped by the initial scan:object(0)", "_doc": "Concatenated for the same instance.:object(0)", "$schema": "http://json-schema.org/draft-03/schema", "type": "object", "properties": {"phoneNumber": {"items": {"required": false, "type": "object", "properties": {"type": {"required": false, "type": "string"}, "number": {"required": false, "type": "string"}}}, "_comment": "This is a comment(1):array", "required": false, "type": "array"}, "address": {"_comment": "This is a comment(0):address", "required": true, "type": "object", "properties": {"city": {"required": true, "type": "string"}, "streetAddress": {"required": true, "type": "string"}, "houseNumber": {"required": false, "type": "number"}}}}}
"""
#         print "sout<"+sout+">"
#         print "conf_out<"+conf_out+">"

        assert conf_out == sout


#
#######################
#

if __name__ == '__main__':
    unittest.main()
