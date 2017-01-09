"""Verifies 'jsondata --selftest'.
"""
from __future__ import absolute_import

import unittest
import os
import sys


if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
import jsonschema


jval = None

from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF

# name of application, used for several filenames as MODE_SCHEMA_DRAFT4
_APPNAME = "jsondc"
appname = _APPNAME
#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        """Selftest.
        """
        p = os.path.abspath(__file__)
        p = os.path.dirname(p)
        p = os.path.dirname(p)
        p = os.path.dirname(p)
        p = os.path.dirname(p)
        p = os.path.dirname(p)
        p = os.path.dirname(p)
        if sys.platform == 'win32':
            call = 'set PYTHONPATH=%PYTHONPATH%;'+str(p)+';python '+str(p)+os.sep+'bin'+os.sep+'jsondc --selftest'
        else:
            call = 'export PYTHONPATH=$PYTHONPATH:'+str(p)+';python '+str(p)+os.sep+'bin'+os.sep+'jsondc --selftest'
        #print call
        exit_code = os.system(call)
        assert exit_code == 0

#
#######################
#
if __name__ == '__main__':
    unittest.main()
