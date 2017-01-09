"""Pretty print self.schema.
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
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):


    #
    # Create by object
    #
    def testCase000(self):
        """Create a configuration object, load again by provided filelist.

        Load parameters:

        * appname = 'jsondc'

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
        pass

    #
    # Data verification
    #

    def testCase950(self):
        """Print into a string for assertion.
        """
        oout = sys.stdout
        sys.stdout = StringIO()
        configdata.printSchema()
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
