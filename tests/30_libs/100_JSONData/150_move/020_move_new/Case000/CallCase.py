"""Move branches by jsondata.JSONDataSerializer.branch_move().
"""
from __future__ import absolute_import

import unittest
import os
import sys

# pre-set the base JSON libraries for 'jsondata' by PyUnit call 
if 'ujson' in sys.argv:
    import ujson as myjson
elif 'json' in sys.argv:
    import json as myjson
else:
    import json as myjson
import jsonschema

# import 'jsondata'
from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_DRAFT4
from jsondata.JSONDataExceptions import JSONDataKeyError

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_copy.
    """
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        """Load initial main/master data, and validate it with standard draft4.
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

    def testCase500(self):
        """Import another branch into memory and move into the initial master data.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch1.json'
          #---
            [
                {
                  "type":"home2",
                  "number":"222 222-333"
                }
            ]
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # branch to be added
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['datafile'] = datafile
        kargs['nosubdata'] = True
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        # load branch data into memory
        branchdata = ConfigData(appname,**kargs)
        bdata="""{u'phoneNumber': [{u'type': u'home0', u'number': u'111 222-333'}]}"""
        assert repr(branchdata.data) == bdata

        #move branch to target
        target = configdata['phoneNumber'] # target container
        ret = configdata.branch_move(target, '-', branchdata['phoneNumber'], 0)
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'111 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase501(self):
        """Import another branch into memory and copy into the initial master data.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch1.json'
          #---
            [
                {
                  "type":"home2",
                  "number":"222 222-333"
                }
            ]
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # branch to be added
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch1.json')

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['datafile'] = datafile
        kargs['nosubdata'] = True
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        # load branch data into memory
        branchdata = ConfigData(appname,**kargs)
        assert repr(branchdata.data) == """[{u'type': u'home1', u'number': u'222 222-333'}]"""

        #move branch to target
        target = configdata['phoneNumber'] # target container
        ret = configdata.branch_move(target, '-', branchdata.data, 0)
        assert ret == True

        b_dat = repr(branchdata)
        b_dat = """[]"""
        assert repr(branchdata) == b_dat

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'111 222-333'}, {u'type': u'home1', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase502(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            [
                {
                  "type":"home2",
                  "number":"333 222-333"
                }
            ]
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # branch to be added
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')

        # import settings
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['datafile'] = datafile
        kargs['nosubdata'] = True
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        # load branch data into memory
        branchdata = ConfigData(appname,**kargs)
        assert repr(branchdata.data) == """[{u'type': u'home2', u'number': u'333 222-333'}]"""


        #move branch to target
        target = configdata.data['phoneNumber'] # target container
        ret = configdata.branch_move(target, '-', branchdata.data, 0)
        assert ret == True

        b_dat = repr(branchdata)
        b_dat = """[]"""
        assert repr(branchdata) == b_dat

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'111 222-333'}, {u'type': u'home1', u'number': u'222 222-333'}, {u'type': u'home2', u'number': u'333 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase510(self):
        """Import a branch with erroneous key, must not change any state.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            [
                {
                  "type":"home2",
                  "number":"333 222-333"
                }
            ]
          #---

        with key:
            'phoneNumber'

        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # import settings
        branchfile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')
        kargs = {}
        kargs['schema'] = schema
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['datafile'] = branchfile
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        branchdata = ConfigData(appname,**kargs)
        assert repr(branchdata.data) == """[{u'type': u'home2', u'number': u'333 222-333'}]"""

        # target container
        target = configdata.data['phoneNumber']

        # do it...
        try:
            ret = configdata.branch_move(target, 'phoneNumber', branchfile, 0)
        except JSONDataKeyError as e:
            pass
        try:
            assert ret != True
        except UnboundLocalError:
            pass

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home0', u'number': u'111 222-333'}, {u'type': u'home1', u'number': u'222 222-333'}, {u'type': u'home2', u'number': u'333 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

if __name__ == '__main__':
    unittest.main()
