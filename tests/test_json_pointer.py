import pytest

from jsondata.data import JSONData, SchemaMode
from jsondata.pointer import JSONPointer
from jsondata.serializer import JSONDataSerializer


@pytest.mark.parametrize(
    'pointer,initial,source,result,get_node_parent,key',
    [
        ('', {},
         {'a': {'b': {'c': 2}}},
         {'a': {'b': {'c': 2}}},
         False, None
         ),
        ('', [],
         {'a': {'b': {'c': 2}}},
         [{'a': {'b': {'c': 2}}}],
         False, '-'
         ),
        ('/a', {'a': {'b': {'c': 2}}},
         {'a': {'b': {'c': 2}}},
         {'a': {'a': {'b': {'c': 2}}}},
         False, None
         ),
        ('/a/b/c', {'a': {'b': {'c': 2}}},
         {'d': 3},
         {'a': {'b': {'d': 3}}},
         True, None
         )
    ]
)
def test_get_node(pointer, initial, source, result, get_node_parent, key):
    json_data = JSONData(initial)
    target_node = JSONPointer(pointer).get_node(json_data.data,
                                                parent=get_node_parent)
    json_data.branch_add(target_node, key, source)
    assert json_data.data == result


def test_get_node_or_value_static(fixture_folder):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['data_for_pointer.json'],
        validator=SchemaMode.OFF
    )

    assert serializer.data["address"]["streetAddress"] == "21 2nd Street"

    # by pointer
    pointer = JSONPointer('/address/streetAddress')
    assert pointer
    pointer_data = pointer.get_node_or_value(serializer.data)
    assert str(pointer_data) == serializer.data["address"]["streetAddress"]

    # now in one line
    assert serializer.data["address"]["streetAddress"] == \
           JSONPointer('/address/streetAddress').get_node_or_value(serializer.data)

    assert serializer.data["phoneNumber"][0]["type"] == "home0"
    assert serializer.data["phoneNumber"][0]["type"] == \
           JSONPointer('/phoneNumber/0/type').get_node_or_value(serializer.data)

    assert serializer.data["phoneNumber"][0]["number"] == "000"
    assert serializer.data["phoneNumber"][0]["number"] == \
           JSONPointer('/phoneNumber/0/number').get_node_or_value(serializer.data)

    assert serializer.data["phoneNumber"][0]["number"] == "000"
    assert serializer.data["phoneNumber"][0]["number"] == \
           JSONPointer('/phoneNumber/0/number').get_node_or_value(serializer.data)


def test_get_node_or_value_dynamic(fixture_folder, json_pointer_data):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['data_for_pointer.json'],
        validator=SchemaMode.OFF
    )
    for l in ('domestic', 'abroad'):
        for n in (0, 1):
            cdata = serializer.data["customers"][l][n]["name"]
            jdata = json_pointer_data["customers"][l][n]["name"]
            assert cdata == jdata

            # now pointer
            ptr = JSONPointer('/customers/%s/%s/name' % (l, n))
            assert cdata == ptr.get_node_or_value(serializer.data)

            cdata = serializer.data["customers"][l][n]["industries"]
            jdata = json_pointer_data["customers"][l][n]["industries"]
            assert cdata == jdata

            # now pointer
            ptr = JSONPointer('/customers/%s/%s/industries' % (l, n))
            assert cdata == ptr.get_node_or_value(serializer.data)

            for p in (0, 1):
                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["name"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["name"]
                assert cdata == jdata

                ptr = JSONPointer('/customers/%s/%s/products/%s/name'
                                  % (l, n, p))
                assert cdata == ptr.get_node_or_value(serializer.data)

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["quantities"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["quantities"]
                assert cdata == jdata

                # now pointer
                ptr = JSONPointer('/customers/%s/%s/products/%s/quantities'
                                  % (l, n, p))
                assert cdata == ptr.get_node_or_value(serializer.data)

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["priority"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["priority"]
                assert cdata == jdata

                # now pointer
                ptr = JSONPointer('/customers/%s/%s/products/%s/priority'
                                  % (l, n, p))
                assert cdata == ptr.get_node_or_value(serializer.data)


def test_add_basic(fixture_folder):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['data_for_pointer.json'],
        validator=SchemaMode.OFF
    )
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert serializer.data["address"]["streetAddress"] == \
           jp.get_node_or_value(serializer.data)

    jp = JSONPointer('/address') + 'streetAddress'
    assert serializer.data["address"]["streetAddress"] == \
           jp.get_node_or_value(serializer.data)

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert serializer.data["phoneNumber"][0]["type"] == \
           jp.get_node_or_value(serializer.data)

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert serializer.data["phoneNumber"][0]["type"] == \
           jp.get_node_or_value(serializer.data)

    assert serializer.data["phoneNumber"][0]["number"] == "000"
    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert serializer.data["phoneNumber"][0]["number"] == \
           jp.get_node_or_value(serializer.data)


def test_add_advanced(fixture_folder, json_pointer_data):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['data_for_pointer.json'],
        validator=SchemaMode.OFF
    )
    for l in ('domestic', 'abroad'):
        for n in (0, 1):
            cdata = serializer.data["customers"][l][n]["name"]
            jdata = json_pointer_data["customers"][l][n]["name"]
            assert cdata == jdata

            ptr = JSONPointer('/customers') + l + n + 'name'
            assert cdata == ptr.get_node_or_value(serializer.data)

            cdata = serializer.data["customers"][l][n]["industries"]
            jdata = json_pointer_data["customers"][l][n]["industries"]
            assert cdata == jdata

            ptr = JSONPointer('/customers') + l + n + 'industries'
            assert cdata == ptr.get_node_or_value(serializer.data)

            for p in (0, 1):
                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["name"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["name"]
                assert cdata == jdata

                ptr = JSONPointer('/customers') + l + n + 'products' + p + 'name'
                assert cdata == ptr.get_node_or_value(serializer.data)

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["quantities"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["quantities"]
                assert cdata == jdata

                ptr = JSONPointer('/customers') + l + n + 'products' + p + 'quantities'
                assert cdata == ptr.get_node_or_value(serializer.data)

                cdata = \
                    serializer.data["customers"][l][n]["products"][p]["priority"]
                jdata = \
                    json_pointer_data["customers"][l][n]["products"][p]["priority"]
                assert cdata == jdata

                ptr = JSONPointer('/customers') + l + n + 'products' + p + 'priority'
                assert cdata == ptr.get_node_or_value(serializer.data)


def test_equality_basics():
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert '/address/streetAddress' == jp
    assert jp == '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    assert '/address/streetAddress' == jp
    assert jp == '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert '/phoneNumber/0/type' == jp
    assert jp == '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert '/phoneNumber/0/type' == jp
    assert jp == '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert '/phoneNumber/0/number' == jp
    assert jp == '/phoneNumber/0/number'


def test_equality_advanced():
    jp = JSONPointer('/address/streetAddress/')
    assert '/address/streetAddress' == jp
    assert jp == '/address/streetAddress'

    jp = JSONPointer('address/streetAddress')
    assert '/address/streetAddress' == jp
    assert jp == '/address/streetAddress'

