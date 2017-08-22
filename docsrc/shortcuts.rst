API Shortcuts - jsondata
************************

jsondata - epydoc
=================
Javadoc style API documentation for Python.

* `API by Epydoc <epydoc/index.html>`_

jsondata - CLI
==============
CLI Wrapper for filtered subprocess calls and streaming of results
`[details] <commandline_tools.html>`_ 
 
* `jsondc <jsondc.html#>`_


jsondata.JSONData
=================

JSONData
--------

  The class JSONData provides branch operations, which actually are logical set operations on structured subsets
  of attributes.
  This comprises basically two types of operations:

  * **branch operations**: 

    The unit of action is a complete branch, thus the branch is not intermixed with other attributes 
    e.g. 'branch_add' or 'branch_copy'.

  * **attribute operations**:

    The unit of action is/are attributes, thus the branches are intermixed, or disjoined at the level of attributes 
    e.g.  '__add__' and '__or__', or '__xor__'.

  The column [op-unit-scope] depicts the types and levels of provided operations:

  * A: attribute 
  * B: branch

Methods
^^^^^^^
  
* **Basic**:

  +---------------------------------+------------------------------+----------------------+--------------------+
  | [docs]                          | [source]                     | [op-unit-scope]      | [logic-operator]   |
  +=================================+==============================+======================+====================+
  | `JSONData`_                     | `JSONData.__init__`_         |                      |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__repr__`_                     | `JSONData.__repr__`_         | B,A                  |  repr              |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__str__`_                      | `JSONData.__str__`_          | B,A                  |  str               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `get_data`_                      | `JSONData.get_data`_          |                      |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `get_schema`_                    | `JSONData.get_schema`_        |                      |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `print_data`_                    | `JSONData.print_data`_        | A                    |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `print_schema`_                  | `JSONData.print_schema`_      |                      |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `set_schema`_                    | `JSONData.set_schema`_        |                      |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `validate`_                     | `JSONData.validate`_         | B,A                  |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+

  .

* **Branches and Trees**:

  +---------------------------------+------------------------------+----------------------+--------------------+
  | [docs]                          | [source]                     | [op-unit-scope]      | [logic-operator]   |
  +=================================+==============================+======================+====================+
  | `branch_add`_                   | `JSONData.branch_add`_       | B                    |  add               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_copy`_                  | `JSONData.branch_copy`_      | B                    |  cp                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_create`_                | `JSONData.branch_create`_    | B                    |  new               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_move`_                  | `JSONData.branch_move`_      | B                    |  mv                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_remove`_                | `JSONData.branch_remove`_    | B                    |  del               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_replace`_               | `JSONData.branch_replace`_   | B                    |  replace           |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `branch_test`_                  | `JSONData.branch_test`_      | B                    |  test              |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `get_tree_diff`_                  | `JSONData.get_tree_diff`_      | B,A                  |  diff              |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `get_pointer_path`_               | `JSONData.get_pointer_path`_   | B,A                  |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `get_canonical`_                 | `JSONData.get_canonical`_     | B                    |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `is_applicable`_                 | `JSONData.is_applicable`_     | B                    |                    |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `pop`_                          | `JSONData.pop`_              |                      |  pop               |
  +---------------------------------+------------------------------+----------------------+--------------------+

Operators
^^^^^^^^^

  +---------------------------------+------------------------------+----------------------+--------------------+
  | [docs]                          | [source]                     | [op-unit-scope]      | [logic-operator]   |
  +=================================+==============================+======================+====================+
  | `__add__`_                      | `JSONData.__add__`_          | B,A                  |  \+                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__and__`_                      | `JSONData.__and__`_          | B,A                  |  &&                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__call__`_                     | `JSONData.__call__`_         | A                    |  exec              |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__eq__`_                       | `JSONData.__eq__`_           | B,A                  |  ==                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__getitem__`_                  | `JSONData.__getitem__`_      | B,A                  |  f(x)              |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__iadd__`_                     | `JSONData.__iadd__`_         | B,A                  |  +=                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__iand__`_                     | `JSONData.__rand__`_         | B,A                  |  &&=               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__imod__`_                     | `JSONData.__imod__`_         | B,A                  |  %                 |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__imul__`_                     | `JSONData.__imul__`_         | B,A                  |  \*                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__ior__`_                      | `JSONData.__ior__`_          | B,A                  |  ||=               |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__isub__`_                     | `JSONData.__isub__`_         | B,A                  |  \-                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__ixor__`_                     | `JSONData.__ixor__`_         | B,A                  |  ^                 |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__mod__`_                      | `JSONData.__mod__`_          | B,A                  |  %                 |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__mul__`_                      | `JSONData.__mul__`_          | B,A                  |  \*                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__ne__`_                       | `JSONData.__ne__`_           | B,A                  |  !=                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__or__`_                       | `JSONData.__or__`_           | B,A                  |  ||                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__radd__`_                     | `JSONData.__radd__`_         | B,A                  |  S \+ x            |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__rand__`_                     | `JSONData.__rand__`_         | B,A                  |  S && x            |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__rmod__`_                     | `JSONData.__rmod__`_         | B,A                  |  %                 |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__rmul__`_                     | `JSONData.__rmul__`_         | B,A                  |  \*                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__ror__`_                      | `JSONData.__ror__`_          | B,A                  |  S || x            |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__rsub__`_                     | `JSONData.__rsub__`_         | B,A                  |  \-                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__rxor__`_                     | `JSONData.__rxor__`_         | B,A                  |  ^                 |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__sub__`_                      | `JSONData.__sub__`_          | B,A                  |  \-                |
  +---------------------------------+------------------------------+----------------------+--------------------+
  | `__xor__`_                      | `JSONData.__xor__`_          | B,A                  |  ^                 |
  +---------------------------------+------------------------------+----------------------+--------------------+

Iterators
^^^^^^^^^

  +---------------------------------+------------------------------+----------------------+--------------------+
  | [docs]                          | [source]                     | [op-unit-scope]      | [logic-operator]   |
  +=================================+==============================+======================+====================+
  | `__iter__`_                     | `JSONData.__iter__`_         | B,A                  |  ->                |
  +---------------------------------+------------------------------+----------------------+--------------------+

.. _JSONData: jsondata_m_data.html#jsondata.JSONData.JSONData.__init__
.. _JSONData.__init__: _modules/jsondata/JSONData.html#JSONData.__init__

.. _\__call__: jsondata_m_data.html#jsondata.JSONData.JSONData.__call__
.. _JSONData.__call__: _modules/jsondata/JSONData.html#JSONData.__call__

.. _\__eq__: jsondata_m_data.html#jsondata.JSONData.JSONData.__eq__
.. _JSONData.__eq__: _modules/jsondata/JSONData.html#JSONData.__eq__

.. _\__repr__: jsondata_m_data.html#jsondata.JSONData.JSONData.__repr__
.. _JSONData.__repr__: _modules/jsondata/JSONData.html#JSONData.__repr__

.. _\__str__: jsondata_m_data.html#jsondata.JSONData.JSONData.__str__
.. _JSONData.__str__: _modules/jsondata/JSONData.html#JSONData.__str__

.. _\__getitem__: jsondata_m_data.html#jsondata.JSONData.JSONData.__getitem__
.. _JSONData.__getitem__: _modules/jsondata/JSONData.html#JSONData.__getitem__

.. _\__iter__: jsondata_m_data.html#jsondata.JSONData.JSONData.__iter__
.. _JSONData.__iter__: _modules/jsondata/JSONData.html#JSONData.__iter__

.. _\__add__: jsondata_m_data.html#jsondata.JSONData.JSONData.__add__
.. _JSONData.__add__: _modules/jsondata/JSONData.html#JSONData.__add__
.. _\__iadd__: jsondata_m_data.html#jsondata.JSONData.JSONData.__iadd__
.. _JSONData.__iadd__: _modules/jsondata/JSONData.html#JSONData.__iadd__
.. _\__radd__: jsondata_m_data.html#jsondata.JSONData.JSONData.__radd__
.. _JSONData.__radd__: _modules/jsondata/JSONData.html#JSONData.__radd__

.. _\__and__: jsondata_m_data.html#jsondata.JSONData.JSONData.__and__
.. _JSONData.__and__: _andules/jsondata/JSONData.html#JSONData.__and__
.. _\__iand__: jsondata_m_data.html#jsondata.JSONData.JSONData.__iand__
.. _JSONData.__iand__: _andules/jsondata/JSONData.html#JSONData.__iand__
.. _\__rand__: jsondata_m_data.html#jsondata.JSONData.JSONData.__rand__
.. _JSONData.__rand__: _andules/jsondata/JSONData.html#JSONData.__rand__

.. _\__mod__: jsondata_m_data.html#jsondata.JSONData.JSONData.__mod__
.. _JSONData.__mod__: _modules/jsondata/JSONData.html#JSONData.__mod__
.. _\__imod__: jsondata_m_data.html#jsondata.JSONData.JSONData.__imod__
.. _JSONData.__imod__: _modules/jsondata/JSONData.html#JSONData.__imod__
.. _\__rmod__: jsondata_m_data.html#jsondata.JSONData.JSONData.__rmod__
.. _JSONData.__rmod__: _modules/jsondata/JSONData.html#JSONData.__rmod__

.. _\__mul__: jsondata_m_data.html#jsondata.JSONData.JSONData.__mul__
.. _JSONData.__mul__: _modules/jsondata/JSONData.html#JSONData.__mul__
.. _\__imul__: jsondata_m_data.html#jsondata.JSONData.JSONData.__imul__
.. _JSONData.__imul__: _modules/jsondata/JSONData.html#JSONData.__imul__
.. _\__rmul__: jsondata_m_data.html#jsondata.JSONData.JSONData.__rmul__
.. _JSONData.__rmul__: _modules/jsondata/JSONData.html#JSONData.__rmul__

.. _\__or__: jsondata_m_data.html#jsondata.JSONData.JSONData.__or__
.. _JSONData.__or__: _modules/jsondata/JSONData.html#JSONData.__or__
.. _\__ior__: jsondata_m_data.html#jsondata.JSONData.JSONData.__ior__
.. _JSONData.__ior__: _modules/jsondata/JSONData.html#JSONData.__ior__
.. _\__ror__: jsondata_m_data.html#jsondata.JSONData.JSONData.__ror__
.. _JSONData.__ror__: _modules/jsondata/JSONData.html#JSONData.__ror__

.. _\__sub__: jsondata_m_data.html#jsondata.JSONData.JSONData.__sub__
.. _JSONData.__sub__: _modules/jsondata/JSONData.html#JSONData.__sub__
.. _\__isub__: jsondata_m_data.html#jsondata.JSONData.JSONData.__isub__
.. _JSONData.__isub__: _modules/jsondata/JSONData.html#JSONData.__isub__
.. _\__rsub__: jsondata_m_data.html#jsondata.JSONData.JSONData.__rsub__
.. _JSONData.__rsub__: _modules/jsondata/JSONData.html#JSONData.__rsub__

.. _\__xor__: jsondata_m_data.html#jsondata.JSONData.JSONData.__xor__
.. _JSONData.__xor__: _modules/jsondata/JSONData.html#JSONData.__xor__
.. _\__ixor__: jsondata_m_data.html#jsondata.JSONData.JSONData.__ixor__
.. _JSONData.__ixor__: _modules/jsondata/JSONData.html#JSONData.__ixor__
.. _\__rxor__: jsondata_m_data.html#jsondata.JSONData.JSONData.__rxor__
.. _JSONData.__rxor__: _modules/jsondata/JSONData.html#JSONData.__rxor__


.. _\__ne__: jsondata_m_data.html#jsondata.JSONData.JSONData.__ne__
.. _JSONData.__ne__: _modules/jsondata/JSONData.html#JSONData.__ne__

.. _branch_add: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_add
.. _JSONData.branch_add: _modules/jsondata/JSONData.branch_add

.. _branch_copy: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_copy
.. _JSONData.branch_copy: _modules/jsondata/JSONData.html#JSONData.branch_copy

.. _branch_create: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_create
.. _JSONData.branch_create: _modules/jsondata/JSONData.html#JSONData.branch_create

.. _branch_move: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_move
.. _JSONData.branch_move: _modules/jsondata/JSONData.html#JSONData.branch_move

.. _branch_remove: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_remove
.. _JSONData.branch_remove: _modules/jsondata/JSONData.html#JSONData.branch_remove

.. _branch_replace: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_replace
.. _JSONData.branch_replace: _modules/jsondata/JSONData.html#JSONData.branch_replace

.. _branch_test: jsondata_m_data.html#jsondata.JSONData.JSONData.branch_test
.. _JSONData.branch_test: _modules/jsondata/JSONData.html#JSONData.branch_test

.. _getTreeDiff: jsondata_m_data.html#jsondata.JSONData.JSONData.get_tree_diff
.. _JSONData.get_tree_diff: _modules/jsondata/JSONData.html#JSONData.get_tree_diff

.. _getPointerPath: jsondata_m_data.html#jsondata.JSONData.JSONData.get_pointer_path
.. _JSONData.get_pointer_path: _modules/jsondata/JSONData.html#JSONData.get_pointer_path

.. _getData: jsondata_m_data.html#jsondata.JSONData.JSONData.get_data
.. _JSONData.get_data: _modules/jsondata/JSONData.html#JSONData.get_data

.. _getSchema: jsondata_m_data.html#jsondata.JSONData.JSONData.get_schema
.. _JSONData.get_schema: _modules/jsondata/JSONData.html#JSONData.get_schema

.. _getCanonical: jsondata_m_data.html#jsondata.JSONData.JSONData.get_canonical
.. _JSONData.get_canonical: _modules/jsondata/JSONData.html#JSONData.get_canonical

.. _isApplicable: jsondata_m_data.html#jsondata.JSONData.JSONData.is_applicable
.. _JSONData.is_applicable: _modules/jsondata/JSONData.html#JSONData.is_applicable

.. _pop: jsondata_m_data.html#jsondata.JSONData.JSONData.pop
.. _JSONData.pop: _modules/jsondata/JSONData.html#JSONData.pop

.. _printData: jsondata_m_data.html#jsondata.JSONData.JSONData.print_data
.. _JSONData.print_data: _modules/jsondata/JSONData.html#JSONData.print_data

.. _printSchema: jsondata_m_data.html#jsondata.JSONData.JSONData.print_schema
.. _JSONData.print_schema: _modules/jsondata/JSONData.html#JSONData.print_schema

.. _setSchema: jsondata_m_data.html#jsondata.JSONData.JSONData.set_schema
.. _JSONData.set_schema: _modules/jsondata/JSONData.html#JSONData.set_schema

.. _validate: jsondata_m_data.html#jsondata.JSONData.JSONData.validate
.. _JSONData.validate: _modules/jsondata/JSONData.html#JSONData.validate


jsondata.JSONDataSerializer
===========================

JSONDataSerializer
------------------

Methods
^^^^^^^

* **Basic**

  +---------------------------------+----------------------------------------------------+
  | [docs]                          | [source]                                           | 
  +=================================+====================================================+
  | `JSONDataSerializer`_           | `JSONDataSerializer.__init__`_                     |
  +---------------------------------+----------------------------------------------------+
  | `print_data (1)`_                | `JSONDataSerializer.print_data`_                    |
  +---------------------------------+----------------------------------------------------+
  | `print_schema (1)`_              | `JSONDataSerializer.print_schema`_                  |
  +---------------------------------+----------------------------------------------------+
  | `set_schema (1)`_                | `JSONDataSerializer.set_schema`_                    |
  +---------------------------------+----------------------------------------------------+

* **Import/Export**

  +---------------------------------+----------------------------------------------------+
  | [docs]                          | [source]                                           | 
  +=================================+====================================================+
  | `json_export`_                  | `JSONDataSerializer.json_export`_                  |
  +---------------------------------+----------------------------------------------------+
  | `json_import`_                  | `JSONDataSerializer.json_import`_                  |
  +---------------------------------+----------------------------------------------------+

.. _JSONDataSerializer.__init__: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.__init__
.. _JSONDataSerializer: jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.__init__

.. _JSONDataSerializer.json_export: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.json_export
.. _json_export: jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.json_export

.. _JSONDataSerializer.json_import: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.json_import
.. _json_import: jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.json_import

.. _JSONDataSerializer.print_data: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.print_data
.. _printData (1): jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.print_data

.. _JSONDataSerializer.print_schema: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.print_schema
.. _printSchema (1): jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.print_schema

.. _JSONDataSerializer.set_schema: _modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.set_schema
.. _setSchema (1): jsondata_m_serializer.html#jsondata.JSONDataSerializer.JSONDataSerializer.set_schema


jsondata.JSONPatch
==================

JSONPatchItem
-------------

Methods
^^^^^^^

* **Basic**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `JSONPatchItem`_                | `JSONPatchItem.__init__`_                          |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__repr__ (2)`_                 | `JSONPatchItem.__repr__`_                          | repr               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__str__ (2)`_                  | `JSONPatchItem.__str__`_                           | str                |
  +---------------------------------+----------------------------------------------------+--------------------+

* **Basic**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `apply (2)`_                    | `JSONPatchItem.apply`_                             |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `repr_export (2)`_              | `JSONPatchItem.repr_export`_                       |                    |
  +---------------------------------+----------------------------------------------------+--------------------+

Operators
^^^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `__call__ (2)`_                 | `JSONPatchItem.__call__`_                          | exec               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__eq__ (2)`_                   | `JSONPatchItem.__eq__`_                            | ==                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__getitem__ (2)`_              | `JSONPatchItem.__getitem__`_                       | [i]                |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__ne__ (2)`_                   | `JSONPatchItem.__ne__`_                            | !=                 |
  +---------------------------------+----------------------------------------------------+--------------------+

.. _JSONPatchItem.__init__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__init__
.. _JSONPatchItem: jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__init__

.. _JSONPatchItem.__call__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__call__
.. _\__call__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__call__

.. _JSONPatchItem.__eq__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__eq__
.. _\__eq__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__eq__

.. _JSONPatchItem.__getitem__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__getitem__
.. _\__getitem__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__getitem__

.. _JSONPatchItem.__ne__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__ne__
.. _\__ne__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__ne__

.. _JSONPatchItem.__repr__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__repr__
.. _\__repr__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__repr__

.. _JSONPatchItem.__str__: _modules/jsondata/JSONPatch.html#JSONPatchItem.__str__
.. _\__str__ (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.__str__

.. _JSONPatchItem.apply: _modules/jsondata/JSONPatch.html#JSONPatchItem.apply
.. _apply (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.apply

.. _JSONPatchItem.repr_export: _modules/jsondata/JSONPatch.html#JSONPatchItem.repr_export
.. _repr_export (2): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItem.repr_export


JSONPatchItemRaw
----------------

Methods
^^^^^^^

  +---------------------------------+----------------------------------------------------+
  | [docs]                          | [source]                                           | 
  +=================================+====================================================+
  | `JSONPatchItemRaw`_             | `JSONPatchItemRaw.__init__`_                       |
  +---------------------------------+----------------------------------------------------+

.. _JSONPatchItemRaw.__init__: _modules/jsondata/JSONPatch.html#JSONPatchItemRaw.__init__
.. _JSONPatchItemRaw: jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchItemRaw.__init__

JSONPatchFilter
---------------

Methods
^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `JSONPatchFilter`_              | `JSONPatchFilter.__init__`_                        |                    |
  +---------------------------------+----------------------------------------------------+--------------------+

Operators
^^^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `__eq__ (4)`_                   | `JSONPatchFilter.__eq__`_                          | ==                 |
  +---------------------------------+----------------------------------------------------+--------------------+

.. _JSONPatchFilter.__init__: _modules/jsondata/JSONPatch.html#JSONPatchFilter.__init__
.. _JSONPatchFilter: jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchFilter.__init__

.. _JSONPatchFilter.__eq__: _modules/jsondata/JSONPatch.html#JSONPatchFilter.__eq__
.. _\__eq__ (4): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatchFilter.__eq__


JSONPatch
---------

Methods
^^^^^^^

* **Basic**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `JSONPatch`_                    | `JSONPatch.__init__`_                              |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__repr__ (5)`_                 | `JSONPatch.__repr__`_                              | repr               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__str__ (5)`_                  | `JSONPatch.__str__`_                               | str                |
  +---------------------------------+----------------------------------------------------+--------------------+

* **Patch**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `apply (5)`_                    | `JSONPatch.apply`_                                 |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get (5)`_                      | `JSONPatch.get`_                                   |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `patch_export (5)`_             | `JSONPatch.patch_export`_                          |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `patch_import (5)`_             | `JSONPatch.patch_import`_                          |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `repr_export (5)`_              | `JSONPatch.repr_export`_                           |                    |
  +---------------------------------+----------------------------------------------------+--------------------+

Operators
^^^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `__add__ (5)`_                  | `JSONPatch.__add__`_                               | \+                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__call__ (5)`_                 | `JSONPatch.__call__`_                              | exec               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__eq__ (5)`_                   | `JSONPatch.__eq__`_                                | ==                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__getitem__ (5)`_              | `JSONPatch.__getitem__`_                           | [i]                |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__iadd__ (5)`_                 | `JSONPatch.__iadd__`_                              | +=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__isub__ (5)`_                 | `JSONPatch.__isub__`_                              | -=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__ne__ (5)`_                   | `JSONPatch.__ne__`_                                | !=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__sub__ (5)`_                  | `JSONPatch.__sub__`_                               | \-                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__len__ (5)`_                  | `JSONPatch.__len__`_                               | len                |
  +---------------------------------+----------------------------------------------------+--------------------+

Iterators
^^^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `__iter__ (5)`_                 | `JSONPatch.__iter__`_                              | ->                 |
  +---------------------------------+----------------------------------------------------+--------------------+

.. _JSONPatch.__init__: _modules/jsondata/JSONPatch.html#JSONPatch.__init__
.. _JSONPatch: jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__init__

.. _JSONPatch.__add__: _modules/jsondata/JSONPatch.html#JSONPatch.__add__
.. _\__add__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__add__

.. _JSONPatch.__call__: _modules/jsondata/JSONPatch.html#JSONPatch.__call__
.. _\__call__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__call__

.. _JSONPatch.__eq__: _modules/jsondata/JSONPatch.html#JSONPatch.__eq__
.. _\__eq__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__eq__

.. _JSONPatch.__getitem__: _modules/jsondata/JSONPatch.html#JSONPatch.__getitem__
.. _\__getitem__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__getitem__

.. _JSONPatch.__iadd__: _modules/jsondata/JSONPatch.html#JSONPatch.__iadd__
.. _\__iadd__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__iadd__

.. _JSONPatch.__isub__: _modules/jsondata/JSONPatch.html#JSONPatch.__isub__
.. _\__isub__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__isub__

.. _JSONPatch.__iter__: _modules/jsondata/JSONPatch.html#JSONPatch.__iter__
.. _\__iter__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__iter__

.. _JSONPatch.__len__: _modules/jsondata/JSONPatch.html#JSONPatch.__len__
.. _\__len__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__len__

.. _JSONPatch.__ne__: _modules/jsondata/JSONPatch.html#JSONPatch.__ne__
.. _\__ne__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__ne__

.. _JSONPatch.__repr__: _modules/jsondata/JSONPatch.html#JSONPatch.__repr__
.. _\__repr__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__repr__

.. _JSONPatch.__str__: _modules/jsondata/JSONPatch.html#JSONPatch.__str__
.. _\__str__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__str__

.. _JSONPatch.__sub__: _modules/jsondata/JSONPatch.html#JSONPatch.__sub__
.. _\__sub__ (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.__sub__

.. _JSONPatch.apply: _modules/jsondata/JSONPatch.html#JSONPatch.apply
.. _apply (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.apply

.. _JSONPatch.get: _modules/jsondata/JSONPatch.html#JSONPatch.get
.. _get (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.get

.. _JSONPatch.patch_export: _modules/jsondata/JSONPatch.html#JSONPatch.patch_export
.. _patch_export (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.patch_export

.. _JSONPatch.patch_import: _modules/jsondata/JSONPatch.html#JSONPatch.patch_import
.. _patch_import (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.patch_import

.. _JSONPatch.repr_export: _modules/jsondata/JSONPatch.html#JSONPatch.repr_export
.. _repr_export (5): jsondata_m_patch.html#jsondata.JSONPatch.JSONPatch.repr_export


jsondata.JSONPointer
====================

JSONPointer
-----------

Methods
^^^^^^^

* **Basic**:

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   | 
  +=================================+====================================================+====================+
  | `JSONPointer`_                  | `JSONPointer.__init__`_                            |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__repr__ (6)`_                 | `JSONPointer.__repr__`_                            | repr               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__str__ (6)`_                  | `JSONPointer.__str__`_                             | str                |
  +---------------------------------+----------------------------------------------------+--------------------+

* **Nodes**:

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   | 
  +=================================+====================================================+====================+
  | `check_node_or_value`_          | `JSONPointer.check_node_or_value`_                 |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `check_path_list`_              | `JSONPointer.check_path_list`_                     |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_node`_                     | `JSONPointer.get_node`_                            |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_node_and_child`_           | `JSONPointer.get_node_and_child`_                  |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_node_or_value`_            | `JSONPointer.get_node_or_value`_                   |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_node_exist`_               | `JSONPointer.get_node_exist`_                      |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_path_list`_                | `JSONPointer.get_path_list`_                       |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_path_list_and_key`_        | `JSONPointer.get_path_list_and_key`_               |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_pointer`_                  | `JSONPointer.get_pointer`_                         |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `get_raw`_                      | `JSONPointer.get_raw`_                             |                    |
  +---------------------------------+----------------------------------------------------+--------------------+

Operators
^^^^^^^^^

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   | 
  +=================================+====================================================+====================+
  | `__add__ (6)`_                  | `JSONPointer.__add__`_                             | \+                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__call__ (6)`_                 | `JSONPointer.__call__`_                            | exec               |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__eq__ (6)`_                   | `JSONPointer.__eq__`_                              | ==                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__ge__ (6)`_                   | `JSONPointer.__ge__`_                              | >=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__gt__ (6)`_                   | `JSONPointer.__gt__`_                              | >                  |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__iadd__ (6)`_                 | `JSONPointer.__iadd__`_                            | +=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__le__ (6)`_                   | `JSONPointer.__le__`_                              | <=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__lt__ (6)`_                   | `JSONPointer.__lt__`_                              | <                  |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__ne__ (6)`_                   | `JSONPointer.__ne__`_                              | !=                 |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `__radd__ (6)`_                 | `JSONPointer.__radd__`_                            | x+                 |
  +---------------------------------+----------------------------------------------------+--------------------+

Iterators
^^^^^^^^^
  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   | 
  +=================================+====================================================+====================+
  | `iter_path`_                    | `JSONPointer.iter_path`_                           | (path)->           |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `iter_path_nodes`_              | `JSONPointer.iter_path_nodes`_                     | (path-nodes)->     |
  +---------------------------------+----------------------------------------------------+--------------------+

.. _JSONPointer.__init__: _modules/jsondata/JSONPointer.html#JSONPointer.__init__
.. _JSONPointer: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__init__

.. _JSONPointer.__add__: _modules/jsondata/JSONPointer.html#JSONPointer.__add__
.. _\__add__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__add__

.. _JSONPointer.__call__: _modules/jsondata/JSONPointer.html#JSONPointer.__call__
.. _\__call__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__call__

.. _JSONPointer.__eq__: _modules/jsondata/JSONPointer.html#JSONPointer.__eq__
.. _\__eq__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__eq__

.. _JSONPointer.__ge__: _modules/jsondata/JSONPointer.html#JSONPointer.__ge__
.. _\__ge__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__ge__

.. _JSONPointer.__gt__: _modules/jsondata/JSONPointer.html#JSONPointer.__gt__
.. _\__gt__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__gt__

.. _JSONPointer.__iadd__: _modules/jsondata/JSONPointer.html#JSONPointer.__iadd__
.. _\__iadd__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__iadd__

.. _JSONPointer.__le__: _modules/jsondata/JSONPointer.html#JSONPointer.__le__
.. _\__le__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__le__

.. _JSONPointer.__lt__: _modules/jsondata/JSONPointer.html#JSONPointer.__lt__
.. _\__lt__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__lt__

.. _JSONPointer.__ne__: _modules/jsondata/JSONPointer.html#JSONPointer.__ne__
.. _\__ne__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__ne__

.. _JSONPointer.__radd__: _modules/jsondata/JSONPointer.html#JSONPointer.__radd__
.. _\__radd__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__radd__

.. _JSONPointer.__repr__: _modules/jsondata/JSONPointer.html#JSONPointer.__repr__
.. _\__repr__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__repr__

.. _JSONPointer.__str__: _modules/jsondata/JSONPointer.html#JSONPointer.__str__
.. _\__str__ (6): jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.__str__

.. _JSONPointer.check_node_or_value: _modules/jsondata/JSONPointer.html#JSONPointer.check_node_or_value
.. _check_node_or_value: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.check_node_or_value

.. _JSONPointer.check_path_list: _modules/jsondata/JSONPointer.html#JSONPointer.check_path_list
.. _check_path_list: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.check_path_list

.. _JSONPointer.get_node: _modules/jsondata/JSONPointer.html#JSONPointer.get_node
.. _get_node: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_node

.. _JSONPointer.get_node_and_child: _modules/jsondata/JSONPointer.html#JSONPointer.get_node_and_child
.. _get_node_and_child: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_node_and_child

.. _JSONPointer.get_node_or_value: _modules/jsondata/JSONPointer.html#JSONPointer.get_node_or_value
.. _get_node_or_value: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_node_or_value

.. _JSONPointer.get_node_exist: _modules/jsondata/JSONPointer.html#JSONPointer.get_node_exist
.. _get_node_exist: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_node_exist

.. _JSONPointer.get_path_list: _modules/jsondata/JSONPointer.html#JSONPointer.get_path_list
.. _get_path_list: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_path_list

.. _JSONPointer.get_path_list_and_key: _modules/jsondata/JSONPointer.html#JSONPointer.get_path_list_and_key
.. _get_path_list_and_key: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_path_list_and_key

.. _JSONPointer.get_pointer: _modules/jsondata/JSONPointer.html#JSONPointer.get_pointer
.. _get_pointer: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_pointer

.. _JSONPointer.get_raw: _modules/jsondata/JSONPointer.html#JSONPointer.get_raw
.. _get_raw: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.get_raw

.. _JSONPointer.iter_path: _modules/jsondata/JSONPointer.html#JSONPointer.iter_path
.. _iter_path: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.iter_path

.. _JSONPointer.iter_path_nodes: _modules/jsondata/JSONPointer.html#JSONPointer.iter_path_nodes
.. _iter_path_nodes: jsondata_m_pointer.html#jsondata.JSONPointer.JSONPointer.iter_path_nodes

jsondata.JSONTree
=================

JSONTree
--------

Methods
^^^^^^^

* **Basic**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `JSONTree`_                     | `JSONTree.__init__`_                               |                    |
  +---------------------------------+----------------------------------------------------+--------------------+

* **Tree**

  +---------------------------------+----------------------------------------------------+--------------------+
  | [docs]                          | [source]                                           | [logic-operator]   |
  +=================================+====================================================+====================+
  | `print_diff`_                    | `JSONTree.print_diff`_                              |                    |
  +---------------------------------+----------------------------------------------------+--------------------+
  | `fetch_diff`_                    | `JSONTree.fetch_diff`_                              | diff               |
  +---------------------------------+----------------------------------------------------+--------------------+

.. _JSONTree.__init__: _modules/jsondata/JSONTree.html#JSONTree.__init__
.. _JSONTree: jsondata_m_tree.html#jsondata.JSONTree.JSONTree.__init__

.. _JSONTree.print_diff: _modules/jsondata/JSONTree.html#JSONTree.print_diff
.. _printDiff: jsondata_m_tree.html#jsondata.JSONTree.JSONTree.print_diff

.. _JSONTree.fetch_diff: _modules/jsondata/JSONTree.html#JSONTree.fetch_diff
.. _fetchDiff: jsondata_m_tree.html#jsondata.JSONTree.JSONTree.fetch_diff


Runtime Test data
=================

basic
-----
* jsondata.data.json `[json] <_static/data.json>`_
* jsondata.schema.jsd `[schema] <_static/schema.jsd>`_

datacheck
---------
* jsondata.datacheck.json `[json] <_static/datacheck.json>`_
* jsondata.datacheck.jsd `[schema] <_static/datacheck.jsd>`_

rfc6902
-------
* jsondata.rfc6902.jsonp `[json-pointer] <_static/rfc6902.jsonp>`_

selftest
--------
* jsondata.selftest.jsd `[schema] <_static/selftest.jsd>`_
* jsondata.selftest.json `[json] <_static/selftest.json>`_
* jsondata.selftest.jsonp `[json-pointer] <_static/selftest.jsonp>`_

jsondata.Selftest
=================

Hard-coded selftests for the runtime system.

Functions
---------

  +--------------------------------------+----------------------------------------------------+
  | [docs]                               | [source]                                           | 
  +======================================+====================================================+
  | `run_self_test`_                       | `Selftest.run_self_test`_                            |
  +--------------------------------------+----------------------------------------------------+
  | `printverbose`_                      | `Selftest.printverbose`_                           |
  +--------------------------------------+----------------------------------------------------+
  | `load_data`_                         | `Selftest.load_data`_                              |
  +--------------------------------------+----------------------------------------------------+
  | `load_appname`_                      | `Selftest.load_appname`_                           |
  +--------------------------------------+----------------------------------------------------+
  | `verify_data_schema`_                | `Selftest.verify_data_schema`_                     |
  +--------------------------------------+----------------------------------------------------+
  | `verify_appname_schema`_             | `Selftest.verify_appname_schema`_                  |
  +--------------------------------------+----------------------------------------------------+
  | `jsonpointer_data_schema`_           | `Selftest.jsonpointer_data_schema`_                |
  +--------------------------------------+----------------------------------------------------+
  | `jsonpointer_selftest_data`_         | `Selftest.jsonpointer_selftest_data`_              |
  +--------------------------------------+----------------------------------------------------+
  | `jsonpointer_selftest_data_schema`_  | `Selftest.jsonpointer_selftest_data_schema`_       |
  +--------------------------------------+----------------------------------------------------+

.. _Selftest.run_self_test: _modules/jsondata/Selftest.html#run_self_test
.. _runselftest: jsondata_m_selftest.html#jsondata.Selftest.run_self_test

.. _Selftest.printverbose: _modules/jsondata/Selftest.html#printverbose
.. _printverbose: jsondata_m_selftest.html#jsondata.Selftest.printverbose

.. _Selftest.load_data: _modules/jsondata/Selftest.html#load_data
.. _load_data: jsondata_m_selftest.html#jsondata.Selftest.load_data

.. _Selftest.load_appname: _modules/jsondata/Selftest.html#load_appname
.. _load_appname: jsondata_m_selftest.html#jsondata.Selftest.load_appname

.. _Selftest.verify_data_schema: _modules/jsondata/Selftest.html#verify_data_schema
.. _verify_data_schema: jsondata_m_selftest.html#jsondata.Selftest.verify_data_schema

.. _Selftest.verify_appname_schema: _modules/jsondata/Selftest.html#verify_appname_schema
.. _verify_appname_schema: jsondata_m_selftest.html#jsondata.Selftest.verify_appname_schema

.. _Selftest.jsonpointer_data_schema: _modules/jsondata/Selftest.html#jsonpointer_data_schema
.. _jsonpointer_data_schema: jsondata_m_selftest.html#jsondata.Selftest.jsonpointer_data_schema

.. _Selftest.jsonpointer_selftest_data: _modules/jsondata/Selftest.html#jsonpointer_selftest_data
.. _jsonpointer_selftest_data: jsondata_m_selftest.html#jsondata.Selftest.jsonpointer_selftest_data

.. _Selftest.jsonpointer_selftest_data_schema: _modules/jsondata/Selftest.html#jsonpointer_selftest_data_schema
.. _jsonpointer_selftest_data_schema: jsondata_m_selftest.html#jsondata.Selftest.jsonpointer_selftest_data_schema

