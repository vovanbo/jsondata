"""Load and access data.
"""


import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


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
            jval = myjson.load(data_file)
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

        kwargs = {}
        kwargs['data_file'] = os.path.dirname(__file__)+os.sep+'testdata.json'
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)

    def testCase900(self):
        """Access some entries by constant references.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

    def testCase901(self):
        """Access another some entries by constant references.
        """
        global configdata

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase920(self):
        """Access some entries by dynamic references from raw data file read.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == jval["address"]["streetAddress"]
        assert configdata.data["address"]["city"] == jval["address"]["city"]
        assert configdata.data["address"]["houseNumber"] == jval["address"]["houseNumber"]

    def testCase921(self):
        """Access another some entries by dynamic references from raw data file read.
        """
        global configdata

        assert configdata.data["phoneNumber"][0]["type"] == jval["phoneNumber"][0]["type"]
        assert configdata.data["phoneNumber"][0]["number"] == jval["phoneNumber"][0]["number"]
        pass

#
#######################
#
if __name__ == '__main__':
    unittest.main()
