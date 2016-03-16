"""Basic operator __add__ tests.
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

    def testCase920(self):
        """Access some entries by dynamic references from raw data file read.
        """
        global configdata

        print "#---------------a"
        for l in ['domestic','abroad',]:
            for n in [0,1,]:
                cdata = configdata.data["customers"][l][n]["name"]
                jdata = jval["customers"][l][n]["name"]
                assert cdata == jdata
                
                #now pointer
                assert configdata.data["customers"][l][n]["name"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/name').get_node_or_value(configdata.data)
        
                #now pointer with add
                jp = JSONPointer('/customers')+l+n+'name'
                assert configdata.data["customers"][l][n]["name"] == jp.get_node_or_value(configdata.data)

                #now pointer with add
                assert configdata.data["customers"][l][n]["name"] == (JSONPointer('/customers')+l+n+'name').get_node_or_value(configdata.data)
                
                cdata = configdata.data["customers"][l][n]["industries"]
                jdata = configdata.data["customers"][l][n]["industries"]
                assert cdata == jdata 

                #now pointer
                assert configdata.data["customers"][l][n]["industries"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/industries').get_node_or_value(configdata.data)
        
                #now pointer add
                assert configdata.data["customers"][l][n]["industries"] == (JSONPointer('/customers')+l+n+'industries').get_node_or_value(configdata.data)

                for p in [0,1,]:
                    cdata = configdata.data["customers"][l][n]["products"][p]["name"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["name"]
                    assert cdata == jdata 

                    #now pointer
                    assert configdata.data["customers"][l][n]["products"][p]["name"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/products/'+str(p)+'/name').get_node_or_value(configdata.data)
             
                    cdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                    assert cdata == jdata 

                    #now pointer
                    assert configdata.data["customers"][l][n]["products"][p]["quantities"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/products/'+str(p)+'/quantities').get_node_or_value(configdata.data)
             
                    cdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                    jdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                    assert cdata == jdata 

                    #now pointer
                    assert configdata.data["customers"][l][n]["products"][p]["priority"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/products/'+str(p)+'/priority').get_node_or_value(configdata.data)


#
#######################
#
if __name__ == '__main__':
    unittest.main()
