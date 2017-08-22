"""Import of new branches by jsondata.JSONDataSerializer.branch_import().
"""


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
from jsondata.serializer import JSONDataSerializer as ConfigData
from jsondata.serializer import MODE_SCHEMA_DRAFT4
from jsondata.exceptions import JSONDataKeyError,JSONDataNodeType

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondatacheck"
appname = _APPNAME

#jval = None

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch import by branch_add.
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
        kargs['schema_file'] = schemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        configdata = ConfigData(appname,**kargs)

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase500(self):
        """Import another branch into initial main/master data, and validate it with branch schema.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch1.json'
          #---
            {
              "type":"home2",
              "number":"222 222-333"
            }
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
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

        # target container
        target = configdata.data['phoneNumber']

        # do it...
        # REMARK: schema_file is here None, because we use an in memory schema,
        #         and do not export - for now
        #
        # Expect False, because the node is already present, thus 'branch_add_only'
        # has to fail.
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch1.json')
        ret = configdata.json_import(target, '-', datafile, None, **kargs)
        assert ret == True

        # expected - after branch_add_only the same state as before
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase502(self):
        """Import a branch into initial main/master data, and validate it with branch schema.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            {
              "type":"home2",
              "number":"333 222-333"
            }
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
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

        # target container
        target = configdata.data['phoneNumber']

        # do it...
        # REMARK: schema_file is here None, because we use an in memory schema,
        #         and do not export - for now
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')
        ret = configdata.json_import(target, 0, datafile, None, **kargs)
        assert ret == True

        # expected - after branch_add_only the same state as before
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home2', u'number': u'333 222-333'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase510(self):
        """Import a branch with erroneous key.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            {
              "type":"home2",
              "number":"333 222-333"
            }
          #---

        with key:
            'phoneNumber'

        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
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

        # target container
        target = configdata.data['phoneNumber']

        # do it...
        # REMARK: schema_file is here None, because we use an in memory schema,
        #         and do not export - for now
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')
        try:
            ret = configdata.json_import(target, 'phoneNumber', datafile, None, **kargs)
        except JSONDataKeyError as e:
            pass
        try:
            assert ret != True
        except UnboundLocalError:
            pass

        # expected - after branch_add failure
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home2', u'number': u'333 222-333'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase511(self):
        """Import a branch with no key and mismatch of types for 'targetnode' and 'branch'.

        Use insertion point:
          target = configdata.data['phoneNumber']

        for file:
          'branch2.json'
          #---
            {
              "type":"home2",
              "number":"333 222-333"
            }
          #---

        Apply '$schema' key for branch/subtree of master schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        # partial schema for branch, use here a subtree of main schema,
        # the entry:
        #    "$schema": "http://json-schema.org/draft-03/schema",
        # seems not to be required,
        #
        # but here just check it
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

        # target container
        target = configdata.data['phoneNumber']

        # do it...
        # REMARK: schema_file is here None, because we use an in memory schema,
        #         and do not export - for now
        # branch to be loaded
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch2.json')
        try:
            ret = configdata.json_import(target, None, datafile, None, **kargs)
        except JSONDataNodeType as e:
            pass
        try:
            assert ret != True
        except UnboundLocalError:
            pass

        # expected - after branch_add failure
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home2', u'number': u'333 222-333'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

if __name__ == '__main__':
    unittest.main()
