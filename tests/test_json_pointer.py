import pytest

from jsondata.data import JSONData, Mode
from jsondata.exceptions import JSONPointerException
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
        validator=Mode.OFF
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
        validator=Mode.OFF
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
        validator=Mode.OFF
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
        validator=Mode.OFF
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
    assert jp == '/address/streetAddress/'

    jp = JSONPointer('address/streetAddress/')
    assert jp == '/address/streetAddress/'

    jp = JSONPointer('address/streetAddress')
    assert jp == '/address/streetAddress'


def test_ge():
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert jp >= '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    assert jp >= '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp >= '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert jp >= '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert jp >= '/phoneNumber/0/number'

    jp = JSONPointer('/address/streetAddress')
    assert jp >= '/address/streetAddress/'

    jp = JSONPointer('/address/streetAddress')
    assert jp >= '/address/streetAddress'

    jp = JSONPointer('address/streetAddress')
    assert jp >= '/address/streetAddress'

    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert not jp >= '/address'

    jp = JSONPointer('/address') + 'streetAddress'
    assert '/address/streetAddress' <= jp

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert '/phoneNumber/0/type' <= jp

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert '/phoneNumber/0/type' <= jp

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert '/phoneNumber/0/number' <= jp


def test_gt():
    jp = JSONPointer('/address')
    assert jp > '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    assert not jp > '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0
    assert jp > '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert not jp > '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 1 + 'number'
    assert not jp > '/phoneNumber/0/number'

    jp = JSONPointer('/address/streetAddress')
    assert jp > '/address/streetAddress/'

    jp = JSONPointer('address')
    assert jp > '/address/streetAddress'

    jp = JSONPointer('address/streetAddress')
    assert not jp > '/address/streetAddress'


def test_le():
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert not jp < '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    assert not jp < '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert not jp < '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert not jp < '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert not jp < '/phoneNumber/0/number'

    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert jp < '/address'

    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert jp <= '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp < '/phoneNumber/0'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp <= '/phoneNumber/0/type'


def test_lt():
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert not jp < '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    assert not jp < '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert not jp < '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0
    jp = jp + 'type'
    assert not jp < '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert not jp < '/phoneNumber/0/number'

    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert jp < '/address'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp < '/phoneNumber/0'


def test_ne():
    jp = JSONPointer('/address')
    jp = jp + 'streetAddress/'
    assert jp != '/address/streetAddress'

    jp = JSONPointer('/address') + 'streetAddress'
    # now in one line
    assert not jp != '/address/streetAddress'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp != '/phoneNumber/0'

    jp = JSONPointer('/phoneNumber') + 0
    assert jp != '/phoneNumber/0/type'

    jp = JSONPointer('/phoneNumber') + 0 + 'number'
    assert jp != '/phoneNumber/0'

    jp = JSONPointer('/address')
    jp = jp + 'streetAddress'
    assert jp != '/address'

    jp = JSONPointer('/phoneNumber') + 0 + 'type'
    assert jp != '/phoneNumber/1/type'


def test_iadd():
    jp = JSONPointer('/foo')
    jp += 'bar'
    assert str(jp) == '/foo/bar'

    jp += 0
    assert str(jp) == '/foo/bar/0'

    jp += ''
    assert str(jp) == '/foo/bar/0'

    jp += ['a', 'b', 1, 'c', 234]
    assert str(jp) == '/foo/bar/0/a/b/1/c/234'

    with pytest.raises(JSONPointerException):
        jp += 1.2

    with pytest.raises(JSONPointerException):
        jp += JSONPointer('')


def test_radd(fixture_folder, json_pointer_data):
    serializer = JSONDataSerializer(
        'test', path_list=fixture_folder, no_default_path=True,
        no_sub_data=True, file_list=['data_for_pointer.json'],
        validator=Mode.OFF
    )

    jp = JSONPointer('/streetAddress')
    jp = '/address' + jp
    jp = JSONPointer(jp)

    # now in one line
    assert serializer.data["address"]["streetAddress"] == \
           jp.get_node_or_value(serializer.data)

    jp = '/address' + JSONPointer('/streetAddress')
    jp = JSONPointer(jp)

    # now in one line
    assert serializer.data["address"]["streetAddress"] == \
           jp.get_node_or_value(serializer.data)

    jp = JSONPointer('/address' + JSONPointer('/streetAddress'))

    # now in one line
    assert serializer.data["address"]["streetAddress"] == \
           jp.get_node_or_value(serializer.data)

    jp = '/phoneNumber' + JSONPointer('0') + '/type'
    assert serializer.data["phoneNumber"][0]["type"] == \
           JSONPointer(jp).get_node_or_value(serializer.data)

    jp = JSONPointer('/phoneNumber/' + str(0) + JSONPointer('type'))
    assert serializer.data["phoneNumber"][0]["type"] == \
           jp.get_node_or_value(serializer.data)

    jp = 0 + JSONPointer('type')
    jp = '/phoneNumber' + jp
    assert serializer.data["phoneNumber"][0]["type"] == \
           JSONPointer(jp).get_node_or_value(serializer.data)

    for l in ('domestic', 'abroad'):
        for n in (0, 1):
            cdata = serializer.data["customers"][l][n]["name"]
            jdata = json_pointer_data["customers"][l][n]["name"]
            assert cdata == jdata

            jp = JSONPointer('/customers/%s/%s' % (l, n) + JSONPointer('name'))
            assert cdata == jp.get_node_or_value(serializer.data)

            jp = JSONPointer('/customers/%s/%s' % (l, n)) + JSONPointer('name')
            assert cdata == jp.get_node_or_value(serializer.data)


def test_repr():
    jp = JSONPointer('/streetAddress/address')
    assert repr(jp) == "JSONPointer(['streetAddress', 'address'])"

    jp = JSONPointer('/streetAddress/address')
    assert str(jp) == '/streetAddress/address'


@pytest.mark.parametrize('json_data_serializer',
                         [Mode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_get_node_exist(json_data_serializer, fixture_folder):
    # partial schema for branch, use here a subtree of main schema
    serializer = json_data_serializer
    schema = {
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }
    target, remaining = \
        JSONPointer('/phoneNumber/-').get_existing_node(serializer.data)

    data_file = fixture_folder / 'branch0.json'
    assert serializer.json_import(target, remaining[0], data_file,
                                  schema=schema)

    assert serializer.data == {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {
                'type': 'home', 'number': '212 555-1234',
                'active': True,
                'private': False,
                'addons': None,
                'index': 0,
                'testnumber': 1.5

            },
            {'type': 'office', 'number': '313 444-555'},
            {'type': 'mobile', 'number': '777 666-555'},
            {'type': 'home0', 'number': '000 222-333'}
        ],
    }


@pytest.mark.parametrize('json_data_serializer',
                         [Mode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_get_node(json_data_serializer, fixture_folder):
    serializer = json_data_serializer
    schema = {
        '$schema': 'http://json-schema.org/draft-03/schema',
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }
    target = JSONPointer("/phoneNumber/0").get_node(serializer.data)

    data_file = fixture_folder / 'branch1.json'
    assert serializer.json_import(target, None, data_file, schema=schema)

    assert serializer.data == {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {'type': 'home1', 'number': '111 222-333'},
            {'type': 'office', 'number': '313 444-555'},
            {'type': 'mobile', 'number': '777 666-555'},
        ],
    }


@pytest.mark.parametrize('json_data_serializer',
                         [Mode.DRAFT4],
                         indirect=['json_data_serializer'])
def test_get_node_again(json_data_serializer, fixture_folder):
    serializer = json_data_serializer
    schema = {
        '$schema': 'http://json-schema.org/draft-03/schema',
        'phoneNumber': serializer.schema['properties']['phoneNumber']
    }

    data_file = fixture_folder / 'branch2.json'
    target = JSONPointer("/phoneNumber/1").get_node(serializer.data)
    assert serializer.json_import(target, None, data_file, schema=schema)

    target = JSONPointer("/phoneNumber/2").get_node(serializer.data)
    assert serializer.json_import(target, None, data_file, schema=schema)

    assert serializer.data == {
        'address': {
            'city': 'New York',
            'streetAddress': '21 2nd Street',
            'houseNumber': 12
        },
        'phoneNumber': [
            {
                'type': 'home', 'number': '212 555-1234',
                'active': True,
                'private': False,
                'addons': None,
                'index': 0,
                'testnumber': 1.5

            },
            {'type': 'home2', 'number': '222 222-333'},
            {'type': 'home2', 'number': '222 222-333'},
        ],
    }