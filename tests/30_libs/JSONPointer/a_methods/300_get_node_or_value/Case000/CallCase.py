"""Basic operator __add__ tests.
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

try:
    from jsondata.pointer import JSONPointer
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n")
try:
    from jsondata.serializer import JSONDataSerializer as ConfigData
    from jsondata.serializer import MODE_SCHEMA_OFF
except Exception as e:
    print("\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n")

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
        kwargs['schema_file'] = os.path.dirname(__file__)+os.sep+'testdata.jsd'
        kwargs['no_default_path'] = True
        kwargs['nosubdata'] = True
        kwargs['path_list'] = os.path.dirname(__file__)
        kwargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kwargs)
        dummy4debugbreak = 0
        pass

    def testCase900(self):
        """Access by constant references and by pointer.
        """
        global configdata

        # in mem
        assert configdata.data["address"]["streetAddress"] == "21 2nd Street"
        
        # by pointer
        jsonptr = JSONPointer('/address/streetAddress')
        if not jsonptr:
            raise BaseException("Failed to create JSONPointer")    
        jsonptrdata = jsonptr.get_node_or_value(configdata.data)
        jsx=str(jsonptrdata)
        assert jsx == configdata.data["address"]["streetAddress"]

        # now in one line
        assert configdata.data["address"]["streetAddress"] == JSONPointer('/address/streetAddress').get_node_or_value(configdata.data)

    def testCase901(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["type"] == "home0"
        assert configdata.data["phoneNumber"][0]["type"] == JSONPointer('/phoneNumber/0/type').get_node_or_value(configdata.data)


    def testCase902(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["number"] == "000"
        assert configdata.data["phoneNumber"][0]["number"] == JSONPointer('/phoneNumber/0/number').get_node_or_value(configdata.data)

    def testCase910(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["number"] == "000"
        assert configdata.data["phoneNumber"][0]["number"] == JSONPointer('/phoneNumber/0/number').get_node_or_value(configdata.data)

    def testCase920(self):
        """Access some entries by dynamic references from raw data file read.
        """
        global configdata

        #print "#---------------a"
        for l in ['domestic','abroad',]:
            for n in [0,1,]:
                cdata = configdata.data["customers"][l][n]["name"]
                jdata = jval["customers"][l][n]["name"]
                assert cdata == jdata
                
                #now pointer
                assert configdata.data["customers"][l][n]["name"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/name').get_node_or_value(configdata.data)
        
                cdata = configdata.data["customers"][l][n]["industries"]
                jdata = configdata.data["customers"][l][n]["industries"]
                assert cdata == jdata 

                #now pointer
                assert configdata.data["customers"][l][n]["industries"] == JSONPointer('/customers/'+str(l)+'/'+str(n)+'/industries').get_node_or_value(configdata.data)
        
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
