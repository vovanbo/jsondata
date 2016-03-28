"""Import of branches by jsondata.JSONDataSerializer.branch_import().
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
        """Create an object by load of JSON data and JSONschema from files, finally validate.
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

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase100(self):
        """Load and import data file, use in-memory schema for validation - ConfigData.BRANCH_REMOVE.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch
        schema = { 'phoneNumber':configdata.schema['properties']['phoneNumber'] }

        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        target = configdata.data
        configdata.json_import(target, None, datafile, None, **kargs)

        # Expected the nodes within the datafile to be removed.
        # No content is checked, just the complete tree is removed.
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'111 222-333'}]}"""
        assert repr(configdata.data) == conf_dat

#
#######################
#
if __name__ == '__main__':
    unittest.main()
