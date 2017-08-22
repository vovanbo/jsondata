"""Basic operator tests for: __ge__
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

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'testdata.json'
        kargs['schema_file'] = os.path.dirname(__file__)+os.sep+'testdata.jsd'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)
        dummy4debugbreak = 0
        pass

    def testCase900(self):
        """Access by constant references and by pointer.
        """
        jp = JSONPointer('/address')
        jp = jp + 'streetAddress'
        # now in one line
        assert  not jp >= '/address' 

    def testCase901(self):
        """Access by constant references and by pointer.
        """
        jp = JSONPointer('/address') + 'streetAddress'
        # now in one line
        assert  '/address/streetAddress' <= jp

    def testCase902(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0 + 'type'
        assert  '/phoneNumber/0/type' <= jp

    def testCase903(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0
        jp = jp + 'type'
        assert  '/phoneNumber/0/type' <= jp

    def testCase904(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["number"] == "000"
        jp = JSONPointer('/phoneNumber') + 0 + 'number'        
        assert  '/phoneNumber/0/number' <= jp



#
#######################
#
if __name__ == '__main__':
    unittest.main()
