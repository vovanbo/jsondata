from jsondata.data import Mode
from jsondata.pointer import JSONPointer
from jsondata.serializer import JSONDataSerializer


def test_load_data(fixture_folder, json_basic):
    data_file = fixture_folder / 'draft3.json'
    schema_file = fixture_folder / 'draft3.jsd'
    serializer = JSONDataSerializer(
        'test', data_file=data_file, schema_file=schema_file,
        path_list=[fixture_folder], validator=Mode.OFF
    )
    for l in ('address',):
        for n in ('streetAddress', 'city', 'houseNumber'):
            assert serializer.data[l][n] == json_basic[l][n]

    for l in ('phoneNumber',):
        for n in (0, 1):
            for p in ('type', 'number'):
                assert serializer.data[l][n][p] == json_basic[l][n][p]


def test_load_data_with_app_name(fixture_folder, json_pointer_data):
    serializer = JSONDataSerializer(
        'data_for_pointer', validator=Mode.OFF, path_list=[fixture_folder]
    )
    for l in ('domestic', 'abroad'):
        for n in (0, 1):
            assert serializer.data["customers"][l][n]["name"] == \
                   json_pointer_data["customers"][l][n]["name"]
            assert serializer.data["customers"][l][n]["industries"] == \
                   json_pointer_data["customers"][l][n]["industries"]

            for p in (0, 1):
                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["name"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["name"]
                assert cdata == jdata

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["quantities"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["quantities"]
                assert cdata == jdata

                cdata = serializer.data["customers"][l][n]["products"][p]["priority"]
                jdata = json_pointer_data["customers"][l][n]["products"][p]["priority"]
                assert cdata == jdata


def test_jsonpointer_data_schema(fixture_folder):
    data_file = fixture_folder / 'draft3.json'
    schema_file = fixture_folder / 'draft3.jsd'
    serializer = JSONDataSerializer(
        'test', schema_file=schema_file, data_file=data_file,
        validator=Mode.DRAFT3, path_list=[fixture_folder]
    )

    pointer = JSONPointer('/address')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node(serializer.data)
    ref = {
        'city': 'New York',
        'streetAddress': '21 2nd Street',
        'houseNumber': 12
    }
    assert pointer_data == ref

    pointer = JSONPointer('/address/streetAddress')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == "21 2nd Street"

    pointer = JSONPointer('/address/city')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == "New York"

    pointer = JSONPointer('/address/houseNumber')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == 12

    pointer = JSONPointer('/phoneNumber/0/type')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == "home"

    pointer = JSONPointer('/phoneNumber/0/number')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == "212 555-1234"

    pointer = JSONPointer('/phoneNumber/0/active')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data is True

    pointer = JSONPointer('/phoneNumber/0/private')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data is False

    pointer = JSONPointer('/phoneNumber/0/addons')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data is None

    pointer = JSONPointer('/phoneNumber/0/index')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == 0

    pointer = JSONPointer('/phoneNumber/0/testnumber')
    if not pointer:
        raise BaseException("Failed to create JSONPointer")
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert pointer_data == 1.5


def test_jsonpointer_data_for_pointer(fixture_folder):
    serializer = JSONDataSerializer(
        'data_for_pointer', validator=Mode.DRAFT3, path_list=[fixture_folder]
    )

    for l in ('domestic', 'abroad'):
        for n in (0, 1):
            base_pointer = '/customers/%s/%s' % (l, n)
            pointer = JSONPointer(base_pointer + '/name')
            pointer_data = pointer.get_node_or_value(serializer.data)
            assert pointer_data == 'customer%s' % n

            pointer = JSONPointer(base_pointer + '/industries')
            pointer_data = pointer.get_node_or_value(serializer.data)
            assert pointer_data == 'industry%s' % n

            for p in (0, 1):  # products
                base_pointer = '/customers/%s/%s/products/%s' % (l, n, p)

                product_list = {
                    'name': 'product%s' % p,
                    'quantities': 2000 + p,
                    'priority': 0 + p,
                    'quota': 1.5 + p
                }
                for attr, ref in product_list.items():
                    pointer = JSONPointer(base_pointer + '/' + attr)
                    pointer_data = pointer.get_node_or_value(serializer.data)
                    assert pointer_data == ref
