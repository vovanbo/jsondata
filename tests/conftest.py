import json

import pytest
from pathlib import Path

from jsondata.data import Mode, JSONData
from jsondata.serializer import JSONDataSerializer

cwd = Path.cwd()
json_basic_file = cwd / 'fixtures' / 'basic.json'
schema_draft3_file = cwd / 'fixtures' / 'draft3.jsd'
schema_draft4_file = cwd / 'fixtures' / 'draft4.jsd'
json_pointer_data_file = cwd / 'fixtures' / 'data_for_pointer.json'


@pytest.fixture
def fixture_folder():
    return cwd / 'fixtures'


@pytest.fixture
def json_basic():
    with open(json_basic_file) as fp:
        return json.load(fp)


@pytest.fixture
def json_pointer_data():
    with open(json_pointer_data_file) as fp:
        return json.load(fp)


@pytest.fixture
def schema_draft3():
    with open(schema_draft3_file) as fp:
        return json.load(fp)


@pytest.fixture
def schema_draft4():
    with open(schema_draft4_file) as fp:
        return json.load(fp)


@pytest.fixture
def json_data_serializer(request):
    if request.param is Mode.OFF:
        schema_file = None
    elif request.param is Mode.DRAFT3:
        schema_file = schema_draft3_file
    else:
        schema_file = schema_draft4_file

    return JSONDataSerializer(
        'json_data_serializer_fixture', data_file=json_basic_file,
        no_default_path=True, no_sub_data=True, path_list=[cwd],
        validator=request.param, schema_file=schema_file
    )
