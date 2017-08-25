import pytest

from jsondata.data import Mode, JSONData
from jsondata.patch import JSONPatch, JSONPatchItem


def test_create_patch_task_list():
    json_data = JSONData({'foo': 'bar'}, validator=Mode.OFF)

    json_patch_list = JSONPatch()
    for i in range(10):
        json_patch_list += JSONPatchItem("add", "/a%s" % i, 'v%s' % i)

    ref = '[{}]'.format(
        ','.join("{{'op': 'add', 'path': '/a{0}', 'value': 'v{0}'}}".format(i)
                 for i in range(10))
    )
    assert ref == repr(json_patch_list)

    count, errors = json_patch_list.apply(json_data)
    ref = {'a1': 'v1', 'a0': 'v0', 'a3': 'v3', 'a2': 'v2', 'a5': 'v5',
           'a4': 'v4', 'a7': 'v7', 'a6': 'v6', 'a9': 'v9', 'a8': 'v8',
           'foo': 'bar'}

    assert count == 10
    assert errors == []
    assert json_data.data == ref
