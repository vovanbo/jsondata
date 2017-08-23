import json

import pytest
from pathlib import Path

from jsondata.data import SchemaMode
from jsondata.serializer import JSONDataSerializer

cwd = Path.cwd()
json_basic_file = cwd / 'fixtures' / 'basics' / 'basic.json'
schema_draft3_file = cwd / 'fixtures' / 'basics' / 'draft3.jsd'


@pytest.fixture
def fixture_folder():
    return cwd / 'fixtures'


@pytest.fixture
def json_basic():
    with open(json_basic_file) as fp:
        return json.load(fp)


@pytest.fixture
def schema_draft3():
    with open(schema_draft3_file) as fp:
        return json.load(fp)


@pytest.fixture
def json_data_serializer(request):
    if request.param is SchemaMode.OFF:
        schema_file = None
    else:
        schema_file = schema_draft3_file

    return JSONDataSerializer(
        'json_data_serializer_fixture', data_file=json_basic_file,
        no_default_path=True, no_sub_data=True, path_list=[cwd],
        validator=request.param, schema_file=schema_file
    )