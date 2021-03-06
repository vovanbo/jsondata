"""Import of branches by jsondata.JSONDataSerializer.branch_export().
"""

from __future__ import absolute_import

import unittest
import os
import sys

#
if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF,MODE_SCHEMA_DRAFT4
from jsondata.JSONPointer import JSONPointer

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):
    """Read in reference data and export.
    """
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Load initial main/master data, and validate it with standard validator.
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

    def testCase700(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Do not insert '$schema' key.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # partial schema for branch, use here a subtree of main schema
        schema = { 
            'phoneNumber':configdata.schema['properties']['phoneNumber'] 
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        # target container - here with one key
        target,remaining = JSONPointer("/phoneNumber/-").get_node_exist(configdata.data)

        # do it...
        # ATTENTION: works here for: remaining => one level only
        ret = True
        for k in remaining:
            ret &= configdata.json_import(target, k, datafile, None, **kargs)
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'000 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat

    def testCase701(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch1.json')

        # partial schema for branch, use here a subtree of main schema
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF

        # target container - here with one key
        target,remaining = JSONPointer("/phoneNumber/-").get_node_exist(configdata.data)

        # do it...
        # ATTENTION: works here for: remaining => one level only
        ret = True
        for k in remaining:
            ret &= configdata.json_import(target, k, datafile, None, **kargs)
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'000 222-333'}, {u'type': u'home1', u'number': u'111 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat

    def testCase702(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')

        # partial schema for branch, use here a subtree of main schema
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        # target container - here with one key
        target,remaining = JSONPointer("/phoneNumber/-").get_node_exist(configdata.data)

        # do it...
        # ATTENTION: works here for: remaining => one level only
        ret = True
        for k in remaining:
            ret &= configdata.json_import(target, k, datafile, None, **kargs)
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'000 222-333'}, {u'type': u'home1', u'number': u'111 222-333'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
    
    def testCase900(self):
        """Export complete document.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export.json')
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export.jsd')

        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # import settings
        kargs = {}
        #kargs['schema'] = schema
        #kargs['validator'] = MODE_SCHEMA_DRAFT4

        # target container
        #target = configdata.data
        target = None

        ret = configdata.json_export(target, datafile, **kargs)
        assert ret == True

        ret = configdata.json_export(schema, schemafile, **kargs)
        assert ret == True

    def testCase910(self):
        """Load initial main/master data, and validate it with standard validator.
        """
        global jval
        global sval
        global exporteddata
        global appname

        exdatafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export.json')
        exschemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export.jsd')

        kargs = {}
        kargs['datafile'] = exdatafile
        kargs['schemafile'] = exschemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        exporteddata = ConfigData(appname,**kargs)

        erepr = repr(exporteddata.data)
        #print erepr
        
        crepr = repr(configdata.data)
        #print crepr

        assert erepr == crepr
        pass


#
#######################
#
#
#######################
#


if __name__ == '__main__':
    unittest.main()
