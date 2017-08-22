"""Append list element.
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
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):
    """Base branch_add.
    """


    def testCase000(self):
        """Load initial main/master data, and validate it with standard draft4.
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

    def testCase500(self):
        """Import another branch into memory and add the representation into the initial master data.

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
        schema = {
            "$schema": "http://json-schema.org/draft-03/schema",
            'phoneNumber':configdata.schema['properties']['phoneNumber']
        }

        # branch to be added
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch0.json')

        # import settings
        kwargs = {}
        kwargs['schema'] = schema
        kwargs['no_default_path'] = True
        kwargs['data_file'] = datafile
        kwargs['nosubdata'] = True
        kwargs['validator'] = MODE_SCHEMA_DRAFT4

        # load branch data into memory
        branchdata = ConfigData(appname,**kwargs)
        assert branchdata.data == {'phoneNumber': [{'type': 'home', 'number': '111 222-333'}]}


        # target container
        target = configdata
        ret = configdata.branch_replace(target.data, 'phoneNumber', branchdata.data['phoneNumber'])
        assert ret == True

        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'111 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat

        pass

 
if __name__ == '__main__':
    unittest.main()
