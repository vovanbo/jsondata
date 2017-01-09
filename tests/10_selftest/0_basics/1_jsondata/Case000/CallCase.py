"""Load a data file and access the data.
"""
from __future__ import absolute_import

import unittest
import os
import sys

#
if 'ujson' in sys.argv:
    import ujson as myjson
else:
    import json as myjson
#import jsonschema


#
#######################
#
class CallUnits(unittest.TestCase):


    def testCase000(self):
        """Read a data file.
        """
        global jval

        # data
        datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('datafile.json')
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

    def testCase900(self):
        """Access some entries.
        """
        global jval

        assert jval["address"]["streetAddress"] == "21 2nd Street"
        assert jval["address"]["city"] == "New York"
        assert jval["address"]["houseNumber"] == 12

    def testCase901(self):
        """Access another some entries.
        """
        global jval

        assert jval["phoneNumber"][0]["type"] == "home"
        assert jval["phoneNumber"][0]["number"] == "212 555-1234"
        pass


#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()


