# -*- coding: utf-8 -*-
"""Test of basic features for the user by '--selftest'.

This module is used by 'jsondatacheck' when the option 
'--selftest' is applied. It performs a series of hardoced 
basic functional checks by calling 'runselftest'.

The display of actions and results could be activated and 
raised by multiple repetition of the '-v' option.

The following data and schema are applied:
    0. jsondata/data.json + jsondata/schema.jsd
    1. jsondata/jsondatacheck.json + jsondata/jsondatacheck.jsd

The performed process flow is:
    0. load
    1. validate
    2. verify

By default either 'True' is returned, or in case of a failed test
and/or error condition an exception is raised.
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.0'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import os,sys
import json#,jsonschema

try:
    from jsondata.JSONPointer import JSONPointer
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
    from jsondata.JSONDataSerializer import MODE_SCHEMA_OFF,MODE_SCHEMA_DRAFT3
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
# name of application, used for several filenames as default
_APPNAME = "selftest"

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

debug = False
_verbose = 0

def runselftest(appname="selftest",**kargs):
    """Performs the selftest returns True or False.
    Executes some the basic runtime test cases for user verification.

    Args:
        appname: Name of the application. Changing this may break the
            selftest.
            default:=selftest

        **kargs:
            debug: Displays extended state data for developers.
                Requires __debug__==True.
            verbose: Extends the amount of the display of 
                processing data.
            _verbose=#levels: Extends the amount of the display 
                of processing data by given number of levels
                at once.

    Returns:
        Selftest object.

    Raises:
        bypassed subsystems

    """
    global debug
    global _verbose
    
    # set display mode for errors
    _interactive = kargs.get('interactive',False)
    _verbose = 0

    debug = kargs.get('debug',False)

    for _o,_a in kargs.items():
        if _o == 'verbose':
            _verbose += 1
        elif _o == '_verbose':
            _verbose += _a

    #
    # load tests
    case00(appname)
    case01(appname)
    
    #
    # validation tests
    case02(appname)
    case03(appname)

    #
    # JSONPointer tests
    case04(appname)
    case05(appname)
    case06(appname)
    
    return True
        
def printverbose(lvl,args):
    if lvl<=_verbose or debug:
        print args
    
def case00(appname):
    """Loads and verifies the self test 'data.json'.

    Therefore the result of the creation of JSONDataSerializer 
    is compared to the load by json.load().
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    # case=0:
    datafile = position+"data.json"        
    schemafile = position+"schema.jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case00: load "+str(datafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    _kargs['validator'] = MODE_SCHEMA_OFF
    configdata = ConfigData(appname,**_kargs)        

    # jval
    if not os.path.isfile(datafile):
        raise BaseException("Missing JSON data:file="+str(datafile))
    # load data
    with open(datafile) as data_file:
        jval = json.load(data_file)
    if jval == None:
        raise BaseException("Failed to load data:"+str(data_file))

    printverbose(2, "check data...")
    for l in ['address',]:
        printverbose(2,"check data["+l+"]...")   
        for n in ['streetAddress',"city","houseNumber",]:
            cdata = configdata.data[l][n]
            jdata = jval[l][n]
            assert cdata == jdata 
            printverbose(2,"check data["+l+"]["+str(n)+"]...OK")   
       
    for l in ['phoneNumber',]:
        printverbose(2,"check data["+l+"]...")   
        for n in [0,]:
            printverbose(2,"check data["+l+"]["+str(n)+"]...")   
            for p in ['type',"number",]:
                cdata = configdata.data[l][n][p]
                jdata = jval[l][n][p]
                assert cdata == jdata 
                printverbose(2,"check data["+l+"]["+str(n)+"]["+str(p)+"]...OK")   
    printverbose(2,"")   

def case01(appname):
    """Loads and verifies the self test 'selftest.json'.

    Therefore the result of the creation of JSONDataSerializer
    is compared to the load by json.load().
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    # case=0:
    datafile = position+appname+".json"        
    schemafile = position+appname+".jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case01: load "+str(datafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = MODE_SCHEMA_OFF
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    configdata = ConfigData(appname,**_kargs)        

    # jval
    if not os.path.isfile(datafile):
        raise BaseException("Missing JSON data:file="+str(datafile))
    # load data
    with open(datafile) as data_file:
        jval = json.load(data_file)
    if jval == None:
        raise BaseException("Failed to load data:"+str(data_file))

    printverbose(2,"check data[customers]...")   

    for l in ['domestic','abroad',]:
        printverbose(2,"check data[customers]["+l+"]...")   
        for n in [0,1,]:
            printverbose(2,"check data[customers]["+l+"]["+str(n)+"]...")
            cdata = configdata.data["customers"][l][n]["name"]
            jdata = jval["customers"][l][n]["name"]
            assert cdata == jdata 
            printverbose(2,"check data[customers]["+l+"]["+str(n)+"][name]...OK")
    
            cdata = configdata.data["customers"][l][n]["industries"]
            jdata = configdata.data["customers"][l][n]["industries"]
            assert cdata == jdata 
            printverbose(2,"check data[customers]["+l+"]["+str(n)+"][industries]...OK")
    
            for p in [0,1,]:
                cdata = configdata.data["customers"][l][n]["products"][p]["name"]
                jdata = configdata.data["customers"][l][n]["products"][p]["name"]
                assert cdata == jdata 
                printverbose(2,"check data[customers]["+l+"]["+str(n)+"][products]["+str(p)+"][name]...OK")
         
                cdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                jdata = configdata.data["customers"][l][n]["products"][p]["quantities"]
                assert cdata == jdata 
                printverbose(2,"check data[customers]["+l+"]["+str(n)+"][products]["+str(p)+"][quantities]...OK")   
         
                cdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                jdata = configdata.data["customers"][l][n]["products"][p]["priority"]
                assert cdata == jdata 
                printverbose(2,"check data[customers]["+l+"]["+str(n)+"][products]["+str(p)+"][priority]...OK")   

    printverbose(2,"")   

def case02(appname):
    """Loads and validates the self test 'data.json' and 'schema.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    # case=0:
    datafile = position+"data.json"        
    schemafile = position+"schema.jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case02: load and validate "+str(datafile))   
    printverbose(1,"case02: load and validate "+str(schemafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    _kargs['validator'] = MODE_SCHEMA_DRAFT3
    configdata = ConfigData(appname,**_kargs)        
    printverbose(2,"")   

def case03(appname):
    """Loads and validates the self test 'selftest.json' and 'selftest.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    #
    datafile = position+appname+".json"        
    schemafile = position+appname+".jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case03: load and validate "+str(datafile))   
    printverbose(1,"case03: load and validate "+str(schemafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    _kargs['validator'] = MODE_SCHEMA_DRAFT3
    configdata = ConfigData(appname,**_kargs)        
    printverbose(2,"")   

def case04(appname):
    """Loads and verifies by using JSONPointer access 'data.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    # case=0:
    datafile = position+"data.json"        
    schemafile = position+"schema.jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case04: load "+str(datafile))   
    printverbose(1,"case04: load "+str(schemafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = MODE_SCHEMA_DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    configdata = ConfigData(appname,**_kargs)        


    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node(configdata.data)
    jsx=str(jsonptrdata)
    ref = "{u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}"
    assert jsx == ref

    jsonptr = JSONPointer('/address/streetAddress')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == "21 2nd Street"

    jsonptr = JSONPointer('/address/city')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == "New York"

    jsonptr = JSONPointer('/address/houseNumber')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == 12

    printverbose(2,"")   

def case05(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    #
    datafile = position+"data.json"        
    schemafile = position+"schema.jsd"        
#     datafile = position+appname+".json"        
#     schemafile = position+appname+".jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case05: load "+str(datafile))   
    printverbose(1,"case05: load "+str(schemafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = MODE_SCHEMA_DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    configdata = ConfigData(appname,**_kargs)        


    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node(configdata.data)
    jsx=str(jsonptrdata)
    ref = "{u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}"
    assert jsx == ref

    jsonptr = JSONPointer('/phoneNumber/0/type')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == "home"

    jsonptr = JSONPointer('/phoneNumber/0/number')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == "212 555-1234"

    jsonptr = JSONPointer('/phoneNumber/0/active')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == True

    jsonptr = JSONPointer('/phoneNumber/0/private')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == False

    jsonptr = JSONPointer('/phoneNumber/0/addons')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == None

    jsonptr = JSONPointer('/phoneNumber/0/index')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == 0

    jsonptr = JSONPointer('/phoneNumber/0/testnumber')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")    
    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
    assert jsonptrdata == 1.5

    printverbose(2,"")   

def case06(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__))+os.sep

    #
    datafile = position+appname+".json"        
    schemafile = position+appname+".jsd"        
    
    printverbose(2,"#------------------------------------------")   
    printverbose(1,"case06: load "+str(datafile))   
    printverbose(1,"case06: load "+str(schemafile))   
    printverbose(2,"#------------------------------------------")   

    if debug:
        printverbose(0,"DBG:self.schemafile=  "+str(datafile))
        printverbose(0,"DBG:self.schemafile=  "+str(schemafile))

    
    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose>2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = MODE_SCHEMA_DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schemafile'] = schemafile
    configdata = ConfigData(appname,**_kargs)        


    for l in ['domestic','abroad',]:
        for n in [0,1,]:

            basep = '/customers/'+str(l)+'/'+str(n)
            jsonptr = JSONPointer(basep+'/name')
            jsonptrdata = jsonptr.get_node_or_value(configdata.data)
            jsx=str(jsonptrdata)
            ref = "customer"+str(n)
            assert jsx == ref

            jsonptr = JSONPointer(basep+'/industries')
            jsonptrdata = jsonptr.get_node_or_value(configdata.data)
            jsx=str(jsonptrdata)
            ref = "industry"+str(n)
            assert jsx == ref

            for p in [0,1,]: # products
                basep = '/customers/'+str(l)+'/'+str(n)+'/products/'+str(p)

                prodlist = {
                    'name': "product"+str(p),
                    "quantities": 2000+p,
                    "priority": 0+p,
                    "quota": 1.5+p
                }
                for k,v in prodlist.items():
                    attr = k # attribute
                    ref = v # attribute value
                    #
                    jsonptr = JSONPointer(basep+'/'+attr)
                    jsonptrdata = jsonptr.get_node_or_value(configdata.data)
                    jsx=jsonptrdata

                    #assert jsx == ref

                    try:
                        assert jsx == ref
                    except AssertionError as e:
                        print >>sys.stderr, "ERROR:AssertionError:k="+str(k)+" / v="+str(v)+" / type="+str(type(v))
                        print >>sys.stderr, "ERROR:AssertionError:jsx="+str(jsx)+" / type="+str(type(jsx))
                        assert jsx == ref
                        #raise AssertionError
                        #raise Exception

    printverbose(2,"")   
