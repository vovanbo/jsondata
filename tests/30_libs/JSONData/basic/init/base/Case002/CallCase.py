"""Load and validate JSON data from files.
Access to in-memory storage of schema for validation.
Read entries.
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

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_DRAFT4

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        """Create an object with validation by schemafile.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('datafile.json')
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')

        kargs = {}
        kargs['datafile'] = datafile
        kargs['schemafile'] = schemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4
        configdata = ConfigData(appname,**kargs)
        pass

    def testCase900(self):
        """Verify loaded data.
        """
        global configdata

        conf_dat = "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        assert str(configdata.data) == conf_dat

    def testCase007(self):
        """Verify loaded schema.
        """
        global configdata

        conf_schema = "{u'required': False, u'_comment': u'This is a comment to be dropped by the initial scan:object(0)', u'_doc': u'Concatenated for the same instance.:object(0)', u'$schema': u'http://json-schema.org/draft-03/schema', u'type': u'object', u'properties': {u'phoneNumber': {u'items': {u'required': False, u'type': u'object', u'properties': {u'type': {u'required': False, u'type': u'string'}, u'number': {u'required': False, u'type': u'string'}}}, u'_comment': u'This is a comment(1):array', u'required': False, u'type': u'array'}, u'address': {u'_comment': u'This is a comment(0):address', u'required': True, u'type': u'object', u'properties': {u'city': {u'required': True, u'type': u'string'}, u'streetAddress': {u'required': True, u'type': u'string'}, u'houseNumber': {u'required': False, u'type': u'number'}}}}}"
        assert str(configdata.schema) == conf_schema

#
#######################
#
if __name__ == '__main__':
    unittest.main()
