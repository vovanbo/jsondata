# -*- coding: utf-8 -*-
"""Test of basic features for the user by '--selftest'.

This module is used by 'jsondc' when the opverify_data_schemaardoced 
basic functional checks by calling 'run_self_test'.

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
import json

from pathlib import Path

from jsondata.pointer import JSONPointer
from jsondata.serializer import JSONDataSerializer
from jsondata.data import SchemaMode

__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.12'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


def run_self_test(appname='selftest'):
    """
    Performs the self test returns True or False.
    Executes some the basic runtime test cases for user verification.

    Args:
        appname: Name of the application. Changing this may break the self test.
            default:=selftest

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


def load_data(appname):
    """Loads and verifies the self test 'data.json'.

    Therefore the result of the creation of JSONDataSerializer 
    is compared to the load by json.load().
    """
    cwd = Path.cwd()
    data_file = cwd / "data.json"
    schema_file = cwd / "schema.jsd"

    logger.info("load_data: load %s", data_file)
    logger.debug("self.schema_file=%s", data_file)
    logger.debug("self.schema_file=%s", schema_file)

    serializer = JSONDataSerializer(
        appname, data_file=data_file, schema_file=schema_file,
        path_list=[cwd], validator=SchemaMode.OFF
    )

    # json_data
    if not data_file.is_file():
        raise BaseException("Missing JSON data:file=" + str(data_file))
    # load data
    with open(data_file) as data_file:
        json_data = json.load(data_file)

    if json_data is None:
        raise BaseException("Failed to load data:" + str(data_file))

    logger.info("check data...")
    for l in ['address', ]:
        logger.info("check data[" + l + "]...")
        for n in ['streetAddress', "city", "houseNumber", ]:
            cdata = serializer.data[l][n]
            jdata = json_data[l][n]
            assert cdata == jdata
            logger.info("check data[%s][%s]...OK", l, n)

    for l in ['phoneNumber', ]:
        logger.info("check data[%s]...", l)
        for n in [0, ]:
            logger.info("check data[%s][%s]...", l, n)
            for p in ['type', "number", ]:
                cdata = serializer.data[l][n][p]
                jdata = json_data[l][n][p]
                assert cdata == jdata
                logger.info("check data[%s][%s][%s]...OK", l, n, p)


def load_appname(appname):
    """Loads and verifies the self test 'selftest.json'.

    Therefore the result of the creation of JSONDataSerializer
    is compared to the load by json.load().
    """
    cwd = Path.cwd()
    data_file = (cwd / appname).with_suffix(".json")
    schema_file = (cwd / appname).with_suffix(".jsd")

    logger.info("#------------------------------------------")
    logger.info("load_appname: load " + str(data_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    serializer = JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.OFF, path_list=[cwd]
    )

    # json_data
    if not os.path.isfile(data_file):
        raise BaseException("Missing JSON data:file=" + str(data_file))
    # load data
    with open(data_file) as data_file:
        json_data = json.load(data_file)
    if json_data is None:
        raise BaseException("Failed to load data:" + str(data_file))

    logger.info("check data[customers]...")

    for l in ['domestic', 'abroad', ]:
        logger.info("check data[customers][" + l + "]...")
        for n in [0, 1, ]:
            logger.info("check data[customers][%s][%s]...", l, n)
            cdata = serializer.data["customers"][l][n]["name"]
            jdata = json_data["customers"][l][n]["name"]
            assert cdata == jdata
            logger.info("check data[customers][%s][%s][name]...OK", l, n)

            cdata = serializer.data["customers"][l][n]["industries"]
            jdata = serializer.data["customers"][l][n]["industries"]
            assert cdata == jdata
            logger.info("check data[customers][%s][%s][industries]...OK", l, n)

            for p in [0, 1, ]:
                cdata = serializer.data["customers"][l][n]["products"][p][
                    "name"]
                jdata = serializer.data["customers"][l][n]["products"][p][
                    "name"]
                assert cdata == jdata
                logger.info("check data[customers][%s][%s][products][%s]"
                            "[name]...OK", l, n, p)

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["quantities"]
                jdata = \
                    serializer.data["customers"][l][n]["products"][p]["quantities"]
                assert cdata == jdata
                logger.info("check data[customers][%s][%s][products][%s]"
                            "[quantities]...OK", l, n, p)

                cdata = serializer.data["customers"][l][n]["products"][p]["priority"]
                jdata = serializer.data["customers"][l][n]["products"][p]["priority"]
                assert cdata == jdata
                logger.info("check data[customers][%s][%s][products][%s]"
                            "[priority]...OK", l, n, p)


def verify_data_schema(appname):
    """
    Loads and validates the self test 'data.json' and 'schema.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    cwd = Path.cwd()
    data_file = cwd / "data.json"
    schema_file = cwd / "schema.jsd"

    logger.info("#------------------------------------------")
    logger.info("verify_data_schema: load and validate " + str(data_file))
    logger.info("verify_data_schema: load and validate " + str(schema_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.DRAFT3, path_list=[cwd]
    )


def verify_appname_schema(appname):
    """Loads and validates the self test 'selftest.json' and 'selftest.jsd'.

    Therefore the result of the creation of JSONDataSerializer is performed
    with draft3 validation by jsonschema.validate().
    """
    cwd = Path.cwd()
    data_file = (cwd / appname).with_suffix(".json")
    schema_file = (cwd / appname).with_suffix(".jsd")

    logger.info("#------------------------------------------")
    logger.info("verify_appname_schema: load and validate " + str(data_file))
    logger.info("verify_appname_schema: load and validate " + str(schema_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.DRAFT3, path_list=[cwd]
    )


def jsonpointer_data_schema(appname):
    """
    Loads and verifies by using JSONPointer access 'data.json'.
    """
    cwd = Path.cwd()
    data_file = cwd / "data.json"
    schema_file = cwd / "schema.jsd"

    logger.info("#------------------------------------------")
    logger.info("jsonpointer_data_schema: load " + str(data_file))
    logger.info("jsonpointer_data_schema: load " + str(schema_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    serializer = JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.DRAFT3, path_list=[cwd]
    )

    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node(serializer.data)
    ref = {
        'city': 'New York',
        'streetAddress': '21 2nd Street',
        'houseNumber': 12
    }
    assert jsonptrdata == ref

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


def jsonpointer_selftest_data(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    cwd = Path.cwd()
    data_file = cwd / "data.json"
    schema_file = cwd / "schema.jsd"

    logger.info("#------------------------------------------")
    logger.info("jsonpointer_selftest_data: load " + str(data_file))
    logger.info("jsonpointer_selftest_data: load " + str(schema_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    serializer = JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.DRAFT3, path_list=[cwd]
    )

    jsonptr = JSONPointer('/address')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node(serializer.data)
    ref = {
        'city': 'New York',
        'streetAddress': '21 2nd Street',
        'houseNumber': 12
    }
    assert jsonptrdata == ref

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
    assert jsonptrdata is True

    jsonptr = JSONPointer('/phoneNumber/0/private')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata is False

    jsonptr = JSONPointer('/phoneNumber/0/addons')
    if not jsonptr:
        raise BaseException("Failed to create JSONPointer")
    jsonptrdata = jsonptr.get_node_or_value(serializer.data)
    assert jsonptrdata is None

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


def jsonpointer_selftest_data_schema(appname):
    """Loads and verifies by using JSONPointer access 'selftest.json'.
    """
    cwd = Path.cwd()
    data_file = (cwd / appname).with_suffix(".json")
    schema_file = (cwd / appname).with_suffix(".jsd")

    logger.info("#------------------------------------------")
    logger.info("jsonpointer_selftest_data_schema: load " + str(data_file))
    logger.info("jsonpointer_selftest_data_schema: load " + str(schema_file))
    logger.info("#------------------------------------------")
    logger.debug("self.schema_file=  " + str(data_file))
    logger.debug("self.schema_file=  " + str(schema_file))

    serializer = JSONDataSerializer(
        appname, schema_file=schema_file, data_file=data_file,
        validator=SchemaMode.DRAFT3, path_list=[cwd]
    )

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
                basep = '/customers/%s/%s/products/%s' % (l, n, p)

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
                        logger.error("AssertionError: k=%s / v=%s / type=%s",
                                     k, v, type(v))
                        logger.error("AssertionError: jsx=%s / type=%s",
                                     jsx, type(jsx))
                        assert jsx == ref
                        # raise AssertionError
                        # raise Exception


if __name__ == '__main__':
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s [%(asctime)s.%(msecs)03d] '
               '(%(name)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.Formatter.converter = time.gmtime

    run_self_test()
