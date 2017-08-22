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
_APPNAME = "jsondc"
appname = _APPNAME

#
#######################
#
class CallUnits(unittest.TestCase):


    #
    # Create by object
    #
    def testCase000(self):
        """Create a configuration object, load again by provided filelist.

        Load parameters:

        * appname = 'jsondc'

        * kargs['filelist'] = ['testdata.json']

        * kargs['nodefaultpath'] = True

        * kargs['nosubdata'] = True

        * kargs['pathlist'] = os.path.dirname(__file__)

        * kargs['validator'] = ConfigData.MODE_SCHEMA_OFF

        """
        global jval
        global sval
        global configdata
        global appname

        kargs = {}
        kargs['filelist'] = ['testdata.json']
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)


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
