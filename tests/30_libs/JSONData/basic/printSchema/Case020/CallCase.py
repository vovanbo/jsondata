"""Pretty print data read from 'source'.
"""


import unittest
import os, sys
from io import StringIO

#
if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
#import jsonschema
jval = None

from jsondata.serializer import JSONDataSerializer as ConfigData
from jsondata.serializer import MODE_SCHEMA_OFF

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
        """Create a configuration object, load again by provided file_list.

        Load parameters:

        * appname = 'jsondc'

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
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)


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
        
        source = open(os.path.dirname(__file__)+os.sep+"testdata.json").read()
        source = myjson.loads(source)
        kwargs = {'source':source}
        configdata.print_data(**kwargs)
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
        #print "sout<"+sout+">"
        #print "conf_out<"+conf_out+">"

        assert conf_out == sout


#
#######################
#

if __name__ == '__main__':
    unittest.main()
