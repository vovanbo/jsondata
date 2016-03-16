"""Load, verify, and compare data and schema with raw calls,
and by encapsulation via a container object.

Validator: jsonschema.MODE_SCHEMA_DRAFT3Validator
"""
from __future__ import absolute_import

import unittest
import os
#import sys

import json #,jsonschema
jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_DRAFT3
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
    # Create raw
    #
    def testCase000(self):
        """Load persistent data from files into into memory.
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

    def testCase001(self):
        """Load persistent schema from files into into memory.
        """
        global sval
        global datafile
        global schemafile

        # schema
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')
        if not os.path.isfile(schemafile):
            raise BaseException("Missing JSONschema:file="+str(schemafile))
        with open(schemafile) as schema_file:
            sval = json.load(schema_file)
        if sval == None:
            raise BaseException("Failed to load schema:"+str(schema_file))

    #
    # Create by object
    #
    def testCase050(self):
        """Create a configuration object, load again by provided filelist.

        Load parameters:

        * appname = 'jsondatacheck'

        * kargs['datafile'] = datafile

        * kargs['schemafile'] = schemafile

        * kargs['nodefaultpath'] = True

        * kargs['nosubdata'] = True

        * kargs['pathlist'] = os.path.dirname(__file__)

        * kargs['validator'] = ConfigData.MODE_SCHEMA_DRAFT3

        """
        global jval
        global sval
        global configdata
        global appname
        global schemafile

        kargs = {}
        kargs['datafile'] = datafile
        kargs['schemafile'] = schemafile
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_DRAFT3
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

    def testCase920(self):
        """Check 'address' loaded from JSON data file:
        -> configdata.data["address"]'.
        """
        global configdata

        assert configdata.data["address"]["streetAddress"] == jval["address"]["streetAddress"]
        assert configdata.data["address"]["city"] == jval["address"]["city"]
        assert configdata.data["address"]["houseNumber"] == jval["address"]["houseNumber"]

    def testCase921(self):
        """Check 'phoneNumber' loaded from JSON data file:
        -> configdata.data["phoneNumber"]'.
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
