"""Add an existing entry again.
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

from jsondata.serializer import JSONDataSerializer as ConfigData
from jsondata.serializer import MODE_SCHEMA_DRAFT4

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

        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('data_file.json')
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')

        kwargs = {}
        kwargs['data_file'] = datafile
        kwargs['schema_file'] = schemafile
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_DRAFT4
        configdata = ConfigData(appname,**kwargs)

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase100(self):
        """Load and add branch with failure.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        branchfile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch
        schema = { 'phoneNumber':configdata.schema['properties']['phoneNumber'] }

        kwargs = {}
        kwargs['schema'] = schema
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['data_file'] = branchfile
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_DRAFT4
        branchdata = ConfigData(appname,**kwargs)

        target = configdata.data
        tconf = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(target) == tconf
        
        ret = configdata.branch_replace(target, 'phoneNumber', branchdata['phoneNumber'])
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'111 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass
    
#
#######################
#
if __name__ == '__main__':
    unittest.main()
