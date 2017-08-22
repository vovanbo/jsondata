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
        # now in one line
        assert  jp > '/address/streetAddress'

    def testCase901(self):
        """Access by constant references and by pointer.
        """
        jp = JSONPointer('/address') + 'streetAddress'
        # now in one line
        assert  not jp > '/address/streetAddress'

    def testCase902(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0 
        assert  jp > '/phoneNumber/0/type'

    def testCase903(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["type"] == "home0"

        jp = JSONPointer('/phoneNumber') + 0
        jp = jp + 'type'
        assert  not jp > '/phoneNumber/0/type'

    def testCase904(self):
        """Access by constant references and by pointer.
        """
        assert configdata.data["phoneNumber"][0]["number"] == "000"
        jp = JSONPointer('/phoneNumber') + 1 + 'number'        
        assert  not jp > '/phoneNumber/0/number'



#
#######################
#
if __name__ == '__main__':
    unittest.main()
