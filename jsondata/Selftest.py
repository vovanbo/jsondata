# -*- coding: utf-8 -*-
"""Test of basic features for the user by '--selftest'.

This module is used by 'jsondc' when the opverify_data_schemaardoced 
basic functional checks by calling 'runselftest'.

The display of actions and results could be activated and 
raised by multiple repetition of the '-v' option.

The following data and schema are applied:
    0. jsondata/data.json + jsondata/schema.jsd
    1. jsondata/datacheck.json + jsondata/datacheck.jsd

The performed process flow is:
    0. load
    1. validate
    2. verify

By default either 'True' is returned, or in case of a failed test
and/or error condition an exception is raised.
"""
import logging
import os
import sys
import json

from .pointer import JSONPointer
from .serializer import JSONDataSerializer
from .data import SchemaMode

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.12'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


def runselftest(appname='selftest', interactive=False, debug=False,
                verbose=True):
    """Performs the selftest returns True or False.
    Executes some the basic runtime test cases for user verification.

    Args:
        appname: Name of the application. Changing this may break the
            selftest.
            default:=selftest

        **kwargs:
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
    #
    # load tests
    load_data(appname)
    load_appname(appname)

    #
    # validation tests
    verify_data_schema(appname)
    verify_appname_schema(appname)

    #
    # JSONPointer tests
    jsonpointer_data_schema(appname)
    jsonpointer_selftest_data(appname)
    jsonpointer_selftest_data_schema(appname)

    return True


def printverbose(lvl, args):
    if lvl <= _verbose or debug:
        print(args)


def load_data(appname):
    """Loads and verifies the self test 'data.json'.

    Therefore the result of the creation of JSONDataSerializer 
    is compared to the load by json.load().
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    # case=0:
    datafile = position + "data.json"
    schemafile = position + "schema.jsd"

    logger.info("load_data: load %s", datafile)
    logger.debug("self.schema_file=%s", datafile)
    logger.debug("self.schema_file=%s", schemafile)

    kwargs = {
        'debug': debug,
        'verbose': _verbose > 2,
        'pathlist': [position],
        'datafile': datafile,
        'schema_file': schemafile,
        'validator': SchemaMode.OFF
    }
    serializer = JSONDataSerializer(appname, **kwargs)

    # jval
    if not os.path.isfile(datafile):
        raise BaseException("Missing JSON data:file=" + str(datafile))
    # load data
    with open(datafile) as data_file:
        jval = json.load(data_file)

    if jval == None:
        raise BaseException("Failed to load data:" + str(data_file))

    printverbose(2, "check data...")
    for l in ['address', ]:
        printverbose(2, "check data[" + l + "]...")
        for n in ['streetAddress', "city", "houseNumber", ]:
            cdata = serializer.data[l][n]
            jdata = jval[l][n]
            assert cdata == jdata
            printverbose(2, "check data[" + l + "][" + str(n) + "]...OK")

    for l in ['phoneNumber', ]:
        printverbose(2, "check data[" + l + "]...")
        for n in [0, ]:
            printverbose(2, "check data[" + l + "][" + str(n) + "]...")
            for p in ['type', "number", ]:
                cdata = serializer.data[l][n][p]
                jdata = jval[l][n][p]
                assert cdata == jdata
                printverbose(2, "check data[" + l + "][" + str(n) + "][" + str(
                    p) + "]...OK")
    printverbose(2, "")


def load_appname(appname):
    """Loads and verifies the self test 'selftest.json'.

    Therefore the result of the creation of JSONDataSerializer
    is compared to the load by json.load().
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    # case=0:
    datafile = position + appname + ".json"
    schemafile = position + appname + ".jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "load_appname: load " + str(datafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = SchemaMode.OFF
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    serializer = JSONDataSerializer(appname, **_kargs)

    # jval
    if not os.path.isfile(datafile):
        raise BaseException("Missing JSON data:file=" + str(datafile))
    # load data
    with open(datafile) as data_file:
        jval = json.load(data_file)
    if jval == None:
        raise BaseException("Failed to load data:" + str(data_file))

    printverbose(2, "check data[customers]...")

    for l in ['domestic', 'abroad', ]:
        printverbose(2, "check data[customers][" + l + "]...")
        for n in [0, 1, ]:
            printverbose(2,
                         "check data[customers][" + l + "][" + str(n) + "]...")
            cdata = serializer.data["customers"][l][n]["name"]
            jdata = jval["customers"][l][n]["name"]
            assert cdata == jdata
            printverbose(2, "check data[customers][" + l + "][" + str(
                n) + "][name]...OK")

            cdata = serializer.data["customers"][l][n]["industries"]
            jdata = serializer.data["customers"][l][n]["industries"]
            assert cdata == jdata
            printverbose(2, "check data[customers][" + l + "][" + str(
                n) + "][industries]...OK")

            for p in [0, 1, ]:
                cdata = serializer.data["customers"][l][n]["products"][p][
                    "name"]
                jdata = serializer.data["customers"][l][n]["products"][p][
                    "name"]
                assert cdata == jdata
                printverbose(2, "check data[customers][" + l + "][" + str(
                    n) + "][products][" + str(p) + "][name]...OK")

                cdata = serializer.data["customers"][l][n]["products"][p][
                    "quantities"]
                jdata = serializer.data["customers"][l][n]["products"][p][
                    "quantities"]
                assert cdata == jdata
                printverbose(2, "check data[customers][" + l + "][" + str(
                    n) + "][products][" + str(p) + "][quantities]...OK")

                cdata = serializer.data["customers"][l][n]["products"][p][
                    "priority"]
                jdata = serializer.data["customers"][l][n]["products"][p][
                    "priority"]
                assert cdata == jdata
                printverbose(2, "check data[customers][" + l + "][" + str(
                    n) + "][products][" + str(p) + "][priority]...OK")

    printverbose(2, "")


def verify_data_schema(appname):
    """Loads and validates the self test 'data.json' and 'schema.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    # case=0:
    datafile = position + "data.json"
    schemafile = position + "schema.jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "verify_data_schema: load and validate " + str(datafile))
    printverbose(1, "verify_data_schema: load and validate " + str(schemafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    _kargs['validator'] = SchemaMode.DRAFT3
    serializer = JSONDataSerializer(appname, **_kargs)
    printverbose(2, "")


def verify_appname_schema(appname):
    """Loads and validates the self test 'selftest.json' and 'selftest.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    #
    datafile = position + appname + ".json"
    schemafile = position + appname + ".jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "verify_appname_schema: load and validate " + str(datafile))
    printverbose(1,
                 "verify_appname_schema: load and validate " + str(schemafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    _kargs['validator'] = SchemaMode.DRAFT3
    serializer = JSONDataSerializer(appname, **_kargs)
    printverbose(2, "")


def jsonpointer_data_schema(appname):
    """Loads and verifies by using JSONPointer access 'data.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    # case=0:
    datafile = position + "data.json"
    schemafile = position + "schema.jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "jsonpointer_data_schema: load " + str(datafile))
    printverbose(1, "jsonpointer_data_schema: load " + str(schemafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = SchemaMode.DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    serializer = JSONDataSerializer(appname, **_kargs)

    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node(serializer.data)
    jsx = str(jsonptrdata)
    ref = "{u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}"
    assert jsx == ref

    jsonptr = JSONPointer('/address/streetAddress')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == "21 2nd Street"

    jsonptr = JSONPointer('/address/city')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == "New York"

    jsonptr = JSONPointer('/address/houseNumber')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == 12

    printverbose(2, "")


def jsonpointer_selftest_data(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    #
    datafile = position + "data.json"
    schemafile = position + "schema.jsd"
    #     datafile = position+appname+".json"
    #     schema_file = position+appname+".jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "jsonpointer_selftest_data: load " + str(datafile))
    printverbose(1, "jsonpointer_selftest_data: load " + str(schemafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = SchemaMode.DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    serializer = JSONDataSerializer(appname, **_kargs)

    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node(serializer.data)
    jsx = str(jsonptrdata)
    ref = "{u'city': u'New York', u'streetAddress': u'21 2nd Street', u'houseNumber': 12}"
    assert jsx == ref

    jsonptr = JSONPointer('/phoneNumber/0/type')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == "home"

    jsonptr = JSONPointer('/phoneNumber/0/number')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == "212 555-1234"

    jsonptr = JSONPointer('/phoneNumber/0/active')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == True

    jsonptr = JSONPointer('/phoneNumber/0/private')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == False

    jsonptr = JSONPointer('/phoneNumber/0/addons')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == None

    jsonptr = JSONPointer('/phoneNumber/0/index')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == 0

    jsonptr = JSONPointer('/phoneNumber/0/testnumber')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata == 1.5

    printverbose(2, "")


def jsonpointer_selftest_data_schema(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    position = os.path.abspath(os.path.dirname(__file__)) + os.sep

    #
    datafile = position + appname + ".json"
    schemafile = position + appname + ".jsd"

    printverbose(2, "#------------------------------------------")
    printverbose(1, "jsonpointer_selftest_data_schema: load " + str(datafile))
    printverbose(1, "jsonpointer_selftest_data_schema: load " + str(schemafile))
    printverbose(2, "#------------------------------------------")

    if debug:
        printverbose(0, "DBG:self.schema_file=  " + str(datafile))
        printverbose(0, "DBG:self.schema_file=  " + str(schemafile))

    _kargs = {}
    _kargs['debug'] = debug
    _kargs['verbose'] = _verbose > 2
    _kargs['pathlist'] = [position]
    _kargs['validator'] = SchemaMode.DRAFT3
    _kargs['datafile'] = datafile
    _kargs['schema_file'] = schemafile
    serializer = JSONDataSerializer(appname, **_kargs)

    for l in ['domestic', 'abroad', ]:
        for n in [0, 1, ]:

            basep = '/customers/' + str(l) + '/' + str(n)
            jsonptr = JSONPointer(basep + '/name')
            jsonptrdata = jsonptr.get_node_or_value(serializer.data)
            jsx = str(jsonptrdata)
            ref = "customer" + str(n)
            assert jsx == ref

            jsonptr = JSONPointer(basep + '/industries')
            jsonptrdata = jsonptr.get_node_or_value(serializer.data)
            jsx = str(jsonptrdata)
            ref = "industry" + str(n)
            assert jsx == ref

            for p in [0, 1, ]:  # products
                basep = '/customers/' + str(l) + '/' + str(
                    n) + '/products/' + str(p)

                prodlist = {
                    'name': "product" + str(p),
                    "quantities": 2000 + p,
                    "priority": 0 + p,
                    "quota": 1.5 + p
                }
                for k, v in list(prodlist.items()):
                    attr = k  # attribute
                    ref = v  # attribute value
                    #
                    jsonptr = JSONPointer(basep + '/' + attr)
                    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
                    jsx = jsonptrdata

                    # assert jsx == ref

                    try:
                        assert jsx == ref
                    except AssertionError as e:
                        print(
                            "ERROR:AssertionError:k=" + str(k) + " / v=" + str(
                                v) + " / type=" + str(type(v)), file=sys.stderr)
                        print("ERROR:AssertionError:jsx=" + str(
                            jsx) + " / type=" + str(type(jsx)), file=sys.stderr)
                        assert jsx == ref
                        # raise AssertionError
                        # raise Exception

    printverbose(2, "")
