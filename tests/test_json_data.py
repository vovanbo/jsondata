from jsondata.data import JSONData, Mode


def test_initialization(json_basic):
    json_data = JSONData(json_basic, validator=Mode.OFF)