import json

import pytest

from jsondata.data import SchemaMode
from jsondata.serializer import JSONDataSerializer


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.OFF, SchemaMode.DRAFT3, SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_access_some_entries_by_constant_references(json_data_serializer):
    """
    Access some entries by constant references.
    """
    assert json_data_serializer.data["address"]["streetAddress"] == \
           "21 2nd Street"
    assert json_data_serializer.data["address"]["city"] == "New York"
    assert json_data_serializer.data["address"]["houseNumber"] == 12

    assert json_data_serializer.data["phoneNumber"][0]["type"] == "home"
    assert json_data_serializer.data["phoneNumber"][0]["number"] == \
           "212 555-1234"


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.OFF, SchemaMode.DRAFT3, SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_access_some_entries_by_dynamic_references(json_data_serializer,
                                                   json_basic):
    """Access some entries by dynamic references from raw data file read.
    """
    assert json_data_serializer.data["address"]["streetAddress"] == \
           json_basic["address"]["streetAddress"]
    assert json_data_serializer.data["address"]["city"] == \
           json_basic["address"]["city"]
    assert json_data_serializer.data["address"]["houseNumber"] == \
           json_basic["address"]["houseNumber"]

    assert json_data_serializer.data["phoneNumber"][0]["type"] == \
           json_basic["phoneNumber"][0]["type"]
    assert json_data_serializer.data["phoneNumber"][0]["number"] == \
           json_basic["phoneNumber"][0]["number"]


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_verify_loaded_data(json_data_serializer):
    conf_dat = {
        'phoneNumber': [{'type': 'home', 'number': '212 555-1234'}],
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        }
    }
    assert json_data_serializer.data == conf_dat


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT3],
                         indirect=['json_data_serializer'])
def test_verify_loaded_schema(json_data_serializer):
    conf_schema = {
        'required': False,
        '_comment': 'This is a comment to be dropped by the initial '
                    'scan:object(0)',
        '_doc': 'Concatenated for the same instance.:object(0)',
        '$schema': 'http://json-schema.org/draft-03/schema',
        'type': 'object',
        'properties': {
            'phoneNumber': {
                'items': {
                    'required': False,
                    'type': 'object',
                    'properties': {
                        'type': {
                            'required': False,
                            'type': 'string'
                        },
                        'number': {
                            'required': False,
                            'type': 'string'
                        }
                    }
                },
                '_comment': 'This is a comment(1):array',
                'required': False,
                'type': 'array'
            },
            'address': {
                '_comment': 'This is a comment(0):address',
                'required': True,
                'type': 'object',
                'properties': {
                    'city': {
                        'required': True,
                        'type': 'string'
                    },
                    'streetAddress': {
                        'required': True,
                        'type': 'string'
                    },
                    'houseNumber': {
                        'required': False,
                        'type': 'number'
                    }
                }
            }
        }
    }
    assert json_data_serializer.schema == conf_schema


@pytest.mark.parametrize('validator',
                         [SchemaMode.OFF, SchemaMode.DRAFT3, SchemaMode.DRAFT4])
def test_advanced_create_and_check(fixture_folder, json_basic, validator):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['basics/basic.json'],
        validator=validator
    )
    assert serializer.data["address"]["streetAddress"] == "21 2nd Street"
    assert serializer.data["address"]["city"] == "New York"
    assert serializer.data["address"]["houseNumber"] == 12
    assert serializer.data["phoneNumber"][0]["type"] == "home"
    assert serializer.data["phoneNumber"][0]["number"] == "212 555-1234"

    assert serializer.data["address"]["streetAddress"] == \
           json_basic["address"]["streetAddress"]
    assert serializer.data["address"]["city"] == json_basic["address"]["city"]
    assert serializer.data["address"]["houseNumber"] == \
           json_basic["address"]["houseNumber"]
    assert serializer.data["phoneNumber"][0]["type"] == \
           json_basic["phoneNumber"][0]["type"]
    assert serializer.data["phoneNumber"][0]["number"] == \
           json_basic["phoneNumber"][0]["number"]