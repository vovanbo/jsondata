"""Basic operator tests for: __iadd__
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
        
    def testCase901(self):
        """Access by constant references and by pointer.
        """
        global configdata

        # by pointer
        jsonptr = JSONPointer('/address')
        if not jsonptr:
            raise BaseException("Failed to create JSONPointer")    
        jsonptr += 'streetAddress'

        assert jsonptr == '/address/streetAddress'

    def testCase902(self):
        """Access by constant references and by pointer.
        """
        global configdata
        # now in one line
        assert configdata.data["address"]["streetAddress"] == JSONPointer('/address/streetAddress').get_node_or_value(configdata.data)

    def testCase903(self):
        """Access by constant references and by pointer.
        """
        global configdata


#
#######################
#
if __name__ == '__main__':
    unittest.main()
