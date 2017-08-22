"""Pretty print self.schema.
"""


import unittest
import os, sys
from io import StringIO

import json #,jsonschema
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

    #
    # Create by object
    #
    def testCase000(self):
        """Create a configuration object, load again by provided file_list.

        Load parameters:

        * appname = 'jsondatacheck'

        * kwargs['file_list'] = ['testdata.json']

        * kwargs['no_default_path'] = True

        * kwargs['nosubdata'] = True

        * kwargs['path_list'] = os.path.dirname(__file__)

        * kwargs['validator'] = ConfigData.MODE_SCHEMA_OFF

        """
        global jval
        global sval
        global configdata
        global appname

        kwargs = {}
        kwargs['file_list'] = ['testdata.json']
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_DRAFT4
        configdata = ConfigData(appname,**kwargs)
        pass

    #
    # Data verification
    #

    def testCase950(self):
        """Print into a string for assertion.
        """
        oout = sys.stdout
        sys.stdout = StringIO()
        configdata.print_schema()
        sout = sys.stdout.getvalue()
        sys.stdout = oout

        #srepr = repr(configdata.schema)
        #print srepr
        srepr = """{u'required': False, u'_comment': u'This is a comment to be dropped by the initial scan:object(0)', u'_doc': u'Concatenated for the same instance.:object(0)', u'$schema': u'http://json-schema.org/draft-03/schema', u'type': u'object', u'properties': {u'phoneNumber': {u'items': {u'required': False, u'type': u'object', u'properties': {u'type': {u'required': False, u'type': u'string'}, u'number': {u'required': False, u'type': u'string'}}}, u'_comment': u'This is a comment(1):array', u'required': False, u'type': u'array'}, u'address': {u'_comment': u'This is a comment(0):address', u'required': True, u'type': u'object', u'properties': {u'city': {u'required': True, u'type': u'string'}, u'streetAddress': {u'required': True, u'type': u'string'}, u'houseNumber': {u'required': False, u'type': u'number'}}}}}"""

        assert srepr == repr(configdata.schema)


#
#######################
#

if __name__ == '__main__':
    unittest.main()
