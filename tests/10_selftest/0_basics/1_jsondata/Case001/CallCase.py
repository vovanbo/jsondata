"""Load data file and access some data.
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

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

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

    def testCase100(self):
        """Access some entries.
        """
        global jval

        assert jval["address"]["streetAddress"] == "21 2nd Street"
        assert jval["address"]["city"] == "New York"
        assert jval["address"]["houseNumber"] == 12

    def testCase101(self):
        """Access another some entries.
        """
        global jval

        assert jval["phoneNumber"][0]["type"] == "home"
        assert jval["phoneNumber"][0]["number"] == "212 555-1234"
        pass

    def testCase500(self):
        """Read a schema file.
        """
        global sval

        # schema
        schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('datafile.json')
        if not os.path.isfile(schemafile):
            raise BaseException("Missing JSONschema:file="+str(schemafile))
        with open(schemafile) as schema_file:
            sval = myjson.load(schema_file)
        if sval == None:
            raise BaseException("Failed to load schema:"+str(schema_file))

    def testCase600(self):
        """Validate by standard API: jsonschema.validate
        """
        global sval
        global jval

        # validate data
        jsonschema.validate(jval, sval)

    def testCase700(self):
        """Validate by MODE_SCHEMA_DRAFT3 API: jsonschema.MODE_SCHEMA_DRAFT3Validator
        """
        global sval
        global jval

        # validate data
        jsonschema.Draft3Validator(jval, sval)



#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()


