# -*- coding:utf-8   -*-
"""Core features for the processing of structured JSON based in-memory data.
This comprises the load of a master model from a JSON file, and the 
incremental addition and removal of branches by loading additional
JSON modules into the master model.
The resulting data could be saved for later reuse, where complex configuration
is varied by user interaction.
The implementation is based on the standard packages 'json' and 'jsonschema'.

This module uses for the syntax of JSON data either a preloaded
module, or loads the standard module by default. Current supported
packages are:
    
- **json**: The standard json package of the Python distribution.

- **ujson**: 'Ultra-JSON', a wrapped C implementation with 
    high-performance conversion. 

The current default module is 'json' for syntax processing, 
the standard package 'jsonschema' for the optional validation.
    
"""
import copy
import logging
import os
from enum import Enum, IntEnum, unique, auto

from jsondata.exceptions import JSONDataAmbiguity

try:
    import ujson as myjson
except ImportError:
    import json as myjson

import jsonschema

from .exceptions import (
    JSONDataParameter, JSONDataException, JSONDataValue, JSONDataKeyError,
    JSONDataSourceFile, JSONDataTargetFile, JSONDataNodeType
)

logger = logging.getLogger(__name__)


class JSONMode(Enum):
    RFC4927 = 0
    RFC7951 = 2
    ECMA264 = 10


class PointerMode(Enum):
    RFC6901 = 20


class PatchMode(Enum):
    RFC6902 = 30


class SchemaMode(Enum):
    OFF = 40
    DRAFT3 = 43
    DRAFT4 = 44
    ON = 44


@unique
class Match(IntEnum):
    INSERT = 0
    NO = auto()
    KEY = auto()
    CHLDATTR = auto()
    INDEX = auto()
    MEM = auto()
    NEW = auto()
    PRESENT = auto()


class JSONpl(list):
    """A wrapper for a 'list' representing a path pointer
    at the method interfaces. Required due to possible 
    ambiguity with the other type of in-memory node.  
    """
    pass


class JSONData:
    """ Representation of a JSON based object data tree.
    
    This class provides for the handling of the in-memory data
    by the main hooks 'data', and 'schema'. This includes generic 
    methods for the advanced management of arbitrary 'branches'
    in extension to RCF6902, and additional methods strictly 
    compliant to RFC6902.

    Due to the pure in-memory support and addressing by the enclosed 
    module JSONPointer for RFC6901 compliant addressing by in memory
    caching, the JSONData may outperform designs based on 
    operation on the native JSON representation.

    Attributes:
        **data**: The data tree of JSON based objects provided
            by the module 'json'.
        **schema**: The validator for 'data' provided by 
            the module 'jsonschema'.

    Common call parameters provided by the methods of this class are:
        *targetnode := addressreference*
            The target node of called method. The 'targetnode' in general 
            represents the target of the called method. In most cases this
            has to be a reference to a container for the modification 
            and/or insertion of resulting elements. The methods require
            the change of contained items, which involves the application
            of a 'key' pointing to the hook in point of the reference
            to the modification.
            
        *key := key-value* 
            The hook-in point for references of modified entries within
            the targetnode container. The following values are supported:
                       
        *sourcenode := addressreference*
            The in-memory node address of the source branch for the method,
            e.g. 'copy' or 'move' operation.

    The address references supported in this class refer the resulting
    in-memory representation of a pointer path. The target is a node 
    within a Python data representation as provided by the package 
    '**json**' and compatible packages, e.g. '**ujson**'. The supported input
    syntax is one of the following interchangeable formats::
        
        # The reference to a in-memory-node.
        addressreference := (
              nodereference
            | addressreference-source
        )

        nodereference:= (
              <in-memory>
            | ''
        )
        
        <in-memory> := "Memory representation of a JSON node, a 'dict'
            or a 'list'. The in-memory Python node reference has to be
            located within the document, due to performance reasons this
            is not verified by default.
            
            The 'nodereference' could be converted from the
            'addressreference-source' representation."

        '' := "Represents the whole document in accordance to RFC6901.
            Same as 'self.data'." 
        
        # The source of the syntax for the description of the reference
        # pointer path to a node. This is applicable on paths to be created.
        addressreference-source := (
            JSONPointer
        )
              
        JSONPointer:="A JSONPointer object in accordance to RFC6901.
            for additional information on input formats refer to the 
            class documentation.
            This class provides a fully qualified path pointer, which
            could be converted into any of the required representations."

    For hooks by 'key-value' within addressed containers::

        key-value:=(None|<list-index>|<dict-key>) 
            
        None := "When the 'key' parameter is 'None', the action 
            optionally could be based on the keys of the 'sourcenode'.  
            The contents of the branch replace the node contents
            when the type of the branch matches the hook."

        <list-index>:=('-'|int)
        
        <dict-key>:="Valid for a 'dict' only, sets key/value pair, 
            where present is replace, new is created."

        '-' := "Valid for a 'list' only, appends to present."
        
        int := "Valid for a 'list' only, replaces present when
            0 < #int < len(Node)."
       
    In the parameter lists of methods used term 'pointer' is either 
    an object of class 'JSONPointer', or a list of pointer path 
    entries.
    
    The JSON types 'object' and 'array' behave in Python slightly 
    different in accordance to RFC6902. The main difference arise 
    from the restrictions on applicable key values. Whereas the
    ranges are limited logically by the actual container sizes, 
    the object types provide free and unlimited keys. The limit 
    is set by type restriction to unicode and 'non-nil' only 
    for keys.  

    """

    def __init__(self, data, *, schema=None, indent_str=4, load_cached=False,
                 requires=None, validator=SchemaMode.OFF, **kwargs):
        """
        Loads and validates a JSON definition with the corresponding
        schema file.

        Args:
                data: JSON data within memory.

        Kwargs:
                schema: A valid in-memory JSON schema.

                    default:= None
                indent_str: Defied the indentation of 'str'.

                    default:= 4
                validator: [default, draft3, draft4, on, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None
                    
                    default:= off

        Returns:
            Results in an initialized object.

        Raises:
            NameError:

            JSONDataValue:

            jsonschema.ValidationError:

            jsonschema.SchemaError:

        """
        # static final defaults

        # JSON-Syntax modes
        self.mode_json = JSONMode.RFC7951
        self.mode_schema = SchemaMode.DRAFT4
        self.mode_pointer = PointerMode.RFC6901
        self.mode_patch = PatchMode.RFC6902

        self.branch = None
        self.data = data
        self.indent = 4
        self.sort_keys = False
        self.validator = validator

        # The internal object schema for the framework -
        # a fixed set of files as final SchemaMode.DRAFT4
        self.schema = schema
        self.indent_str = indent_str
        self.load_cached = load_cached
        self.requires = requires

        logger.debug("JSON=%s / %s", myjson.__name__, myjson.__version__)
        logger.debug("self.data=#[%s]#", self.data)
        logger.debug("self.schema=#[%s]#", self.schema)

        # Check data.
        if self.data is None:
            raise JSONDataParameter("value", "data", str(self.data))

        # Validate.
        if not self.schema and self.validator is not SchemaMode.OFF:
            raise JSONDataParameter("value", "schema", str(self.schema))

        # INPUT-BRANCH: validate data
        if self.validator is not SchemaMode.OFF:
            self.validate(self.data, self.schema, self.validator)

    def __add__(self, x):
        """
        Adds the structure 'x' to 'self', performs deep-operation.
        """
        return self

    def __and__(self):
        """
        Gets the intersection of 'x' and 'self', performs deep-operation.
        """
        return self

    def __call__(self, x):
        """
        Evaluates the pointed value from the document.

        Args:
            x: A valid JSONPointer.

        Returns:
            The pointed value, or None.

        Raises:
            JSONPointerException
        """
        if isinstance(x, JSONPointer):
            return x.get_node_or_value(self.data)
        return JSONPointer(x).get_node_or_value(self.data)

    def __eq__(self, x):
        """
        Compares this JSONData.data with x.

        Args:
            x: A valid JSONData.

        Returns:
            True or False

        Raises:
            JSONDataException
        """
        if not self.data and not x:  # all None is equal,
            return True
        return JSONData.get_tree_diff(self.data, x)

    def __iadd__(self, x):
        """
        Adds the structure 'x' to 'self', performs deep-operation.
        """
        return self

    def __iand__(self):
        """
        Gets the intersection of 'x' and 'self', performs deep-operation.
        """
        return self

    def __imod__(self, x):
        """
        Returns the difference-modulo-set.
        """
        return self

    def __imul__(self, x):
        """
        Duplicates the elements of 'self' 'x' times.
        """
        return self

    def __mul__(self, x):
        """
        Duplicates the elements of 'self' 'x' times.
        
        The operations::

           z = S * x

        Returns the remaining subset of: 

           z = S - 1 * x

        where '1*x' is for each present element of 'x'. When multiple exist
        'n-1' remain.
        """
        return self

    def __ior__(self, x):
        """
        Returns the superset of branches and attributes.
        """
        return self

    def __isub__(self, x):
        """
        Returns the residue of X after each present element of 'x' is removed.
        """
        return self

    def __ixor__(self, x):
        """
        Returns the elements present in one only.
        """
        return self

    def __mod__(self, x):
        """
        Returns the difference-modulo-set.
        
        The operations::

           z = S % x

        Returns the remaining subset of: 

           z = S - n * x

        where 'n*x' is the maximum number of present branches 'x'. When
        multiple exist, all matching are removed.
        """
        return self

    def __radd__(self, x):
        """
        Adds the structure 'x' to 'self', performs deep-operation.
        """
        return self

    def __rand__(self):
        """
        Gets the intersection of 'x' and 'self', performs deep-operation.
        """
        return self

    def __rmod__(self, x):
        """
        Returns the difference-modulo-set.
        """
        return self

    def __rmul__(self, x):
        """
        Duplicates the elements of 'self' 'x' times.
        """
        return self

    def __or__(self, x):
        """
        Returns the superset of branches and attributes.
        """
        return self

    def __ror__(self, x):
        """
        Returns the superset of branches and attributes.
        """
        return self

    def __rsub__(self, x):
        """
        Returns the residue of X after each present element of 'x' is removed.
        """
        return self

    def __rxor__(self, x):
        """
        Returns the elements present in one only.
        """
        return self

    def __sub__(self, x):
        """
        Returns the residue of X after each present element of 'x' is removed.
        
        The operations::

           z = S - x

        Returns the remaining subset of: 

           z = S - 1 * x

        where '1*x' is for each present element of 'x'. When multiple exist
        'n-1' remain.
        """
        return self

    def __xor__(self):
        """
        Returns the structure elements present in in one only.
        """
        return self

    def __repr__(self):
        """
        Dump data.
        """
        return repr(self.data)

    def __str__(self):
        """
        Dumps data by pretty print.
        """
        return myjson.dumps(self.data, indent=self.indent,
                            sort_keys=self.sort_keys)

    def __getitem__(self, key):
        """
        Support of slices, for 'iterator' refer to self.__iter__.
        """
        if not self.data:
            return None
        return self.data[key]

    def __iter__(self):
        """
        Provides an iterator for data.
        """
        return iter(self.data)

    def __ne__(self, x):
        """
        Compares this JSONData with x.

        Args:
            x: A valid JSONData.

        Returns:
            True or False

        Raises:
            JSONDataException
        """
        return not self.__eq__(x)

    def branch_add(self, target_node, key, source_node):
        """
        Add a complete branch into a target structure of type object.

        Present previous branches are replaced, non-existent branches are 
        added. The added branch is created by a deep copy, thus is completely 
        independent from the source. 

           Call: *branch_add* ( **t**, **k**, **s** )

           +---+------------------+---------+----------------+-----------+
           | i |  target          | source  | add            |           |
           |   +----------+-------+---------+-------+--------+           |
           |   |  t       | k     | s       | from  | to     | type      |
           +===+==========+=======+=========+=======+========+===========+
           | 0 |  node    | key   | node    | s     | t[k]   | any       |
           +---+----------+-------+---------+-------+--------+-----------+
           | 1 |  node    | None  | node    | s     | t[*]   | match     |
           +---+----------+-------+---------+-------+--------+-----------+

            0. Use-Case-0: Any source node type is added as 't[k]'.
            
            1. Use-Case-1: The content keys of node 's' are added each
                to the node 't'. Therefore the node types of 's' and 't'
                have to match.
                
                This behaviour is defined in respect to the parameter 
                passing of Python.
                 
        Args:
            target_node := nodereference
                Target container node where the branch is to be inserted.
            
            key := key-value
                Hook for the insertion within target node.
            
            source_node := nodereference
                Source branch to be inserted into the target tree.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataNodeType:
            JSONDataKeyError:

        """
        if isinstance(target_node, JSONPointer):
            try:
                if not key:
                    target_node, key = target_node.get_node_and_child(self.data)
                else:
                    target_node = target_node.get_node(self.data, False)
            except:
                # requires some more of a new path than for the node-only
                self.branch_create('', target_node)
                if not key:
                    target_node, key = target_node.get_node_and_child(self.data)
                else:
                    target_node = target_node.get_node(self.data, True)

        if isinstance(target_node, dict):
            if key:
                target_node[key] = copy.deepcopy(source_node)
            else:
                if not isinstance(source_node, dict):
                    raise JSONDataNodeType(
                        "type", "target_node/source_node",
                        '{}/{}'.format(type(target_node), type(source_node))
                    )
                target_node.clear()
                for k, v in list(source_node.items()):
                    target_node[k] = copy.deepcopy(v)
            return True
        elif isinstance(target_node, list):
            if key == '-':
                target_node.append(copy.deepcopy(source_node))
            elif 0 <= key < len(target_node):
                target_node[key] = copy.deepcopy(source_node)
            elif key is None:  # 0 is valid
                if not isinstance(source_node, list):
                    raise JSONDataNodeType("node/keys != type:does not match:",
                                           target_node, source_node)
                for k in range(0, len(target_node)):
                    target_node.pop()
                for v in source_node:
                    target_node.append(copy.deepcopy(v))
            else:
                raise JSONDataKeyError("mismatch:node:type", 'key', key,
                                       'key-type', type(key), 'node-type',
                                       type(target_node))
            return True

        else:
            raise JSONDataNodeType("type", "target_node/source_node",
                                   str(type(target_node)) + "/" + str(
                                       type(source_node)))

    def branch_copy(self, target_node, key, source_node, force=True):
        """
        Copies the source branch to the target node.

        The copy is internally mapped onto the 'branch_add' call, 
        thus shares basically the same parameters and behaviour.
        Due to the required modification of the target only, the
        copy is slightly different from the 'branch_move' call.
        
           Call: *branch_copy* ( **t**, **k**, **s** )

           +---+------------------+---------+----------------+-----------+
           | i |  target          | source  | copy           |           |
           |   +----------+-------+---------+-------+--------+           |
           |   |  t       | k     | s       | from  |  to    | type      |
           +===+==========+=======+=========+=======+========+===========+
           | 0 |  node    | key   | node    | s     | t[k]   | any       |
           +---+----------+-------+---------+-------+--------+-----------+
           | 1 |  node    | None  | node    | s     | t[sk]  | match     |
           +---+----------+-------+---------+-------+--------+-----------+

            For the description of the Use-Cases refer to branch_add.

        Args:
            target_node := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
            
            source_node := nodereference
                Source branch to be inserted into target tree.
            
            force: If true present are replaced, else only non-present 
                are copied.
                
                default:=True

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:
        
        """
        if force:
            # force replace of existing
            return self.branch_add(target_node, key, source_node)
        elif self.is_applicable(target_node, key, source_node, [Match.NEW]):
            # only new
            return self.branch_add(target_node, key, source_node)
        else:
            # not applicable
            return False

    def branch_create(self, target_node, branch, value=None):
        """Creates a branch located at target node.

        The requested branch as created as child value of provided 
        'target_node'. 'target_node' is required to exist.
         
        **REMARK**: Current version relies for the created nodes on the
            content type of the key(str,unicode)/index(int), later 
            versions may use a provided schema.
  
           Call: *branch_create* ( **t**, **b**, **v** )

           +---+----------+---------+-------+
           | i |  target  | branch  | value |
           |   +----------+---------+-------+
           |   |  t       | b       | v     |
           +===+==========+=========+=======+
           | 0 |  node    | list    | [any] |
           +---+----------+---------+-------+
           | 1 |  node    | list    | [any] |
           +---+----------+---------+-------+
           | 2 |  node    | pointer | [any] |
           +---+----------+---------+-------+
           | 3 |  node    | pointer | [any] |
           +---+----------+---------+-------+


        Args:
            target_node := nodereference
                Base node for the insertion of branch.

            branch :=  addressreference-source
                New branch to be created in the target tree.
                A Pointer address path relative to the 'targetnode'. 

            value: Optional value for the leaf. The value itselfn
                could be either an atomic type, or a branch itself
                in accordance to RFC6902. 

        Returns:
            When successful returns the leaf node, else returns either 
            'None', or raises an exception.

        Raises:
            JSONData:

        """
        ret = None

        def get_new_node(key_type):
            """Fetch the required new container."""
            if key_type == '-':
                return []
            elif isinstance(key_type, int):
                return []
            elif isinstance(key_type, str):
                return {}
            elif not key_type:
                return None
            else:
                raise JSONDataKeyError("type", 'key_type', str(key_type))

        if isinstance(branch, JSONPointer):
            # FIXME: iterator
            branch = branch.get_path_list()

        if not isinstance(branch, list):
            raise JSONDataException("value", "branch", branch)

        if target_node == '':  # RFC6901 - whole document
            target_node = self.data

        if isinstance(target_node, dict):
            # Be aware, the special '-' could be a valid key,
            # thus cannot be prohibited!!!
            if not isinstance(branch[0], str):
                raise JSONDataException(
                    "value", "container/branch",
                    '{}/{}'.format(type(target_node), type(branch[0]))
                )

            if len(branch) > 1:
                if not target_node.get(str(branch[0]), False):
                    target_node[str(branch[0])] = get_new_node(branch[1])
                ret = self.branch_create(
                    target_node[branch[0]], branch[1:], value
                )
            else:
                if target_node.get(branch[0], False):
                    raise JSONDataException("exists", "branch", str(branch[0]))
                ret = target_node[str(branch[0])] = self.get_canonical(value)

        elif isinstance(target_node, list):
            if isinstance(branch[0], int) and branch[0] < len(target_node):
                # see RFC6902 for '-'/append
                raise JSONDataException("exists", "branch", str(branch[0]))
            elif str(branch[0]) == '-':  # see RFC6902 for '-'/append
                pass
            else:
                raise JSONDataException("value", "target_node/branch:" + str(
                    type(target_node)) + "/" + str(type(branch[0])))

            if len(branch) == 1:
                if branch[0] == '-':
                    branch[0] = len(target_node)
                    target_node.append(self.get_canonical(value))
                else:
                    target_node[branch[0]] = self.get_canonical(value)
                ret = target_node
            else:
                if branch[0] == '-':
                    branch[0] = len(target_node)
                    target_node.append(get_new_node(branch[1]))
                ret = self.branch_create(
                    target_node[branch[0]], branch[1:], value
                )

        else:
            raise JSONDataException("type", "target_node",
                                    str(type(target_node)))

        return ret

    def branch_move(self, target_node, key, source_node, source_key, force=True,
                    force_extend=False):
        """Moves a source branch to target node.

        Moves by default only when target is not yet present. The
        parameters for 'list', 'force' enabled to overwrite, whereas 
        the parameter 'forcext' enables to move all entries and 
        extend the target items.
        
        Due to the Python specific passing of flat parameters as
        a copy of the reference without access to the actual source
        entry, these are slightly different from the 'branch_copy'
        and 'branch_add' methods modifying the target only. Therefore 
        additional source keys 'source_key' are required by 'move' in order
        to enable the modification of the source entry. 

           Call: *branch_move* ( **t**, **k**, **s**, **sk** )

           +---+------------------+-----------------+---------------+-------+
           | i |  target          | source          | move          |       |
           |   +----------+-------+---------+-------+-------+-------+       |
           |   |  t       | k     | s       | sk    | from  |  to   | type  |
           +===+==========+=======+=========+=======+=======+=======+=======+
           | 0 |  node    | key   | node    | key   | s[sk] | t[k]  | any   |
           +---+----------+-------+---------+-------+-------+-------+-------+
           | 1 |  node    | None  | node    | key   | s[sk] | t[sk] | match |
           +---+----------+-------+---------+-------+-------+-------+-------+

           0. Use-Case-0: Moves any.
        
           1. Use-Case-1: Moves matching key types only: list-to-list, 
               or dict-to-dict.
        
        Args:
            target_node := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
            
            source_node := nodereference
                Source branch to be inserted into target tree.
            
            source_key := key-value
                Key of the source to be moved to target node.

            force: If true present are replaced, else only 
                non-present are moved.
                
                default:=True

            force_extend: If true target size will be extended when
                required. This is applicable on 'list' only, and
                extends RFC6902. The same effect is given for 
                a 'list' by one of:
                 
                * key:='-' 

                * key:=None and source_key:='-'

        Returns:
            When successful returns 'True', else returns either 
            'False', or raises an exception.

        Raises:
            JSONData:
            JSONDataKey:
            KeyError:
        
        """
        ret = False

        if isinstance(target_node, dict):
            if source_key is None:  # no source key provided
                if key is None:  # no keys provided at all, use source
                    raise JSONDataKeyError("missing", "key", str(key))
                else:  # use target key for both
                    target_node[key] = source_node[key]

            else:
                if key is None:
                    if target_node.get(source_key):
                        if not force:
                            raise JSONDataKeyError("present", "source_key",
                                                   str(source_key))
                    target_node[source_key] = source_node[source_key]
                else:
                    if target_node.get(key):
                        if not force:
                            raise JSONDataKeyError("present", "key", str(key))
                    target_node[key] = source_node[source_key]

            source_node.pop(source_key)
            ret = True
        elif isinstance(target_node, list):
            if source_key is None:  # no source key provided
                if key is None:  # no keys provided at all, use source
                    raise JSONDataKeyError("missing", "key", str(key))
                elif key == '-':  # append all, due to missing 'source_key'
                    if isinstance(source_node, list):  # list to list
                        for v in reversed(source_node):
                            target_node.append(v)
                            source_node.pop()
                    else:  # is dict, requires 'source_key'
                        raise JSONDataKeyError("type/dict", "key", str(key))
                elif key < len(source_node):  # use target key for both
                    target_node[key] = source_node[key]
                    source_node.pop(key)
                else:
                    raise JSONDataKeyError("key", str(key))

            elif source_key == '-':
                raise JSONDataKeyError("type", "source_key", str(source_key))

            else:
                if key is None:
                    if source_key < len(target_node):
                        if force:
                            target_node[source_key] = source_node[source_key]
                        else:
                            raise JSONDataKeyError("present", "source_key",
                                                   str(source_key))
                    elif force_extend:
                        target_node.append(source_node[source_key])
                    else:
                        raise JSONDataKeyError("value", "source_key",
                                               str(source_key))
                else:
                    if isinstance(key, int) and isinstance(source_key, int) \
                            and source_key < len(source_node):
                        if key < len(target_node):
                            if force:
                                target_node[key] = source_node[source_key]
                            else:
                                raise JSONDataKeyError("present", "key",
                                                       str(key))
                        elif force_extend:
                            target_node.append(source_node[source_key])

                    elif key == '-':
                        target_node.append(source_node[source_key])
                    else:  # force_extend is not applicable on explicit given keys
                        raise JSONDataKeyError("value", "source_key", str(source_key))
                source_node.pop(source_key)

            ret = True

        if not ret:
            raise JSONDataException("type", "target_node", str(type(target_node)))

        return ret

    def branch_remove(self, target_node, key):
        """Removes a branch from a target structure.

        The corresponding elements of the 'targetnode' tree are removed.
        The remaining are kept untouched. For tree nodes as leafs the whole
        corresponding subtree is deleted.

        REMARK: No reference checks are done, so the user is responsible
            for additional references.

           Call: *branch_remove* ( **t**, **k** )

           +---+------------------+--------+-------+
           | i |  target          | remove |       |
           |   +----------+-------+--------+       |
           |   |  t       | k     | branch | type  |
           +===+==========+=======+========+=======+
           | 0 |  node    | key   | t[k]   | any   |
           +---+----------+-------+--------+-------+
           | 1 |  node    | None  | t[*]   | any   |
           +---+----------+-------+--------+-------+

           0. Use-Case-0: Removes any type of node.
        
           1. Use-Case-1: Removes all contained items of any type.
        
        Args:
            target_node := nodereference
                Container of 'targetnode' with items to be removed.

            key := key-value
                The item to be removed from the 'targetnode'.
                When 'None', all contained items are removed.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataException:

        """
        try:
            if key:
                target_node.pop(key)
            else:
                target_node.clear()
            return True
        except (AttributeError, KeyError, IndexError):
            raise JSONDataException("type", "target_node", str(target_node))

    def branch_replace(self, target_node, key, source_node):
        """Replaces the value of the target node by the copy of the source branch.

        Requires in order to RFC6902, all items to be replaced has to be
        present. Thus fails if at least one is missing.
        
        Internally the 'branch_add()' call is used with a deep copy.
        When a swallow copy is required the 'branch_move()' has to be used. 

        Args:
            target_node := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
                If key==None, the whole set of keys is replaced by
                the content of the 'source_node'.
            
            source_node := nodereference
                Source branch to be inserted into target tree.
            
            force: If true present are replaced, else only non-present 
                are copied.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:
        
        """
        if not self.is_applicable(target_node, key, source_node,
                                  [Match.PRESENT]):
            return False
        return self.branch_add(target_node, key, source_node)

    @classmethod
    def branch_test(cls, target_node, value):
        """
        Tests match in accordance to RFC6902.

        Args:
            target_node := a valid node
                Node to be compared with the value. Due to
                ambiguity the automated conversion is not 
                reliable, thus it has to be valid. 

            value: Expected value for the given node.
            
        Returns:
            When successful returns 'True', else returns 'False'.

        Raises:
            JSONData:
        """
        if not target_node and not value:  # all None is equal,
            return True
        # value could be a branch itself
        return cls.get_tree_diff(target_node, value)

    def get_data(self):
        """Returns the reference to data."""
        return self.data

    def get_schema(self):
        """Returns the reference to schema."""
        return self.schema

    @classmethod
    def get_tree_diff(cls, n0, n1, diff_list=None, all_diffs=False, dl=0,
                      path=''):
        """
        Recursive tree compare for Python trees as used for the package 'json'.
        
        Finds diff in native Python trees assembled by the
        standard package 'json' and compatible, e.g. 'ujson'.
        """
        # assure JSON strings
        if isinstance(n0, str):
            n0 = str(n0)
        if isinstance(n1, str):
            n1 = str(n1)
        if type(n0) is not type(n1):
            if diff_list is not None:
                diff_list.append({
                    'n0' + path: n0,
                    'n1' + path: n1,
                    'dl': dl
                })
            return False

        if isinstance(n0, list):
            if len(n0) != len(n1):
                if diff_list is not None:
                    diff_list.append({
                        'n0' + path: n0,
                        'n1' + path: n1,
                        'dl': dl
                    })
                return False

            for ni in range(0, len(n0)):
                if isinstance(n0[ni], (list, dict)):
                    if not cls.get_tree_diff(n0[ni], n1[ni], diff_list,
                                             all_diffs, dl + 1,
                                             path + '[' + str(ni) + ']'):
                        if not all_diffs:
                            return False
                elif n0[ni] != n1[ni]:
                    if diff_list is not None:
                        _path = path + '[' + str(ni) + ']'
                        diff_list.append({
                            'n0' + _path: n0[ni],
                            'n1' + _path: n1[ni],
                            'dl': dl
                        })
                    if not all_diffs:
                        return False

        elif isinstance(n0, dict):
            if len(list(n0.keys())) != len(list(n1.keys())):
                if diff_list is not None:
                    diff_list.append({
                        'n0' + path: n0,
                        'n1' + path: n1,
                        'dl': dl
                    })
                return False

            for ni, v in list(n0.items()):
                if n1.get(ni):
                    if type(v) in (list, dict):
                        if not cls.get_tree_diff(v, n1[ni], diff_list,
                                                 all_diffs, dl + 1,
                                                 path + '[' + str(ni) + ']'):
                            if not all_diffs:
                                return False
                    else:
                        if v != n1[ni]:
                            if diff_list is not None:
                                _path = path + '[' + str(ni) + ']'
                                diff_list.append({
                                    'n0' + _path: n0[ni],
                                    'n1' + _path: n1[ni],
                                    'dl': dl
                                })
                            if not all_diffs:
                                return False
                else:
                    if diff_list is not None:
                        _path = path + '[' + str(ni) + ']'
                        diff_list.append({
                            'n0' + _path: n0[ni],
                            'n1' + path: n1,
                            'dl': dl
                        })
                    if not all_diffs:
                        return False

        else:  # invalid types may have been eliminated already
            if n0 == n1:
                return True
            if diff_list is not None:
                diff_list.append({
                    'n0' + path: n0,
                    'n1' + path: n1,
                    'dl': dl
                })
            return False
        if diff_list is not None:
            return len(diff_list) == 0
        return True

    FIRST = 1
    """First match only."""

    ALL = 3
    """All matches."""

    @classmethod
    def get_pointer_path(cls, node, base, restype=FIRST):
        """
        Converts a node address into the corresponding pointer path.
        
        The current implementation is search based, thus may have 
        performance issues when frequently applied.
 
        Args:
            node: Address of Node to be searched for.
            
            base: A tree top nodes to search for node.
            
            restype: Type of search.
                
                first: The first match only. 
                
                all: All matches.
            
        Returns:
            Returns a list of lists, where the contained lists are pointer 
            path-lists for matched elements.
            
            * restype:=FIRST: '[[<first-match>]]',
            
            * restype:=ALL: '[[<first-match>],[<second-match>],...]'

        Raises:
            JSONData:
        """
        if not node or not base:
            return []

        spath = []
        res = []

        if isinstance(base, list):  # first layer - list of elements
            kl = 0
            if node is base:  # top node
                res.append([kl])
            else:
                for sx in base:
                    if node is sx:
                        s = spath[:]
                        s.append(kl)
                        res.append(s)
                    elif isinstance(sx, (dict, list)):
                        sublst = cls.get_pointer_path(node, sx, restype)
                        if sublst:
                            for slx in sublst:
                                s = spath[:]
                                s.append(kl)
                                s.extend(slx)
                                res.append(s)
                    kl += 1

        elif isinstance(base, dict):  # first layer - dict of elements
            if node is base:  # top node
                res.append([''])
            else:
                for k, v in list(base.items()):
                    if node is v:
                        spath.append(k)
                        res.append(spath)
                        continue
                    elif isinstance(v, (list, dict)):
                        sublst = cls.get_pointer_path(node, v, restype)
                        if sublst:
                            for slx in sublst:
                                if slx:
                                    s = spath[:]
                                    s.append(k)
                                    s.extend(slx)
                                    res.append(s)

        # FIXME: for performance
        if res and restype == JSONData.FIRST:
            return [res[0]]
        return res

    def get_canonical(self, value):
        """Fetches the canonical value.
        
        The actual value could be either an atomic value, a node 
        representing a branch, or a reference to an atomic value.
         
        Args:
            value: Value pointer to be evaluated to the actual value.
                Valid input types are:
                    int,str,unicode: Integer, kept as an atomic integer 
                        value.
                    dict,list: Assumed to be a valid node for 'json' 
                        package, used by reference.

                    JSONPointer: A JSON pointer in accordance to 
                        RFC6901.

        Returns:
            When successful returns the value, else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:

        """
        if isinstance(value, (dict, list)):
            # assumes a 'json' package type node
            return value
        elif isinstance(value, (int, float)):
            # assume a 'JSON' RFC7159 int, float
            return value
        elif isinstance(value, str):
            # assume a 'JSON' RFC7159 string
            return str(value)
        elif isinstance(value, JSONPointer):
            # assume the pointed value
            return value.get_node_or_value(self.data)
        elif not value:
            return None
        else:
            raise JSONDataException("type", "value", str(value))

    def is_applicable(self, target_node, key, branch, match_condition=None,
                      child_attr_list=None):
        """ Checks applicability by validation of provided match criteria.

        The contained data in 'data_file' could be either the initial data
        tree, or a new branch defined by a fresh tree structure. The
        'targetnode' defines the parent container where the new branch has
        to be hooked-in.

        Args:
            target_node:
                Target container hook for the inclusion of the loaded branch.
                The branch is treated as a child-branch, hooked into the
                provided container 'target_node'.
            branch:
                Branch to be imported into the target container. The branch
                is treated as a child-branch.
            match_condition:
                Defines the criteria for comparison of present child nodes
                in the target container. The value is a list of critarias
                combined by logical AND. The criteria may vary due to
                the requirement and the type of applied container:
                - common: Common provided criteria are:
                    - insert: Just checks whether the branch could be inserted.
                        In case of 'list' by 'append', in case of a 'dict' by
                        the insert-[]-operator.
                        This is in particular foreseen for the initial creation
                        of new nodes.
                    - present: Checks whether all are present.
                    - no: Inverts the match criteria for the whole current set.
                - dict: The provided criteria are:
                    - key: Both share the same key(s).
                    - child_attr_list: A list of child attributes to be matched.
                        This may assure e.g. compatibility by a user defined ID,
                        and or a UUID.
                    
                    default:=['key',]
                - list: The provided criteria are:
                    - index: The positions of source and target have to match.
                    - child_attr_list: A list of child attributes to be matched,
                        thus e.g. the 'key' of dictionaries could be emulated
                        by an arbitrary attribute like 'mykey'.
                        This may assure e.g. compatibility by a user defined ID,
                        and or a UUID.
                    - mem: Checks whether the in-memory element is already present.
                        Even though this is a quite weak criteria, it is probably
                        the only and one common generic criteria for lists.
                    
                    default:= mem # ATTENTION: almost any call adds a branch!
            child_attr_list: A list of user defined child attributes which
                all together(AND) define the match criteria.

                default:=None, returns 'True'
        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

            The rule of thumb is:
                - type-mismatch: Exception
                - value-mismatch: return False

            Success is: no-defined-condition or no-failing-condition

        Raises:
            JSONData:

            JSONDataValue:

        """
        if match_condition is None:
            match_condition = (Match.INSERT,)

        if not match_condition:
            return True

        if isinstance(target_node, JSONData):
            target_node = target_node.data
        if isinstance(branch, JSONData):
            branch = branch.data

        # The first mandatory requirement definition if the type compatibility
        # of the plug and the plugin-element.
        if key is None and type(target_node) is not type(branch):
            raise JSONDataException("type", "target_node",
                                    str(type(target_node)))

        if Match.NO in match_condition:
            failed = True
            ok = False
        else:
            failed = False
            ok = True

        for m in match_condition:
            if m is Match.NO:
                # handles multiple, does not need alist.branch_remove()
                continue
            elif m is Match.INSERT:
                if not isinstance(target_node, (dict, list)):
                    raise JSONDataException("type", "target_node",
                                            str(type(target_node)))
            elif m is Match.KEY:
                if not isinstance(target_node, dict):
                    raise JSONDataException("type", "target_node",
                                            str(type(target_node)))
                for k in list(branch.keys()):
                    if not target_node.get(k):
                        return failed
            elif m is Match.CHLDATTR:
                if not isinstance(target_node, (list, dict)):
                    raise JSONDataException("type", "target_node",
                                            str(type(target_node)))
                if child_attr_list is not None:
                    if isinstance(branch, dict):
                        for ca in child_attr_list:
                            if not target_node.get(ca):
                                return failed
                    elif isinstance(branch, list):
                        for l in target_node:
                            if not isinstance(l, dict):
                                raise JSONDataException("type", "target_node",
                                                        str(type(target_node)))
                            for ca in child_attr_list:
                                if not isinstance(ca, dict):
                                    raise JSONDataException(
                                        "type", "target_node",
                                        str(type(target_node))
                                    )
                                if not l.get(ca):
                                    return failed
                    else:
                        raise JSONDataException("type", "target_node",
                                                str(type(target_node)))
            elif m is Match.INDEX:
                if isinstance(target_node, list):
                    raise JSONDataException("type", "target_node",
                                            str(type(target_node)))
                if len(target_node) > len(branch):
                    return failed
            elif m is Match.NEW:
                if isinstance(target_node, list):
                    if key == '-':
                        pass
                    elif key is not None:
                        if 0 <= key < len(target_node):
                            if target_node[key]:
                                return failed
                        if len(target_node) > len(branch):
                            return failed
                    else:
                        if isinstance(branch, list):
                            if target_node:
                                return failed

                elif isinstance(target_node, dict):
                    if key:
                        if not target_node.get(key, None):
                            return failed
                    else:
                        if isinstance(branch, dict) and target_node:
                            return failed

            elif m is Match.PRESENT:
                if isinstance(target_node, list):
                    if key is not None:
                        if 0 <= key < len(target_node):
                            return ok
                        else:
                            return failed
                    else:
                        return failed

                elif isinstance(target_node, dict):
                    if key:
                        if not target_node.get(key, None):
                            return failed
                        return ok
                    else:
                        return failed

            elif m is Match.MEM:
                if isinstance(target_node, list):
                    if type(target_node) is not type(branch):
                        raise JSONDataException("type", "target_node",
                                                str(type(target_node)))
                    for l in branch:
                        try:
                            if not target_node.index(l):
                                return failed
                        except:
                            return failed
                elif isinstance(target_node, dict):
                    if type(target_node) is type(branch):
                        raise JSONDataException("type", "target_node",
                                                str(type(target_node)))
                    for k, v in list(branch.items()):
                        if id(v) != id(target_node.get(k)):
                            return failed
                else:
                    raise JSONDataException("type", "target_node",
                                            str(type(target_node)))
            elif match_condition:
                raise JSONDataException("type", "target_node",
                                        str(type(target_node)))
        return ok

    def pop(self, key):
        """
        Transparently passes the 'pop()' call to 'self.data'.
        """
        return self.data.pop(key)

    def print_data(self, pretty=True, source=None, source_file=None):
        """Prints structured data.

        Args:
            pretty: Activates pretty printer for treeview, else flat.

            source_file: Loads data from 'source_file' into 'source'.

                default:=None
            source: Prints data within 'source'.

                default:=self.data

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataAmbiguity:

            forwarded from 'json'

        """
        if source_file and source:
            raise JSONDataAmbiguity('source_file/source',
                                    "source_file=" + str(source_file),
                                    "source=" + str(source))
        if source_file:
            source = open(source_file)
            source = myjson.load(source)
        elif not source:
            source = self.data  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def print_schema(self, pretty=True, source=None, source_file=None):
        """Prints structured schema.

        Args:
            pretty: Activates pretty printer for tree view, else flat.

            source: Prints schema within 'source'.

                default:=self.schema

            source_file: Loads schema from 'sourcefile' into 'source'.

                default:=None

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataAmbiguity:

            forwarded from 'json'

        """
        if source_file and source:
            raise JSONDataAmbiguity('source_file/source',
                                    "source_file=" + str(source_file),
                                    "source=" + str(source))
        if source_file:
            source = open(source_file)
            source = myjson.load(source)
        elif not source:
            source = self.schema  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def set_schema(self, schema_file=None, target_node=None, data_file=None,
                   persistent=False, schema=None, validator=None):
        """
        Sets schema or inserts a new branch into the current assigned schema.

        The main schema(target_node==None) is the schema related to the current
        instance. Additional branches could be added by importing the specific
        schema definitions into the main schema. These could either kept
        volatile as a temporary runtime extension, or stored into a new schema
        file in order as extension of the original for later combined reuse.

        Args:
            schema_file:
                JSON-Schema filename for validation of the subtree/branch.
                See also **kwargs['schema'].
            target_node:
                Target container hook for the inclusion of the loaded branch.
            validator: [default, draft3, off, ]
                Sets schema validator for the data file.
                The values are: default=validate, draft3=Draft3Validator,
                off=None.

                default:= None
            schema:
                In-memory JSON-Schema as an alternative to schema_file.
                When provided the 'schema_file' is ignored.

                default:=None
            persistent:
                Stores the 'schema' persistently into 'schema_file' after
                completion of update including addition of branches.
                Requires valid 'schema_file'.

                default:=False

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:

            JSONData:

            JSONDataSourceFile:

            JSONDataValue:

        """
        logger.debug("set_schema:schema_file=%s", schema_file)

        #
        # *** Fetch parameters
        #
        validator = validator or self.validator
        if schema_file is not None:
            # change filename
            self.schema_file = schema_file
        elif self.schema_file is not None:
            # use present
            schema_file = self.schema_file
        elif data_file is not None:
            # derive co-allocated from config
            schema_file = os.path.splitext(data_file)[0] + '.jsd'
            if not os.path.isfile(schema_file):
                schema_file = None
            else:
                self.schema_file = schema_file

        if not schema_file and persistent:
            # persistence requires storage
            raise JSONDataTargetFile("open", "JSONSchemaFilename",
                                     schema_file)

        # schema for validation
        if schema:  # use loaded
            pass

        elif schema_file:  # load from file
            schema_file = os.path.abspath(schema_file)
            self.schema_file = schema_file
            if not os.path.isfile(schema_file):
                raise JSONDataSourceFile("open", "schema_file", str(schema_file))
            with open(schema_file) as schema_file:
                schema = myjson.load(schema_file)
            if schema is None:
                raise JSONDataSourceFile("read", "schema_file", str(schema_file))

        else:  # missing at all
            raise JSONDataSourceFile("open", "schema_file", str(schema_file))
            pass

        #
        # manage new branch data
        #
        if not target_node:
            self.schema = schema

        else:  # data history present, so decide how to handle

            # the container hook has to match for insertion-
            if type(target_node) is not type(schema):
                raise JSONDataException(
                    "type", "target!=branch",
                    '{}!={}'.format(type(target_node), type(schema))
                )

            self.branch_add(target_node, schema)

        return schema is not None

    def validate(self, data, schema, validator=None):
        """Validate data with schema by selected validator.

        Args:
            data:
                JSON-Data.
            schema:
                JSON-Schema for validation.
            validator:
                Validator to be applied, current supported:
                
                schema:
                    In-memory JSON-Schema as an alternative to schema_file.
                    When provided the 'schema_file' is ignored.
                    
                    default:=None
                validator: [default, draft3, draft4, off, on, ]
                    default|MODE_SCHEMA_ON
                        The current default.
                    draft3|MODE_SCHEMA_DRAFT3
                        The first supported JSONSchema IETF-Draft.
                    draft4|MODE_SCHEMA_DRAFT4
                        The current supported JSONSchema IETF-Draft.
                    off|MODE_SCHEMA_OFF:
                        No validation.

                    Sets schema validator for the data file.
                    
                    default:= MODE_SCHEMA_DRAFT4

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            ValidationError:
            SchemaError:
            JSONDataValue:

        """
        if not validator:
            validator = self.mode_schema

        if validator is SchemaMode.DRAFT4:
            logger.debug("Validate: draft4")
            try:
                jsonschema.validate(data, schema)

            # FIXME:

            except jsonschema.ValidationError as e:
                logger.exception('ValidationError')
                raise
            except jsonschema.SchemaError as e:
                logger.exception('SchemaError', e.path, e.schema_path)
                raise

        elif validator is SchemaMode.DRAFT3:
            logger.debug("Validate: draft3")
            jsonschema.Draft3Validator(data, schema)
        elif validator is not SchemaMode.OFF:
            raise JSONDataValue("unknown", "validator", str(validator))


from .pointer import JSONPointer
# avoid nested recursion problems
