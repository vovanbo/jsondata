# -*- coding:utf-8   -*-
"""
Provides classes for the JSONPointer definition in accordance to RFC6901.

The provided class JSONPointer internally stores and applies pointer data
as a list of keys and indexes with the additional cooperative caching of
the pointed in-memory node reference for fast access on data provided by
the packages 'json' and 'jsonschema'. Requests for the string representation
are transformed into a pointer path in accordance to RFC6901. 

The JSONPointer class combines fast in-memory operations and pointer 
arithmetics with standards compliant path strings at the API.

The JSONPointer class by itself is focused on the path pointer itself, though
the provided operations do not touch the content value. The pointer provides
the hook where the value has to be inserted. 
"""
import logging
import re
from collections import UserList, Mapping, Sequence
from typing import List, Any, Union
from urllib.parse import unquote, quote

from decimal import Decimal

import copy

from .helpers import ensure_text_type, is_collection, MISSING, first
from .exceptions import JSONPointerException

__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__maintainer__ = 'Vladimir Bolshakov'
__maintainer_email__ = 'vovanbo@gmail.com'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


def to_int_if_possible(value):
    return int(value) if value.isdigit() else value


def normalize_part(value):
    """
    6901-escaped, generic chars-quote
    """
    if isinstance(value, str):
        return to_int_if_possible(
            unquote(value).replace('~1', '/').replace('~0', '~')
        )
    else:
        return value


def get_comparable_string(value) -> str:
    if isinstance(value, JSONPointer):
        return value.rfc6901
    elif isinstance(value, list):
        return '/{}'.format('/'.join(str(i) for i in value))
    elif isinstance(value, str):
        return value
    elif isinstance(value, int):
        return '/{!s}'.format(value)
    else:
        raise ValueError('Value is not comparable.')


def get_value_for_keys(keys, obj, default, path=None):
    if path is None:
        path = []
    path.append(keys[0])
    if len(keys) == 1:
        return path, get_value_for_key(keys[0], obj, default)
    else:
        inherit = get_value_for_key(keys[0], obj, default)
        return get_value_for_keys(keys[1:], inherit, default, path)


def get_value_for_key(key, obj, default):
    try:
        return obj[key]
    except (KeyError, AttributeError, IndexError, TypeError):
        try:
            if isinstance(key, str):
                attr = getattr(obj, key)
                return attr() if callable(attr) else attr
            else:
                return default
        except AttributeError:
            return default


class JSONPointer(UserList):
    """
    Represents exactly one JSONPointer in compliance with IETF RFC6901.
    This pointer could be processed by extension, reduction,
    and general modification with support of provided methods
    and path arithmetic operators.
    
    The JSONPointer is provided at the API as a utf(-8) string in accordance 
    to RFC6901, including RFC3869.
    
    For enhancement of the processing performance by the underlying packages 
    'json' and 'jsonschema', the pointer is stored and applied in two variants. 
    
    * self.raw: Raw input of the pointer string for the logical API.
    
    * self.path: Split elements of the pointer path within a list of keys,
        for the programming interface.
      
    The attribute 'self.path' contains the path elements in a
    'list'::
       
       ptrlist := (<EMPTY>|plist)
       <EMPTY> := "empty list, represents the whole document"
       plist := pkey [, plist ]
       pkey := (''|int|keyname)
       '' := "the empty string is a valid key too"
       int := "integer index of an array item, just digits"
       keyname := "the valid name of an object/property entry" 

    The JSONPointer::
    
      "/address/0/streetName"
    
    is represented as::
    
      ['address', 0, 'streetName' ]


    The methods and operators are handling the pointer itself, the values
    referenced by the pointer are not modified. 
    
    The methods of this class support for multiple input format of 
    the JSONPointer. The parameter 'other' in the operations is defined as a
    valid JSONPointer fragment. A pointer fragment is a part of a pointer,
    which could be the complete pointer itself - the all-fragment. 
    
    The syntax element could be one of::
        
        'str': A string i accordance to RFC6901. Strings are represented 
            internally as unicode utf-8.
            
            Here either the input parameter 'other' is split into
            a list, or in case of combining operations, the self.path
            attribute is 'joined' to be used for the method. 

        'int': A numeric value in case of an array index. This value 
            is internally handled for the string representation as a
            unicode utf-8, whereas for the addressing of memory 
            objects the numeric integer value is stored and applied.

        'JSONPointer': The attributes of the input object are used 
            with it's peers.
        
        'list': Expects a path list containing:
            - JSON object names
                Names of the json objects.
            - array indexes
                Numeric index for arrays.
            - JSONPointer
                A JSONPointer object, the path is resolved as a section 
                of overall path.

            The self.ptr attribute is applied for operations.
    
    The provided value is internally stored as a raw input value, and a list
    of keys and indexes for access to in-memory data as provided by the
    packages 'json' and 'jsonschema'. Requests for the string representation
    are transformed into a pointer path in accordance to RFC6901. This provides
    for fast access in case of pointer arithmetic, while providing standards
    conform path strings at the interface.
    """
    # Regular expression for valid numerical index
    VALID_INDEX = re.compile('0|[1-9][0-9]*$')

    # Valid types of in-memory JSON node values
    NODE_VALUE_TYPES = (str, Mapping, Sequence, int, float, Decimal, bool,
                        type(None))
    NODE_TYPES = (Mapping, Sequence)
    NUMERIC_TYPES = (int, float, Decimal)

    def __init__(self, pointer):
        """
        Converts and stores a JSONPointer as a list.

        Processes the ABNF of a JSON Pointer from RFC6901.
    
        Args:
            pointer: A JSONPointer to be represented by this object. The
                supported formats are:
                    'str': A string i accordance to RFC6901
                    JSONPointer: A valid object, will be copied 
                        into this, see 'deep'.
                    'list': expects a path list, where each item
                        is processed for escape and unquote.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception. 
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            ValueError:

        """
        if isinstance(pointer, str) and pointer.startswith('#'):
            # Support for creation from URI representation:
            # https://tools.ietf.org/html/rfc6901#section-6
            pointer = pointer.lstrip('#')

        if pointer == '' or pointer == []:
            # shortcut for whole document, see RFC6901
            self._raw = ''
            init_list = []
        else:
            if isinstance(pointer, JSONPointer):
                init_list = pointer.data.copy()
            elif is_collection(pointer):
                init_list = [self.normalize_path_part(p) for p in pointer]
            elif isinstance(pointer, str):
                init_list = pointer.lstrip('/').split('/')
            else:
                raise ValueError("Create JSON pointer is not supported "
                                 "from type: {!s}".format(type(pointer)))

            self._raw = '/{}'.format('/'.join(init_list)) if init_list else ''

        self._node = None

        super(JSONPointer, self).__init__(normalize_part(p) for p in init_list)

    @property
    def path(self):
        return self.data

    @property
    def parent_path(self):
        return self.data[:-1]

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def node(self):
        return self._node

    @property
    def rfc6901(self) -> str:
        """
        JSON String Representation of pointer in compliance to RFC6901.
        https://tools.ietf.org/html/rfc6901#section-5

        Returns:
            The pointer in accordance to RFC6901.
        """
        if not self.path:  # ==[] : special RFC6901, whole document
            return ''
        if len(self.path) == 1 and self.path[0] == '':
            # special RFC6901, '/' empty top-tag
            return '/'
        return '/{}'.format('/'.join(str(i) for i in self.path))

    @property
    def uri(self):
        """
        URI Fragment Identifier Representation in compliance to RFC6901.
        https://tools.ietf.org/html/rfc6901#section-6
        """
        return '#/{}'.format(
            '/'.join(
                (
                    quote(str(part), safe='/~')
                    .replace('~', '~0').replace('/', '~1')
                )
                for part in self.path
            )
        ) if self.path else '#'

    def __str__(self):
        """
        Returns the string for the processed path.
        """
        return self.rfc6901

    def __repr__(self):
        return 'JSONPointer({!r})'.format(self.path)

    def __hash__(self):
        return hash(tuple(self.path))

    def __call__(self, data):
        """
        Evaluates the pointed value from the document.

        Args:
            data: A valid JSON document.

        Returns:
            The pointed value, or None.

        Raises:
            JSONPointerException
        """
        return self.get_node_or_value(data)

    def __add__(self, other) -> 'JSONPointer':
        """
        Appends a Pointer to self.

        Args:
            other: A valid JSONPointer fragment.

        Returns:
            A new object of JSONPointer

        Raises:
            JSONPointerException:

        """
        result = JSONPointer(self.data)
        if not isinstance(other, JSONPointer):
            try:
                pointer = JSONPointer(
                    str(other) if isinstance(other, int) else other
                )
            except ValueError as e:
                raise JSONPointerException('Can not add pointer. '
                                           'Error: {!s}'.format(e))
        else:
            pointer = other

        if not pointer.path:
            raise JSONPointerException('Cannot add the whole document')

        result._raw += pointer.raw
        result.data.extend(pointer.data)

        return result

    def __iadd__(self, other) -> 'JSONPointer':
        """
        Add in place x to self, appends a path.

        Args:
            other: A valid Pointer.

        Returns:
            'self' with updated pointer attributes

        Raises:
            JSONPointerException:
        """
        if not isinstance(other, JSONPointer):
            if other == '' or other == []:
                return self

            try:
                pointer = JSONPointer(
                    str(other) if isinstance(other, int) else other
                )
            except ValueError as e:
                raise JSONPointerException('Can not add pointer. '
                                           'Error: {!s}'.format(e))
        else:
            pointer = other

        if not pointer.path:
            raise JSONPointerException('Cannot add the whole document')

        if pointer.raw.startswith('/'):
            self._raw = pointer.raw
        else:
            self._raw = '{}/{}'.format(self.raw, other.raw)

        self.data.extend(pointer.data)

        return self

    def __radd__(self, other):
        """
        Adds itself as the right-side-argument to the left.

        This method appends 'self' to a path fragment on the left.
        Therefore it adds the path separator on it's left side only.
        The left side path fragment has to maintain to be in
        accordance to RFC6901 by itself.

        Once 'self' is added to the left side, it terminates it's
        life cycle. Thus another simultaneous add operation is
        handled by the resulting other element.

        Args:
            other: A valid Pointer.

        Returns:
            The updated input of type 'x' as 'x+S(x)'

        Raises:
            JSONPointerException:
        """
        if other == '':
            # whole document, RFC6901
            return self.rfc6901
        elif other == '/':
            # empty tag
            return '{}{}'.format(other, self.rfc6901)
        elif isinstance(other, int):
            return '/{!s}{}'.format(other, self.rfc6901)
        elif isinstance(other, str):
            return '{}{}'.format(other, self.rfc6901)
        elif isinstance(other, list):
            return other.extend(self.data)
        else:
            raise JSONPointerException()

    def __eq__(self, other) -> bool:
        """
        Compares pointer with other.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        if other is None:
            return False
        else:
            return self.rfc6901 == get_comparable_string(other)

    def __ge__(self, other) -> bool:
        """
        Checks containment(>=) of another pointer within this.

        The weight of contained entries is the criteria, though
        the shorter is the bigger. This is true only in case of
        a containment relation.

        The number of equal path pointer items is compared.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:

        """
        if other is None:
            return True
        else:
            other_rfc6901 = get_comparable_string(other)

        if self.rfc6901 > other_rfc6901:
            # the shorter is the bigger
            return False

        return other_rfc6901.startswith(self.rfc6901)

    def __gt__(self, other) -> bool:
        """
        Checks containment(>) of another pointer or object within this.

        The number of equal items is compared.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        if other is None:
            return True
        else:
            other_rfc6901 = get_comparable_string(other)

        if self.rfc6901 >= other_rfc6901:
            # the shorter is the bigger, so false in any case
            return False

        return other_rfc6901.startswith(self.rfc6901)

    def __le__(self, other) -> bool:
        """
        Checks containment(<=) of this pointer within another.

        The number of equal items is compared.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        if other is None:
            return False
        else:
            other_rfc6901 = get_comparable_string(other)

        if self.rfc6901 < other_rfc6901:
            # the shorter is the bigger
            return False

        return self.rfc6901.startswith(other_rfc6901)

    def __lt__(self, other) -> bool:
        """
        Checks containment(<) of this pointer within another.

        The number of equal items is compared.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        if other is None:
            return False
        else:
            other_rfc6901 = get_comparable_string(other)

        if self.rfc6901 <= other_rfc6901:  # the shorter is the bigger
            return False

        return self.rfc6901.startswith(other_rfc6901)

    def __ne__(self, other) -> bool:
        """
        Compares this pointer with x.

        Args:
            other: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        return not self.__eq__(other)

    def __contains__(self, other) -> bool:
        """
        Returns True if self contains the other given pointer
        """
        if isinstance(other, JSONPointer):
            return self.contains(other)
        else:
            super(JSONPointer, self).__contains__(other)

    def contains(self, other) -> bool:
        """
        Returns True if self contains the other given pointer
        """
        return self.path[:len(other.path)] == other.path

    @staticmethod
    def resolve_path(path: List[Any], data: Union[Sequence, Mapping],
                     default=MISSING):
        if is_collection(data) or isinstance(data, Mapping):
            if not path:
                # special RFC6901, whole document
                return path, data
            if len(path) == 1 and path[0] == '':
                # special RFC6901, '/' empty top-tag
                return path, (first(data) if is_collection(data) else data[''])

            return get_value_for_keys(path, data, default)
        else:
            raise ValueError('Invalid data type for resolving.')

    @staticmethod
    def normalize_path_part(p) -> str:
        if isinstance(p, JSONPointer):
            return p.rfc6901
        elif isinstance(p, str):
            return p
        elif isinstance(p, int):
            return ensure_text_type(p)
        else:
            raise ValueError("Invalid path part: %s" % p)

    def check_node_or_value(self, json_data, parent=False) -> bool:
        """
        Checks the existence of the corresponding node within the JSON document.

        Args:
            json_data: A valid JSON data node.
            parent: Return the parent node of the pointed value.

        Returns:
            True or False

        Raises:
            JSONPointerException:
            forwarded from json
        """
        path = self.parent_path if parent else self.path
        node_path, node = self.resolve_path(path, json_data)
        if node is MISSING:
            return False

        if not isinstance(node, self.NODE_VALUE_TYPES):
            # concrete info for debugging for type mismatch
            raise JSONPointerException(
                "Invalid path node type: %s" % type(json_data)
            )

        return True

    def get_node(self, json_data, parent=False):
        """
        Gets the corresponding node reference for a JSON container type.
        
        This method gets nodes of container types. Container 
        types of JSON are 'array' a.k.a. in Python 'list', 
        and 'objects' a.k.a. in Python 'dict'.
        
        Due to the special case of RFC6902 'append' by the array 
        index '-' in combination of the add rules a special 
        exception-treatment is required, for details refer to RFC6902.
        
        The 'get_node' method therefore returns only an existing 
        node of a of valid non-ambiguous path pointer. This 
        excludes pointers containing the symbolic index '-' for 
        an array component.
        
        See also related methods:
        
            get_node_and_child: For Python access to a child node 
                within a container by the container itself, and the
                item key.
            get_existing_node: For the application of partial valid
                pointer paths of new branches.
            get_node_or_value: For any type of pointed item, either 
                a node, or a value. 
        
        Args:
            json_data: A valid JSON data node.
            parent: Return the parent node of the pointed value.
                When parent is selected, the pointed child node
                is not verified. 

        Returns:
            The node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        path = self.parent_path if parent else self.path
        node_path, node = self.resolve_path(path, json_data)

        if node is MISSING:
            raise JSONPointerException(
                'Requires existing Node(%s): '
                '%s of %s' % (node_path, node, self.path)
            )

        if not isinstance(node, self.NODE_TYPES):
            # concrete info for debugging for type mismatch
            raise JSONPointerException(
                "Invalid path node type: %s" % type(node)
            )

        return node

    def get_node_and_child(self, json_data):
        """
        Returns a tuple containing the parent node and the child.

        Args:
            json_data: A valid JSON data node.

        Returns:
            The the tuple:
            (n,c):  n: Node reference to parent container.
                    c: Key for the child entry, either an 
                       index 'int', or a key ('str', 'unicode'). 
        Raises:
            JSONPointerException:
            forwarded from json
        """
        return self.get_node(json_data, parent=True), self.path[-1]

    def get_node_or_value(self, json_data, value_type=None, parent=False):
        """
        Gets the corresponding node reference or the JSON value of a leaf.

        Relies on the standard package 'json' by 'Bob Ippolito <bob@redivi.com>'.
        This package supports in the current version the following types:
        
            +---------------+-------------------+
            | JSON          | Python            |
            +===============+===================+
            | object        | dict              |
            +---------------+-------------------+
            | array         | list              |
            +---------------+-------------------+
            | string        | str               |
            +---------------+-------------------+
            | number (int)  | int               |
            +---------------+-------------------+
            | number (real) | float             |
            +---------------+-------------------+
            | true          | True              |
            +---------------+-------------------+
            | false         | False             |
            +---------------+-------------------+
            | null          | None              |
            +---------------+-------------------+

            It also understands ``NaN``, ``Infinity``, and
            ``-Infinity`` as their corresponding ``float`` 
            values, which is outside the JSON spec.


        The supported standard value types for Python 
        of get_node_or_value() are mapped automatically 
        as depicted in the following table. Additional
        bindings may be implemented by sub-classing.
        
            +------------------------+-------------------+
            | JSONPointer(json_data) | Python-valtype    |
            +========================+===================+
            | object (dict)          | dict              |
            +------------------------+-------------------+
            | array  (list)          | list              |
            +------------------------+-------------------+
            | array  (tuple)         | list              |
            +------------------------+-------------------+
            | string                 | str               |
            +------------------------+-------------------+
            | number (int)           | int               |
            +------------------------+-------------------+
            | number (long)          | int               |
            +------------------------+-------------------+
            | number (float)         | float             |
            +------------------------+-------------------+
            | *number (double)       | float             |
            +------------------------+-------------------+
            | number (octal)         | int               |
            +------------------------+-------------------+
            | number (hex)           | int               |
            +------------------------+-------------------+
            | number (binary)        | int               |
            +------------------------+-------------------+
            | number (complex)       | - (custom)        |
            +------------------------+-------------------+
            | true                   | True              |
            +------------------------+-------------------+
            | false                  | False             |
            +------------------------+-------------------+
            | null                   | None              |
            +------------------------+-------------------+

        The mappings in detail are:

        * object(dict) => dict:
            {a:b} - native Python dictionary
        
        * array(list) => list:
            [a,b] - native Python list
        
        * (*)array(tuple) => list:
            (a,b) - native Python list
        
        * string(str) => str:
            "abc" - native Python unicode string UTF-8
        
        * number(int) => int:
            1234, −24, 0 - Integers (unlimited precision)

        * number(long) => int:
            1234, −24, 0 - Integers (unlimited precision)
        
        * number(float) => float:
            1.23, 3.14e-10, 4E210, 4.0e+210, 1., .1 - 
            Floating-point (normally implemented as C doubles in CPython)
        
        * (*)number(double) => float:
            1.23, 3.14e-10, 4E210, 4.0e+210, 1., .1 - 
            Floating-point (normally implemented as C doubles in CPython)
        
        * number(octal) => int:
            0o177 - 
            Octal, hex, and binary literals for integers2
        
        * number(hex) => int:
            0x9ff - Octal, hex, and binary literals for integers2
        
        * number(binary) => int:
            0b1111 - Octal, hex, and binary literals for integers2
        
        * number(complex) => <not-supported>(requires custom):
            3+4j, 3.0+4.0j, 3J - Complex numbers
        
        * true(True) => boolean(True):
            True - native Python boolean
        
        * false(False) => boolean(False):
            False - native Python boolean
        
        * null(None) => None:
            False - native Python NoneType

        Args:
            json_data: A valid JSON data node.
            value_type: Type of requested value.
            parent: Return the parent node of the pointed value.

        Returns:
            The node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        path = self.parent_path if parent else self.path
        node_path, node = self.resolve_path(path, json_data)
        if node is MISSING:
            raise JSONPointerException(
                "Node(%s): %s of %s" % (node_path, node, self.path)
            )

        if value_type:  # requested value type
            # fix type ambiguity for numeric
            if value_type in self.NUMERIC_TYPES and isinstance(node, str):
                try:
                    node = value_type(node)
                except ValueError:
                    pass

            if not isinstance(node, value_type):
                raise JSONPointerException(
                    "Invalid path value type: "
                    "%s != %s" % (value_type, type(node))
                )
        else:  # in general valid value types - RFC4729, RFC7951
            if not isinstance(node, self.NODE_VALUE_TYPES):
                raise JSONPointerException(
                    "Invalid path node type: %s" % type(node)
                )

        return node

    def get_existing_node(self, json_data, parent=False):
        """
        Returns the node for valid part of the pointer, and the remaining part.
        
        This method works similar to the 'get_node' method, whereas it
        handles partial valid path pointers, which may also include 
        a '-' in accordance to RFC6902.
        
        Therefore the non-ambiguous part of the pointer is resolved, 
        and returned with the remaining part for a newly create.
        Thus this method is in particular foreseen to support the 
        creation of new sub data structures.
        
        The 'get_node' method therefore returns a list of two elements,
        the first is the node reference, the second the list of the 
        remaining path pointer components. The latter may be empty in
        case of a fully valid pointer.
        
        
        Args:
            json_data: A valid JSON data node.
            parent: Return the parent node of the pointed value.

        Returns:
            The node reference, and the remaining part.
            ret:=[ node, [<remaining-path-components-list>] ]
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if not self.path:
            return json_data, []

        path = self.parent_path if parent else self.path

        for sub_path in self.path_reducer(path):
            existing_node_path, existing_node = self.resolve_path(sub_path,
                                                                  json_data)
            if existing_node is not MISSING:
                break

        if not isinstance(existing_node, self.NODE_TYPES):
            # concrete info for debugging for type mismatch
            raise JSONPointerException(
                "Invalid path node type: %s" % type(existing_node)
            )

        path_set = frozenset((i, v) for i, v in enumerate(path))
        existing_node_path_set = frozenset(
            (i, v) for i, v in enumerate(existing_node_path)
        )
        remaining_set = sorted(path_set - existing_node_path_set,
                               key=lambda i: i[0])

        return existing_node, [v[1] for v in remaining_set]

    @staticmethod
    def path_producer(path):
        for i in range(0, len(path)):
            yield path[:i + 1]

    @staticmethod
    def path_reducer(path):
        for i in range(0, len(path)):
            if i == 0:
                yield path
            else:
                yield path[:-i]

    def iter_path(self, json_data=None, parent=False, reverse=False):
        """
        Iterator for the elements of the path pointer itself.

        Args:
            json_data: If provided a valid JSON data node, the
                path components are successively verified on
                the provided document. If None the path pointer
                components are just iterated.
            parent: Uses the path pointer to parent node.
            reverse: Reverse the order, start with last.

        Returns:
            Yields the iterator for the current path pointer
            component.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if not self.path:
            # special RFC6901, whole document
            yield ''
        elif len(self.path) == 1 and self.path[0] == '':
            # special RFC6901, '/' empty top-tag
            yield '/'
        else:
            path = self.parent_path if parent else self.path
            if reverse:
                path = reversed(path)

            for sub_path in self.path_producer(path):
                if json_data is not None:
                    node_path, node = self.resolve_path(sub_path, json_data)
                    if node is MISSING or not isinstance(node, self.NODE_TYPES):
                        raise ValueError(
                            'Invalid path node type "%s"' % type(node)
                        )
                yield sub_path[-1]

    def iter_path_nodes(self, json_data, parent=False, reverse=False):
        """
        Iterator for the elements the path pointer points to.

        Args:
            json_data: A valid JSON data node.
            parent: Uses the path pointer to parent node.
            reverse: Reverse the order, start with last.

        Returns:
            Yields the iterator of the current node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if not self.path:
            # special RFC6901, whole document
            yield json_data
        elif len(self.path) == 1 and self.path[0] == '':
            # special RFC6901, '/' empty top-tag
            yield json_data[0] if is_collection(json_data) else json_data['']
        else:
            path = self.parent_path if parent else self.path
            if reverse:
                path = reversed(path)

            for sub_path in self.path_producer(path):
                node_path, node = self.resolve_path(sub_path, json_data)
                if node is MISSING or not isinstance(node, self.NODE_TYPES):
                    raise ValueError(
                        'Invalid path node type "%s"' % type(node)
                    )
                yield node

    def set(self, json_data, value, inplace=True):
        """
        Resolve the pointer against the doc and replace the target with value.
        """
        if len(self.path) == 0:
            if inplace:
                raise JSONPointerException('Cannot set root in place')
            return value

        result = copy.deepcopy(json_data) if not inplace else json_data

        parent, part = self.get_node_and_child(result)

        parent[part] = value
        return result
