"""Pretty print self.data.
"""


import unittest
import os, sys
from io import StringIO

import json #,jsonschema
jval = None

from jsondata.serializer import JSONDataSerializer as ConfigData
from jsondata.serializer import MODE_SCHEMA_OFF

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
    # Create by object
    #
    def testCase000(self):
        """Create a configuration object, load again by provided file_list.

        Load parameters:

        * appname = 'jsondatacheck'

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

      
    def testCase912(self):
        """Check 'address' literally:
        -> configdata.data["address"]'.
        """
        global configdata

        assert repr(configdata) == repr(configdata.data)

#
#######################
#

if __name__ == '__main__':
    unittest.main()
