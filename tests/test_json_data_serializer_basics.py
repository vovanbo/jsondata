import tempfile

import pytest
from pathlib import Path

from jsondata.data import SchemaMode
from jsondata.exceptions import JSONDataKeyError, JSONDataNodeType
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
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {'type': 'home', 'number': '212 555-1234'},
            {'type': 'office', 'number': '313 444-555'},
            {'type': 'mobile', 'number': '777 666-555'},
        ],
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
        no_sub_data=True, file_list=['basic.json'],
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


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_json_export(json_data_serializer):
    serializer = json_data_serializer
    schema = {
        '$schema': 'http://json-schema.org/draft-03/schema',
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }

    _, export_data_temp = tempfile.mkstemp()
    _, export_schema_temp = tempfile.mkstemp()
    assert serializer.json_export(None, export_data_temp)
    assert serializer.json_export(schema, export_schema_temp)

    path_list = [Path(export_data_temp).parent, Path(export_schema_temp).parent]

    temp_serializer = JSONDataSerializer(
        'test', data_file=export_data_temp, schema_file=export_schema_temp,
        no_default_path=True, no_sub_data=True, path_list=path_list,
        validator=SchemaMode.DRAFT4
    )
    assert serializer.data == temp_serializer.data


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_add_new(json_data_serializer, fixture_folder):
    serializer = json_data_serializer
    schema = {
        "$schema": "http://json-schema.org/draft-03/schema",
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }
    data_file = fixture_folder / 'branch1.json'
    target = serializer.data['phoneNumber']
    assert serializer.json_import(target, '-', data_file, schema=schema)
    assert serializer.data == {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {'type': 'home', 'number': '212 555-1234'},
            {'type': 'office', 'number': '313 444-555'},
            {'type': 'mobile', 'number': '777 666-555'},
            {'type': 'home1', 'number': '111 222-333'},
        ],
    }

    data_file = fixture_folder / 'branch2.json'
    assert serializer.json_import(target, 0, data_file, schema=schema)
    result = {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {'type': 'home2', 'number': '222 222-333'},
            {'type': 'office', 'number': '313 444-555'},
            {'type': 'mobile', 'number': '777 666-555'},
            {'type': 'home1', 'number': '111 222-333'},
        ],
    }
    assert serializer.data == result


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_json_import_errors(json_data_serializer, fixture_folder, json_basic):
    serializer = json_data_serializer
    target = serializer.data['phoneNumber']
    data_file = fixture_folder / 'branch2.json'
    schema = {
        "$schema": "http://json-schema.org/draft-03/schema",
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }

    with pytest.raises(JSONDataKeyError):
        assert serializer.json_import(target, 'phoneNumber', data_file,
                                      schema=schema)
    assert serializer.data == json_basic

    with pytest.raises(JSONDataNodeType):
        assert serializer.json_import(target, None, data_file,
                                      schema=schema)
    assert serializer.data == json_basic


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_add_present_item(json_data_serializer, fixture_folder):
    serializer = json_data_serializer
    schema = {
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }
    data_file = fixture_folder / 'branch1.json'
    target = serializer.data
    assert serializer.json_import(target, None, data_file, schema=schema)
    assert serializer.data == {'type': 'home1', 'number': '111 222-333'}


@pytest.mark.parametrize('json_data_serializer',
                         [SchemaMode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_load_and_import_with_validation(json_data_serializer, fixture_folder):
    serializer = json_data_serializer
    schema = {
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }
    data_file = fixture_folder / 'branch1.json'
    target = serializer.data
    assert serializer.json_import(target, 'phoneNumber', data_file,
                                  schema=schema)
    assert serializer.data == {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': {'type': 'home1', 'number': '111 222-333'},
    }
