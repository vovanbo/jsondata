"""Basic operator tests for: __ge__
"""
from __future__ import absolute_import

import unittest
import os
import sys

import json,jsonschema
jval = None

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"

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
        """Load a data file.
        """
        global jval
        global datafile

        # data
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('testdata.json')
        if not os.path.isfile(datafile):
            raise BaseException("Missing JSON data:file="+str(datafile))
        # load data
        with open(datafile) as data_file:
            jval = json.load(data_file)
        if jval == None:
            raise BaseException("Failed to load data:"+str(data_file))

        jval = jval
        assert jval
        pass

    def testCase002(self):
        """Create an object for data only - no schema.
        """
        global jval
        global sval
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'testdata.json'
        kargs['schemafile'] = os.path.dirname(__file__)+os.sep+'testdata.jsd'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)
        dummy4debugbreak = 0
        pass

    def testCase900(self):
        """Compare with an additional trailing '/'.
        """
        jp = JSONPointer('/address/streetAddress')
        assert  jp == '/address/streetAddress' 


    def testCase907(self):
        """Compare with an implicit leading '/'.
        """
        jp = JSONPointer('address/streetAddress')
        # now in one line
        assert  jp == '/address/streetAddress'

    def testCase908(self):
        """Compare with an implicit leading '/'.
        """
        jp = JSONPointer('address/streetAddress')
        # now in one line
        assert  jp == '/address/streetAddress'

    def testCase909(self):
        """Compare with an implicit leading '/'.
        """
        jp = JSONPointer('/address/streetAddress')
        # now in one line
        assert  jp == '/address/streetAddress'

    def testCase910(self):
        """Compare with an additional trailing '/'.
        """
        jp = JSONPointer('/address/streetAddress')
        assert '/address/streetAddress' == jp 

    def testCase917(self):
        """Compare with an implicit leading '/'.
        """
        jp = JSONPointer('address/streetAddress')
        # now in one line
        assert '/address/streetAddress' == jp

    def testCase918(self):
        """Compare with an implicit leading '/'.
        """
        jp = JSONPointer('address/streetAddress')
        # now in one line
        assert '/address/streetAddress' == jp


#
#######################
#
if __name__ == '__main__':
    unittest.main()
