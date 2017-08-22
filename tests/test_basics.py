import jsonschema


def test_access_some_entries(json_basic):
    assert json_basic["address"]["streetAddress"] == "21 2nd Street"
    assert json_basic["address"]["city"] == "New York"
    assert json_basic["address"]["houseNumber"] == 12
    assert json_basic["phoneNumber"][0]["type"] == "home"
    assert json_basic["phoneNumber"][0]["number"] == "212 555-1234"


def test_validate_by_standard_api(json_basic, schema_draft3):
    """
    Validate by standard API: jsonschema.validate
    """
    jsonschema.validate(json_basic, schema_draft3)


def test_validate_draft3_api(json_basic, schema_draft3):
    """
    Validate by DRAFT3 API: jsonschema.Draft3Validator
    """
    jsonschema.Draft3Validator(json_basic, schema_draft3)

