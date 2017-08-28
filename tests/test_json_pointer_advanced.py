import copy
import pytest

from jsondata.exceptions import JSONPointerException
from jsondata.pointer import JSONPointer


@pytest.mark.parametrize(
    'pointer,result',
    [
        ('', {"foo": ["bar", "baz"], "": 0, "a/b": 1, "c%d": 2, "e^f": 3,
              "g|h": 4, "i\\j": 5, "k\"l": 6, " ": 7, "m~n": 8}),
        ('/foo', ["bar", "baz"]),
        ('/foo/0', 'bar'),
        ('/', 0),
        ('/a~1b', 1),
        ('/c%d', 2),
        ("/e^f", 3),
        ("/g|h", 4),
        ("/i\\j", 5),
        ("/k\"l", 6),
        ("/ ", 7),
        ("/m~0n", 8),
    ]
)
def test_example(pointer, result):
    doc = {
        "foo": ["bar", "baz"],
        "": 0,
        "a/b": 1,
        "c%d": 2,
        "e^f": 3,
        "g|h": 4,
        "i\\j": 5,
        "k\"l": 6,
        " ": 7,
        "m~n": 8
    }

    p = JSONPointer(pointer)
    assert p.get_node_or_value(doc) == result


@pytest.mark.skip
def test_eol():
    doc = {
        "foo": ["bar", "baz"]
    }
    p = JSONPointer('/foo/-')
    node, _ = p.get_existing_node(doc)
    assert node == ['bar', 'baz']

    p = JSONPointer('/foo/-/1')
    with pytest.raises(JSONPointerException):
        p.get_node_or_value(doc)


def test_round_trip():
    paths = [
        "",
        "/foo",
        "/foo/0",
        "/",
        "/a~1b",
        "/c%d",
        "/e^f",
        "/g|h",
        "/i\\j",
        "/k\"l",
        "/ ",
        "/m~0n",
        "/\xee",
    ]
    for path in paths:
        ptr = JSONPointer(path)
        assert path == ptr.raw

        new_ptr = JSONPointer(ptr.path)
        assert ptr == new_ptr


@pytest.mark.parametrize(
    'pointer,uri,rfc6901,python_repr',
    [
        ("", "#", "", "JSONPointer([])"),
        ("/foo", "#/foo", "/foo", "JSONPointer(['foo'])"),
        ("/foo/0", "#/foo/0", "/foo/0", "JSONPointer(['foo', 0])"),
        ("/", "#/", "/", "JSONPointer([''])"),
        ("/a~1b", "#/a~1b", "/a/b", "JSONPointer(['a/b'])"),
        ("/c%d", "#/c%25d", "/c%d", "JSONPointer(['c%d'])"),
        ("/e^f", "#/e%5Ef", "/e^f", "JSONPointer(['e^f'])"),
        ("/g|h", "#/g%7Ch", "/g|h", "JSONPointer(['g|h'])"),
        ('/i\\j', "#/i%5Cj", '/i\\j', "JSONPointer(['i\\\\j'])"),
        ("/k\"l", "#/k%22l", '/k"l', "JSONPointer(['k\"l'])"),
        ("/ ", "#/%20", "/ ", "JSONPointer([' '])"),
        ("/m~0n", "#/m~0n", "/m~n", "JSONPointer(['m~n'])"),
        ("/\xee", "#/%C3%AE", "/î", "JSONPointer(['î'])"),
    ]
)
def test_representations(pointer, uri, rfc6901, python_repr):
    assert JSONPointer(pointer).uri == uri
    assert JSONPointer(pointer).raw == pointer
    assert JSONPointer(pointer).rfc6901 == rfc6901
    assert JSONPointer(uri).rfc6901 == rfc6901
    assert str(JSONPointer(pointer)) == rfc6901
    assert str(JSONPointer(uri)) == rfc6901
    assert str(JSONPointer(rfc6901)) == rfc6901
    assert repr(JSONPointer(pointer)) == python_repr
    assert JSONPointer(pointer) == eval(repr(JSONPointer(pointer)))


def test_eq_hash():
    p1 = JSONPointer("/something/1/b")
    p2 = JSONPointer("/something/1/b")
    p3 = JSONPointer("/something/1.0/b")

    assert p1 == p2
    assert p1 != p3
    assert p2 != p3

    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)
    assert hash(p2) != hash(p3)

    # a pointer compares not-equal to objects of other types
    assert p1 == '/something/1/b'


def test_contains():
    ptr1 = JSONPointer("/a/b/c")
    ptr2 = JSONPointer("/a/b")
    ptr3 = JSONPointer("/b/c")

    assert ptr1.contains(ptr2)
    assert ptr1.contains(ptr1)
    assert not ptr1.contains(ptr3)

    assert ptr2 in ptr1
    assert ptr1 in ptr1
    assert ptr3 not in ptr1


def test_invalid_index():
    # 'a' is not a valid list index
    doc = [0, 1, 2]
    with pytest.raises(JSONPointerException):
        JSONPointer('/a').get_node(doc)

    with pytest.raises(JSONPointerException):
        JSONPointer('/10').get_node(doc)


def test_remaining_empty_path():
    doc = {'a': [1, 2, 3]}
    ptr = JSONPointer('')
    node, remaining = ptr.get_existing_node(doc)
    assert doc == node
    assert not remaining


def test_remaining_path():
    doc = {'a': [{'b': 1, 'c': 2}, 5]}
    ptr = JSONPointer('/a/0/d')
    node, remaining = ptr.get_existing_node(doc)
    assert node == {'b': 1, 'c': 2}
    assert remaining == ['d']


def test_set():
    doc = {
        "foo": ["bar", "baz"],
        "": 0,
        "a/b": 1,
        "c%d": 2,
        "e^f": 3,
        "g|h": 4,
        "i\\j": 5,
        "k\"l": 6,
        " ": 7,
        "m~n": 8
    }
    original = copy.deepcopy(doc)

    # inplace=False
    p = JSONPointer('/foo/1')
    new = p.set(doc, 'cod', inplace=False)
    assert p.get_node_or_value(new) == 'cod'

    p = JSONPointer('/')
    new = p.set(doc, 9, inplace=False)
    assert p.get_node_or_value(new) == 9

    p1 = JSONPointer('/fud')
    new = p1.set(doc, {}, inplace=False)
    p2 = JSONPointer('/fud/gaw')
    new = p2.set(new, [1, 2, 3], inplace=False)
    assert p1.get_node_or_value(new) == {'gaw': [1, 2, 3]}

    p = JSONPointer('')
    new = p.set(doc, 9, inplace=False)
    assert new == 9
    assert doc == original

    # inplace=True
    p = JSONPointer('/foo/1')
    p.set(doc, 'cod')
    assert p.get_node_or_value(doc) == "cod"

    p = JSONPointer('/')
    p.set(doc, 9)
    assert p.get_node_or_value(doc) == 9

    p = JSONPointer('/fud/gaw')
    with pytest.raises(JSONPointerException):
        p.set(doc, 9)

    p1 = JSONPointer('/fud')
    p1.set(doc, {})
    p2 = JSONPointer('/fud/gaw')
    p2.set(doc, [1, 2, 3])

    assert p1.get_node_or_value(doc) == {'gaw': [1, 2, 3]}

    p = JSONPointer('')
    with pytest.raises(JSONPointerException):
        p.set(doc, 9)
