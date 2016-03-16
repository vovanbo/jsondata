"""Load and access data.
"""
from __future__ import absolute_import

import unittest
import os
import sys

import json,jsonschema
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

        assert configdata.data["phoneNumber"][0]["type"] == "home0"
        assert configdata.data["phoneNumber"][0]["number"] == "000"
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

    def testCase922(self):
        """Access some entries by dynamic references from raw data file read.
        """
        global configdata

        print "#---------------a"
        for l in ['domestic','abroad',]:
            for n in [0,1,]:
                cdata = configdata.data["customers"][l][n]["name"]
                jdata = jval["customers"][l][n]["name"]
                assert cdata == jdata 
        
                cdata = configdata.data["customers"][l][n]["industries"]
                jdata = configdata.data["customers"][l][n]["industries"]
                assert cdata == jdata 
        
                for p in [0,1,]:
                    cdata = configdata.data["customers"][l][n]["products"][p]["name"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["name"]
                    assert cdata == jdata 
             
                    cdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                    assert cdata == jdata 
             
                    cdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                    assert cdata == jdata 



#
#######################
#
if __name__ == '__main__':
    unittest.main()
