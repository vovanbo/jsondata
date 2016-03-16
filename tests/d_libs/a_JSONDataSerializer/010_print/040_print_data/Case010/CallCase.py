"""Pretty print data read from 'sourcefile'.
"""
from __future__ import absolute_import

import unittest
import os, sys
from StringIO import StringIO

import json #,jsonschema
jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF

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
        """Create a configuration object, load again by provided filelist.

        Load parameters:

        * appname = 'jsondatacheck'

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
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)


    #
    # Data verification
    #

    def testCase910(self):
        """Check 'address' literally:
        -> configdata.data["address"]'.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

    def testCase911(self):
        """Check 'phoneNumber' literally:
        -> configdata.data["phoneNumber"]'.
        """
        global configdata

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase950(self):
        """Print into a string for assertion.
        """
        #global configdata

        oout = sys.stdout
        sys.stdout = StringIO()
        
        kargs = {'sourcefile':os.path.dirname(__file__)+os.sep+"testdata.json" }
        configdata.printData(**kargs)
        sout = sys.stdout.getvalue()
        sys.stdout = oout
        conf_out = """{
    "phoneNumber": [
        {
            "type": "home", 
            "number": "212 555-1234"
        }
    ], 
    "address": {
        "city": "New York", 
        "streetAddress": "21 2nd Street", 
        "houseNumber": 12
    }
}
"""
        print "sout<"+sout+">"
        print "conf_out<"+conf_out+">"

        assert conf_out == sout


#
#######################
#

if __name__ == '__main__':
    unittest.main()
