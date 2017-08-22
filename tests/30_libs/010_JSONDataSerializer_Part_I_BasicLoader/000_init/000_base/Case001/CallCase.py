"""Load and validate JSON data from files, access to entries.
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
from jsondata.serializer import MODE_SCHEMA_OFF,MODE_SCHEMA_DRAFT4,MODE_SCHEMA_DRAFT3

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
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('data_file.json')
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

    def testCase010(self):
        """Load a schema file.
        """
        global sval
        global datafile
        global schemafile

        # schema
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')
        if not os.path.isfile(schemafile):
            raise BaseException("Missing JSONschema:file="+str(schemafile))
        with open(schemafile) as schema_file:
            sval = myjson.load(schema_file)
        if sval == None:
            raise BaseException("Failed to load schema:"+str(schema_file))


    def testCase020(self):
        """Create an object for data only - no schema - ConfigData.MODE_SCHEMA_OFF.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        kwargs = {}
        kwargs['data_file'] = datafile
        kwargs['schema_file'] = schemafile
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)

    def testCase030(self):
        """Replace object with a new including validator - ConfigData.MODE_SCHEMA_DRAFT4.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        kwargs = {}
        kwargs['data_file'] = datafile
        kwargs['schema_file'] = schemafile
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_DRAFT4
        configdata = ConfigData(appname,**kwargs)

    def testCase040(self):
        """Replace object with a new including validator - ConfigData.MODE_SCHEMA_DRAFT3.
        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        kwargs = {}
        kwargs['data_file'] = datafile
        kwargs['schema_file'] = schemafile
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_DRAFT3
        configdata = ConfigData(appname,**kwargs)


    def testCase900(self):
        """Access data by static references.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        assert configdata.data["address"]["city"] == "New York"
        assert configdata.data["address"]["houseNumber"] == 12

    def testCase901(self):
        """Access another data by static references.
        """
        global configdata

        assert configdata.data["phoneNumber"][0]["type"] == "home"
        assert configdata.data["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase920(self):
        """Access data by dynamic references.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == jval["address"]["streetAddress"]
        assert configdata.data["address"]["city"] == jval["address"]["city"]
        assert configdata.data["address"]["houseNumber"] == jval["address"]["houseNumber"]

    def testCase921(self):
        """Access another data by dynamic references.
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
