"""Export of jsondata.
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

from jsondata.JSONData import JSONData
from jsondata.JSONPointer import JSONPointer
from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_DRAFT4,MODE_SCHEMA_OFF

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
        kargs['schemafile'] = schemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4

        configdata = ConfigData(appname,**kargs)

        assert repr(configdata.data) == "{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"
        pass

    def testCase001(self):
        """Import another branch into initial main/master data, and validate it with branch schema.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

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
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch1.json')
        ret = configdata.json_import(target, '-', datafile, None, **kargs)
        assert ret == True

        # expected - after branch_add_only the same state as before
        conf_dat = repr(configdata.data)
        conf_dat = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'type': u'home2', u'number': u'222 222-333'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        assert repr(configdata.data) == conf_dat
        pass

    def testCase100(self):
        """Export the document.
        """
        global configdata
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export-doc.json')
        ret = configdata.json_export(None, datafile)
        assert ret == True

    def testCase101(self):
        """Export a branch.
        """
        global configdata
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export-doc.json')

        branch = JSONPointer('/phoneNumber/0').get_node(configdata.data)
        ret = configdata.json_export(branch, datafile)
        assert ret == True

    def testCase200(self):
        """Load exported data for verification.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export-doc.json')

        kargs = {}
        kargs['datafile'] = datafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF

        # previous exported branch
        exported = ConfigData(appname,**kargs)

        # original branch
        branch = JSONPointer('/phoneNumber/0').get_node(configdata.data)

        # do a deep compare of branches
        dx = JSONData.getTreeDiff(exported.data, branch)
        assert dx
        pass

if __name__ == '__main__':
    unittest.main()
