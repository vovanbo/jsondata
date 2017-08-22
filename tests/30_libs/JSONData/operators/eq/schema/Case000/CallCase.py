

import unittest
import os, sys
from io import StringIO

from jsondata.serializer import JSONDataSerializer as ConfigData
from jsondata.serializer import MODE_SCHEMA_DRAFT4

from testdata import mypath

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):

    def setUp(self):
        """Create a configuration object, load by provided file list.
        """
        global appname

        _path = mypath+os.sep+'datasets'+os.sep+'basic'+os.sep+'set00'+os.sep+'testdata.json'

        kargs = {}
        kargs['filelist'] = [_path]
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT4
        self.configdata = ConfigData(appname,**kargs)

        self.jval = None
        self.sval = None

        pass

    def testCase200_printSchema_assert(self):
        """Print schema into a string and assert.
        """
        oout = sys.stdout
        sys.stdout = StringIO()
        self.configdata.print_schema()
        sout = sys.stdout.getvalue()
        sys.stdout = oout
        conf_out = """{
    "required": false, 
    "_comment": "This is a comment to be dropped by the initial scan:object(0)", 
    "_doc": "Concatenated for the same instance.:object(0)", 
    "$schema": "http://json-schema.org/draft-03/schema", 
    "type": "object", 
    "properties": {
        "phoneNumber": {
            "items": {
                "required": false, 
                "type": "object", 
                "properties": {
                    "type": {
                        "required": false, 
                        "type": "string"
                    }, 
                    "number": {
                        "required": false, 
                        "type": "string"
                    }
                }
            }, 
            "_comment": "This is a comment(1):array", 
            "required": false, 
            "type": "array"
        }, 
        "address": {
            "_comment": "This is a comment(0):address", 
            "required": true, 
            "type": "object", 
            "properties": {
                "city": {
                    "required": true, 
                    "type": "string"
                }, 
                "streetAddress": {
                    "required": true, 
                    "type": "string"
                }, 
                "houseNumber": {
                    "required": false, 
                    "type": "number"
                }
            }
        }
    }
}
"""
#        print "sout<"+sout+">"
#        print "conf_out<"+conf_out+">"

        assert conf_out == sout


#
#######################
#

if __name__ == '__main__':
    unittest.main()
