# -*- coding: utf-8 -*-
"""Standards tests from RFC6902 for compliance of patch syntax.

"""
from __future__ import absolute_import

import unittest
import os

jval = None

try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF
    from jsondata.JSONPointer import JSONPointer
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
        """Create an object for data only - no schema.
        """
        global configdata
        global appname

        kargs = {}
        kargs['datafile'] = os.path.dirname(__file__)+os.sep+'datafile.json'
        kargs['nodefaultpath'] = True
        kargs['nosubdata'] = True
        kargs['pathlist'] = os.path.dirname(__file__)
        kargs['validator'] = MODE_SCHEMA_OFF
        configdata = ConfigData(appname,**kargs)

        ref = """{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        
        assert ref == repr(configdata)

    def testCase001(self):
        """Create a new branch
        """
        global configdata
        global appname
        global jsonpatchlist


        nx = { 'a': [ {u"home": u"000-111-222"} ] }
        
        #
        # create
        nbranch = configdata.branch_create(
                    JSONPointer("/phoneNumber").get_node(configdata.data),
                    JSONPointer("/-/skype/-"),
                    JSONPointer(['a', 0]).get_node(nx)) 
        
        nrepr = """[{u'home': u'000-111-222'}]"""
        crepr="""{u'phoneNumber': [{u'type': u'home', u'number': u'212 555-1234'}, {u'type': u'office', u'number': u'313 444-555'}, {u'type': u'mobile', u'number': u'777 666-555'}, {u'skype': [{u'home': u'000-111-222'}]}], u'address': {u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}}"""
        
        assert nrepr == repr(nbranch)
        assert crepr == repr(configdata) 
        assert crepr == repr(configdata.data) 

if __name__ == '__main__':
    unittest.main()
