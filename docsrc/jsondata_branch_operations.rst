Process branch data by 'jsondata.JSONData' 
******************************************

The module jsondata.JSONData provides for the operations on data structures,
whereas it relies for the syntax operations on 'json' and compatible compatible
packages.

The design is implemented as a container class providing high level structure 
operations and the access to the data structures by the standard by low-level 
native Python operations.
 
Provided basic operations are:

* **native access attributes**:  The node addresses for the native access to 
  the JSON in-memory representation. The data format is compatible to the 
  packages 'json' and 'jsonschema', e.g. also to 'ujson'. Thus provides
  native Python access performance.

* **branch operations**:  Handle complete sub structures as logical branches
  of a main JSON document. The interface is designed in accordance to RFC6902
  with extension for Python specifics.

* **tree utilities**: Generic tree functions for the provided in-memory
  representation by 'json' and 'jsonschema'.

Syntax Elements
===============
The current release provides the following operators for the class 'JSONPointer'.

Native JSON representation access attributes::

   attr := data, schema

Branch operations(branch_<ops>), see RFC6902::

   ops := add | copy | create | move | remove | replace
          test

Branch operators::

   ops := '[]' | '()'


Generic operations::

   ops := getTreeDiff | getPointerPath | getValueNode


Examples 
========

Examples for the provided basic calculations are:

Create,Add
----------

* **Branch Operations - create a JSON document, add and create branches**::

     import jsondata.JSONData
     import jsondata.JSONPointer

     # JSON document
     jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }
        
     # JSON branch with array
     arr = { 'e': { 'lx': [] } }
        
     # Branch elements for array
     ai0 = { 'v0': 100}
     ai1 = { 'v1': 200}
        
        
     # JSON branch with object
     obj = { 'f': { 'ox': {} } }
        
     # Branch elements for object
     l0 = { 'o0': 10}
     l1 = { 'o1': 20}
        
        
     # JSON in-memory document
     D = JSONData(jdata)
        
        
     # Add a branch with an array
     D.branch_add(JSONPointer('/a/b'),'e',arr['e'])
        
     # Add a items to the new array
     # Remark: for '-' refer to RFC6901 - array-index
     D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai0)
     D.branch_add(JSONPointer('/a/b/e/lx'),'-',ai1)
        
        
     # Add a branch with an object
     D.branch_add(JSONPointer('/a/b'),'f',obj['f'])
        
     # Add an item to the new object, from an object
     D.branch_add(JSONPointer('/a/b/f/ox'),'v0',ai0['v0'])
        
     # Add an item to the new object
     ai1v1 = ai1['v1']
     D.branch_add(JSONPointer('/a/b/f/ox'),'v1',ai1v1)


     nodex = JSONPointer(['a','b']).get_node(D.data)
     ret = D.branch_create(nodex, ['g','x'], {})

     ret['x0'] = 22
     ret['x1'] = 33
        
     ret = D.branch_create(nodex, ['g','x','xlst'], [])

     ret.append('first')
     ret.append('second')

     rdata = {'a': {'b': {'c': 2, 'e': {'lx': [{'v0': 100}, 
        {'v1': 200}]}, 
        'd': 3, u'g': {u'x': {'x0': 22, 'x1': 33, 
        u'xlst': ['first', 'second']}}, 
        'f': {'ox': {'v0': 100, 'v1': 200}}}}
     }
     assert D.data == rdata

     print D


  prints the result::

    {
        "a": {
            "b": {
                "c": 2, 
                "e": {
                    "lx": [
                        {
                            "v0": 100
                        }, 
                        {
                            "v1": 200
                        }
                    ]
                }, 
                "d": 3, 
                "g": {
                    "x": {
                        "x0": 22, 
                        "x1": 33, 
                        "xlst": [
                            "first", 
                            "second"
                        ]
                    }
                }, 
                "f": {
                    "ox": {
                        "v0": 100, 
                        "v1": 200
                    }
                }
            }
        }
    }
    

Access values
-------------

* **Branch Operations - various access to values**::

    print D(['a', 'b', 'c'])

    print D(JSONPointer('/a/b/c'))

    print D('/a/b/c')

    n = JSONPointer('/a/b/c').get_node(D.data,True)
    print n['c']

    n = JSONPointer('/a/b/c').get_node(D.data,True)
    px = D.getPointerPath(n, D.data)[0]
    px.append('c')
    print D(JSONPointer(px))

  prints the result::

    2
    2
    2
    2
    2

Move
----

* **Branch Operations - move a branch**::


    target = JSONPointer('/a/b/new')
    source = JSONPointer('/a/b/c')

    print D(source)
    n = D('/a/b')
    n['c'] = 77

    targetnode = target.get_node(D.data,True)
    sourcenode = source.get_node(D.data,True)

    D.branch_move(targetnode, 'new', sourcenode, 'c')
    print D(target)

    # check new position
    assert D(target) == 77 
        
    # validate old position
    try:
        x = D('/a/b/c')
    except JSONPointerException as e:
        pass
    else:
        raise
 
  prints the result::

    2
    77

Remove
------

* **Branch Operations - remove a branch**::

	# get a pointer
    target     = JSONPointer('/a/b/new')

	# get the parent node for the pointer
    targetnode = target.get_node(D.data,True)

    # verify existence
    x = D('/a/b/new')
    assert x == 77

    # remove item
    D.branch_remove(targetnode, 'new')

    # validate old position
    try:
        x = D('/a/b/new')
    except JSONPointerException as e:
        pass
    else:
        raise
    pass

Replace
-------

* **Branch Operations - replace a branch**::

    # does not verify childnode, when 'parent=True' <=> 'new' does no longer exist
    targetnode = JSONPointer('/a/b/new').get_node(D.data,True)

	# new item
    sourcenode = {'alternate': 4711 }

    # replace old by new item
    ret = D.branch_replace(targetnode, 'f', sourcenode)
    assert ret == True

    # verify new item
    x = D('/a/b/f/alternate')
    assert x == 4711


Test
----

* **Branch Operations - test value**::

    # variant 0
    ret = D.branch_test(JSONPointer('/a/b/f/alternate').get_node_or_value(D.data), 4711)
    assert ret == True

    # variant 1
    ret = D.branch_test(JSONPointer('/a/b/f/alternate')(D.data), 4711)
    assert ret == True

    # variant 2
    p = JSONPointer('/a/b/f/alternate')
    ret = D.branch_test(p(D.data), 4711)
    assert ret == True

Copy
----

* **Branch Operations - copy branch**::

     # JSON branch with array
     arr = { 'cpy': { 'cx': [ 2, 3, 4, ] } }

     # Copy a branch with an array
     D.branch_copy(JSONPointer('/a/b'),'cpy',arr['cpy'])

    

