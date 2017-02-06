# -*- coding:utf-8   -*-
"""Provides classes for the JSONPointer definition in accordance to RFC6901.

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
__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import sys

version = '{0}.{1}'.format(*sys.version_info[:2])
if not version in ('2.6','2.7',): # pragma: no cover
    raise Exception("Requires Python-2.6.* or higher")
# if version < '2.7': # pragma: no cover
#     raise Exception("Requires Python-2.7.* or higher")

from types import StringTypes,NoneType
import re
try:
    from urllib import unquote
    from itertools import izip
except ImportError: # Python 3
    from urllib.parse import unquote
    izip = zip


# Sets display for inetractive JSON/JSONschema design.
_interactive = False

# Notation a the API - in/out.
NOTATION_JSON = 0 # this is the default
"""JSON notation in accordance to RFC7159
"""

NOTATION_HTTP_FRAGMENT = 1
"""JSON notation in accordance to RFC7159 with RFC3986.
"""

VALID_NODE_TYPE = (dict, list, str, unicode, int, float, bool, NoneType,)
"""Valid types of in-memory JSON node types."""


CHARSET_UTF = 0
"""Unicode."""

CHARSET_STR = 1
"""Python string."""

class JSONPointerException(Exception):
    pass

class JSONPointer(list):
    """Represents exactly one JSONPointer in compliance with IETF RFC6901.
    This pointer could be processed by extension, reduction, and general modification
    with support of provided methods and path arithmetic operators. 
    
    The JSONPointer is provided at the API as a utf(-8) string in accordance 
    to RFC6901, including RFC3869.
    
    For enhancement of the processing performance by the underlying packages 
    'json' and 'jsonschema', the pointer is stored and applied in two variants. 
    
    * self.raw: Raw input of the pointer string for the logical API.
    
    * self.ptr: Split elements of the pointer path within a list of keys,
        for the programming interface.
      
    The attribute 'self.ptr' contains the path elements in a 
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
    the JSONPointer. The parameter 'x' in the operations is defined as a
    valid JSONPointer fragment. A pointer fragment is a part of a pointer,
    which could be the complete pointer itself - the all-fragment. 
    
    The syntax element could be one of::
        
        'str': A string i accordance to RFC6901. Strings are represented 
            internally as unicode utf-8.
            
            Here either the input parameter 'x' is split into
            a list, or in case of combining operations, the self.ptr
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
    
    The node reference is cached by the 'get_node' and 'get_node_or_value' 
    method, thus could be accessed by 'self.node', but is not monitored
    to be valid. Another call of the method reloads the cache by evaluating
    the pointer value on the document again.
    
    The provided value is internally stored as a raw input value, and a list
    of keys and indexes for access to in-memory data as provided by the
    packages 'json' and 'jsonschema'. Requests for the string representation
    are transformed into a pointer path in accordance to RFC6901. This provides
    for fast access in case of pointer arithmetics, while providing standards
    conform path strings at the interface.
    """
    VALID_INDEX = re.compile('0|[1-9][0-9]*$')
    """Regular expression for valid numerical index."""
    
    def __init__(self,ptr,replace=True,**kargs):
        """ Converts and stores a JSONPointer as a list.

        Processes the ABNF of a JSON Pointer from RFC6901.
    
        Args:
            ptr: A JSONPointer to be represented by this object. The
                supported formats are:
                    'str': A string i accordance to RFC6901
                    JSONPointer: A valid object, will be copied 
                        into this, see 'deep'.
                    'list': expects a path list, where each item
                        is processed for escape and unquote.
            replace: Replaces masked characters.
            **kargs:
                deep: Applies for copy operations on structured data
                    'deep' when 'True', else 'swallow' only, which is 
                    just a link to the data structure. Flat data types
                    are copied by value in any case.
                node: Force to set the pointed node in the internal cache. 
                debug: Enable debugging.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception. 
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            JSONPointerException:

        """
        self.debug = kargs.get('debug',False)
        self.node = kargs.get('node',None) # cache for reuse
        self.deep = deep = kargs.get('deep',False)
        if ptr and type(ptr) in (str,unicode) and ptr[0] is '#': # pointer are unicode only
            ptr = ptr[1:]

        if type(ptr) in (int,float): # pointer are unicode only
            ptr=u'/'+unicode(ptr)
        
        if ptr == '': # shortcut for whole document, see RFC6901
            self.raw = ''
            self = []
            return None
        
        elif ptr == '/': # shortcut for empty tag at top-level, see RFC6901
            self.raw = ptr
            self.append('')
            return None

        elif isinstance(ptr, StringTypes): # string in accordance to RFC6901
            if ptr[0] == '/':
                self.extend(ptr[1:].split('/'))
            else:                
                self.extend(ptr.split('/'))
                ptr = u'/'+ptr # any pointer is absolute due to RFC6901, force it silently for smart loops

            if deep:
                self.raw = ptr[:]
            else:    
                self.raw = ptr

        elif isinstance(ptr, JSONPointer): # copy a pointer, source has to be valid
            if deep:
                self.raw = ptr.raw[:]
                self.extend(ptr.copy_path())
            else:
                self.raw = ptr.raw
                self.extend(ptr)

        elif type(ptr) is list: # list of entries in accordance to RFC6901, and JSONPointer
            def presolv(p0):
                if isinstance(p0, JSONPointer): # copy constructor
                    return p0.ptr
                elif p0 in ('', '/'): 
                    return p0
                elif type(p0) in (str,unicode): 
                    return p0
                elif type(p0) in (int,float): 
                    return str(p0)
                else:
                    raise JSONPointerException("Invalid nodepart:"+str(p0)) 
                return p0
            if deep:    
                self.extend(map(lambda s:s[:],ptr))
            else:    
                self.extend(map(presolv,ptr))
            self.raw = '/'+'/'.join(self)
        else:
            if not ptr:
                self.raw = None
                return None
            raise JSONPointerException("Pointer type not supported:",type(ptr))

        if replace:
            x = map(lambda p: type(p) in (str,unicode) and unquote(p).replace('~1', '/').replace('~0', '~') or p,self) # 6901-escaped, generic chars-quote
            del self[:] 
            self.extend(x)
        #FIXME: check wheter the assumption is viable
        # SPECIAL: assumes digit only as array index
        def checkint(ix):
            if type(ix) in (str,unicode,) and ix.isdigit():
                return int(ix)
            return ix
        x = map(checkint,self)
        del self[:] 
        self.extend(x)
   
    def __add__(self, x):
        """Appends a Pointer to self.

        Args:
            x: A valid JSONPointer fragment.

        Returns:
            A new object of JSONPointer
            
        Raises:
            JSONPointerException:

        """
        ret = JSONPointer(self)
        if type(x) in (str,unicode) and x[0] is '#': # pointer are unicode only, RFC6901/RFC3829
            x = x[1:]
        
        if x == '': # whole document, RFC6901
            raise JSONPointerException("Cannot add the whole document")
        elif x == u'/': # empty tag
            ret.raw += x
            ret.append('')

        elif isinstance(x, JSONPointer):
            ret.raw += x.raw
            ret.extend(x)
        elif type(x) == list:
            ret.raw += u'/'+u'/'.join(x)
            ret.extend(x)
        elif type(x) in (str,unicode):
            if x[0] == u'/':
                ret.extend(x[1:].split('/'))
                ret.raw += x
            else:
                ret.extend(x.split('/'))
                ret.raw += u'/'+x
        elif type(x) is int:
            ret.append(x)
            ret.raw += u'/'+unicode(x)
        elif type(x) is NoneType:
            return ret

        else:
            raise JSONPointerException()
        return ret

    def __call__(self, x):
        """Evaluates the pointed value from the document.

        Args:
            x: A valid JSON document.

        Returns:
            The pointed value, or None.

        Raises:
            JSONPointerException
        """
        return self.get_node_or_value(x)

    def __eq__(self, x):
        """Compares this pointer with x.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        s = u'/'+u'/'.join(map(unicode,self))
       
        if isinstance(x, JSONPointer):
            return s == x.get_pointer()
        elif type(x) == list:
            #return s == unicode("/"+'/'.join(x))
            return s == JSONPointer(x).get_pointer()
        elif type(x) in (str,unicode):
            return s == unicode(x)
        elif type(x) in (int):
            return s == u'/'+unicode(x)
        elif type(x) is NoneType:
            return False
        
        else:
            raise JSONPointerException()
        return False

    def __ge__(self, x):
        """Checks containment(>=) of another pointer within this.

        The weight of contained entries is the criteria, though
        the shorter is the bigger. This is true only in case of
        a containment relation.
         
        The number of equal path pointer items is compared.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:

        """
        s = u'/'+u'/'.join(map(unicode,self))
       
        if isinstance(x, JSONPointer):
            px = x.get_pointer()
        elif type(x) == list:
            px = u"/"+'/'.join(map(unicode,x))
        elif type(x) in (str,unicode):
            px = unicode(x)
        elif type(x) in (int):
            px = u'/'+unicode(x)
        elif type(x) is NoneType:
            return True
        
        else:
            raise JSONPointerException()

        if s > px: # the shorter is the bigger
            return False
        if unicode(px).startswith(unicode(s)): # matching part has to be literal
            return True
        else:
            return False

    def __gt__(self, x):
        """Checks containment(>) of another pointer or object within this.

        The number of equal items is compared.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        s = u'/'+u'/'.join(map(unicode,self))
       
        if isinstance(x, JSONPointer):
            px = x.get_pointer()
        elif type(x) == list:
            px = u"/"+u'/'.join(map(unicode,x))
        elif type(x) in (str,unicode):
            px = unicode(x)
        elif type(x) in (int):
            px = u'/'+unicode(x)
        elif type(x) is NoneType:
            return True

        else:
            raise JSONPointerException()

        if s >= px: # the shorter is the bigger, so false in any case
            return False
        if unicode(px).startswith(unicode(s)): # matching part has to be literal
            return True
        else:
            return False

    def __iadd__(self, x):
        """Add in place x to self, appends a path.

        Args:
            x: A valid Pointer.

        Returns:
            'self' with updated pointer attributes

        Raises:
            JSONPointerException:
        """
        if type(x) == list:
            self.raw += unicode('/'+'/'.join(x))
            self.extend(x)
        elif isinstance(x, JSONPointer):
            if x.raw[0] != u'/':
                self.raw += u'/'+x.raw
            else:
                self.raw = x.raw
            self.extend(x)
        elif type(x) is int:
            self.append(unicode(x))
            self.raw += u'/'+unicode(x)
        elif x == '': # whole document, RFC6901
            raise JSONPointerException("Cannot add the whole document")
        elif x == u'/': # empty tag
            self.raw += x
            self.append('')
        elif type(x) in (str,unicode):
            if x[0] == u'/':
                self.extend(x[1:].split('/'))
                self.raw += x
            else:
                self.extend(x.split('/'))
                self.raw += u'/'+x
        elif type(x) is NoneType:
            return self

        else:
            raise JSONPointerException()
        return self
        
    def __le__(self, x):
        """Checks containment(<=) of this pointer within another.

        The number of equal items is compared.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        s = u'/'+u'/'.join(map(unicode,self))
       
        if isinstance(x, JSONPointer):
            px = x.get_pointer()
        elif type(x) == list:
            px = u"/"+u'/'.join(map(unicode,x))
        elif type(x) in (str,unicode):
            px = unicode(x)
        elif type(x) in (int):
            px = u'/'+unicode(x)
        elif type(x) is NoneType:
            return False

        else:
            raise JSONPointerException()

        if s < px: # the shorter is the bigger
            return False
        if unicode(s).startswith(unicode(px)): # matching part has to be literal
            return True

    def __lt__(self, x):
        """Checks containment(<) of this pointer within another.

        The number of equal items is compared.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException:
        """
        s = u'/'+u'/'.join(map(unicode,self))
       
        if isinstance(x, JSONPointer):
            px = x.get_pointer()
        elif type(x) == list:
            px = u"/"+u'/'.join(map(unicode,x))
        elif type(x) in (str,unicode):
            px = unicode(x)
        elif type(x) in (int):
            px = u'/'+unicode(x)
        elif type(x) is NoneType:
            return False

        else:
            raise JSONPointerException()

        if s <= px: # the shorter is the bigger
            return False
        if unicode(s).startswith(unicode(px)): # matching part has to be literal
            return True

    def __ne__(self, x):
        """Compares this pointer with x.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        return not self.__eq__(x)

    def __radd__(self, x):
        """Adds itself as the right-side-argument to the left.
        
        This method appends 'self' to a path fragment on the left.
        Therefore it adds the path separator on it's left side only.
        The left side path fragment has to maintain to be in 
        accordance to RFC6901 by itself.

        Once 'self' is added to the left side, it terminates it's
        life cycle. Thus another simultaneous add operation is 
        handled by the resulting other element.
         
        Args:
            x: A valid Pointer.

        Returns:
            The updated input of type 'x' as 'x+S(x)'

        Raises:
            JSONPointerException:
        """
        if x == '': # whole document, RFC6901
            return u'/'+u'/'.join(map(unicode,self))
        elif x == u'/': # empty tag
            return x+u'/'+u'/'.join(map(unicode,self))
        elif type(x) is int:
            return u'/'+unicode(x)+u'/'+u'/'.join(map(unicode,self))
        elif type(x) in (str,unicode):
            return x+u'/'+u'/'.join(map(unicode,self))
        elif type(x) == list:
            return x.extend(self)
        else:
            raise JSONPointerException()
        return x

    def __repr__(self):
        """Returns the attribute self.raw, which is the raw input JSONPointer.
        """
        return unicode(super(JSONPointer,self).__repr__())

    def __str__(self):
        """Returns the string for the processed path.
        """
        ret = self.get_pointer()
        if ret == '':
            return "''"
        return ret

    #
    # ---
    #

    def check_node_or_value(self,jsondata,parent=False):
        """Checks the existance of the corresponding node within the JSON document.

        Args:
            jsondata: A valid JSON data node.
            parent: Return the parent node of the pointed value.

        Returns:
            True or False
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if self == []: # special RFC6901, whole document
            return jsondata
        if self == ['']: # special RFC6901, '/' empty top-tag
            return jsondata['']
        
        if type(jsondata) not in VALID_NODE_TYPE:
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))

        if parent:
            for x in self.ptr[:-1]:
                jsondata=jsondata.get(x,False)
                if not jsondata:
                    return False
        else:
            for x in self.ptr:
                jsondata=jsondata.get(x,False)
                if not jsondata:
                    return False

        if type(jsondata) not in VALID_NODE_TYPE:
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
        self.node = jsondata # cache for reuse
        return True

    def copy_path_list(self,parent=False):
        """Returns a deep copy of the objects pointer path list.

        Args:
            parent: The parent node of the pointer path.

        Returns:
            A copy of the path list.
            
        Raises:
            none
        """
        if self == []: # special RFC6901, whole document
            return []
        if self == ['']: # special RFC6901, '/' empty top-tag
            return ['']
        
        if parent:
            return map(lambda s:s[:],self[:-1])
        else:
            return map(lambda s:s[:],self[:])

    def get_node(self,jsondata,parent=False):
        """Gets the corresponding node reference for a JSON container type.
        
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
            get_node_exist: For the application of partial valid 
                pointer paths of new branches.
            get_node_or_value: For any type of pointed item, either 
                a node, or a value. 
        
        Args:
            jsondata: A valid JSON data node.
            parent: Return the parent node of the pointed value.
                When parent is selected, the pointed child node
                is not verified. 

        Returns:
            The node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if self == []: # special RFC6901, whole document
            return jsondata
        if len(self) == 1 and self[0] == '': # special RFC6901, '/' empty top-tag
            return jsondata[0]
        
        if type(jsondata) not in (dict, list):
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))

        try:
            if parent:
                for x in self[:-1]:
                    jsondata=jsondata[x] # want the exception, the keys within the process has to match
            else:
                for x in self:
                    jsondata=jsondata[x] # want the exception, the keys within the process has to match
        except Exception as e:
            raise JSONPointerException("Requires existing Node("+str(self.index(x))+"):"+str(x)+" of "+str(self)+":"+str(e)) 
        if type(jsondata) not in (dict, list):
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
        self.node = jsondata # cache for reuse
        return jsondata

    def get_node_and_child(self,jsondata):
        """Returns a tuple containing the parent node and the child.

        Args:
            jsondata: A valid JSON data node.

        Returns:
            The the tuple:
            (n,c):  n: Node reference to parent container.
                    c: Key for the child entry, either an 
                       index 'int', or a key ('str', 'unicode'). 
        Raises:
            JSONPointerException:
            forwarded from json
        """
        n = self.get_node(jsondata,True)
        return n,self[-1]
    
    def get_node_or_value(self,jsondata,valtype=None,parent=False):
        """Gets the corresponding node reference or the JSON value of a leaf.

        Relies on the standard package 'json' by 'Bob Ippolito <bob@redivi.com>'.
        This package supports in the current version the following types:
        
            +---------------+-------------------+
            | JSON          | Python            |
            +===============+===================+
            | object        | dict              |
            +---------------+-------------------+
            | array         | list              |
            +---------------+-------------------+
            | string        | unicode           |
            +---------------+-------------------+
            | number (int)  | int, long         |
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
            | JSONPointer(jsondata)  | Python-valtype    |
            +========================+===================+
            | object (dict)          | dict              |
            +------------------------+-------------------+
            | array  (list)          | list              |
            +------------------------+-------------------+
            | array  (tuple)         | list              |
            +------------------------+-------------------+
            | string                 | unicode           |
            +------------------------+-------------------+
            | number (int)           | int               |
            +------------------------+-------------------+
            | number (long)          | long              |
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
        
        * string(str) => unicode"
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
        
        * null(None) => NoneType(None):
            False - native Python NoneType

        Args:
            jsondata: A valid JSON data node.
            valtype: Type of requested value.
            parent: Return the parent node of the pointed value.

        Returns:
            The node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if not self: #  == [] : special RFC6901, whole document
            return jsondata
        if len(self) == 1 and self[0] == '': # special RFC6901, '/' empty top-tag
            return jsondata['']

        if type(jsondata) not in VALID_NODE_TYPE: # requires an object or an array as input
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))

        try:
            if parent: # request for container
                for x in self[:-1]:
                    jsondata=jsondata[x] # want the exception
            else:
                for x in self:
                    jsondata=jsondata[x] # want the exception
        except Exception as e:
            raise JSONPointerException("Node("+str(self.index(x))+"):"+str(x)+" of "+str(self)+":"+str(e)) 
        if valtype: # requested value type
            # fix type ambiguity for numeric
            if valtype in (int,float):
                if jsondata.isdigit():
                    jsondata = int(jsondata)
            elif valtype in (int,float):
                #FIXME:
                if jsondata.isdigit():
                    jsondata = float(jsondata)
            
            if not type(jsondata) is valtype:
                raise JSONPointerException("Invalid path value type:"+str(type(valtype))+" != "+str(type(jsondata)))
        else: # in general valid value types - RFC4729,RFC7951
            if type(jsondata) not in VALID_NODE_TYPE:
                raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
        self.node = jsondata # cache for reuse
        return jsondata

    def get_node_exist(self,jsondata,parent=False):
        """Returns the node for valid part of the pointer, and the remaining part.
        
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
            jsondata: A valid JSON data node.
            parent: Return the parent node of the pointed value.

        Returns:
            The node reference, and the remaining part.
            ret:=[ node, [<remaining-path-components-list>] ]
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if self == []: # special RFC6901, whole document
            return jsondata
        if self == ['']: # special RFC6901, '/' empty top-tag
            return jsondata['']
        
        if type(jsondata) not in (dict, list):
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))
        remaining = None
        try:
            if parent:
                for x in self[:-1]:
                    remaining = x
                    jsondata=jsondata[x] # want the exception, the keys within the process has to match
            else:
                for x in self:
                    remaining = x
                    jsondata=jsondata[x] # want the exception, the keys within the process has to match
        except Exception:
            if parent:
                remaining = self[self.index(remaining):-1]
            else:
                remaining = self[self.index(remaining):]
        if type(jsondata) not in (dict, list):
            # concrete info for debugging for type mismatch
            raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
        self.node = jsondata # cache for reuse
        return [jsondata, remaining]

    def get_path_list(self):
        """Gets for the corresponding path list of the object pointer for in-memory access on the data of the 'json' package.

        Args:
            none

        Returns:
            The path list.
            
        Raises:
            none
        """
        if __debug__:
            if self.debug:
                print repr(self)
        return list(self)

    def get_path_list_and_key(self):
        """Gets for the corresponding path list of the object pointer for in-memory access on the data of the 'json' package.

        Args:
            none

        Returns:
            The path list.
            
        Raises:
            none
        """
        if len(self)>2:
            return self[:-1],self[-1]
        elif len(self)==1:
            return [],self[-1]
        elif len(self)==0:
            return [],None

    def get_pointer(self,forcenotation=None,parent=False):
        """Gets the objects pointer in compliance to RFC6901.

        Args:
            forcenotation: Force the output notation to:
                None := NOTATION_JSON,
                NOTATION_JSON = 0,
                NOTATION_HTTP_FRAGMENT = 1
                
            parent: Get parent of selected node.

        Returns:
            The pointer in accordance to RFC6901.
            
        Raises:
            none
        """
        if not self: # ==[] : special RFC6901, whole document
            return ''
        if len(self) == 1 and self[0] == '': # special RFC6901, '/' empty top-tag
            return '/'

        if parent:
            return unicode('/'+'/'.join(map(unicode,self[:-1])))
        else:
            return unicode('/'+'/'.join(map(unicode,self)))

    def get_raw(self):
        """Gets the objects raw 6901-pointer.

        Args:
            none

        Returns:
            The raw path.
            
        Raises:
            none
        """
        return self.raw

    def iter_path(self,jsondata=None,parent=False,rev=False):
        """Iterator for the elements of the path pointer itself.

        Args:
            jsondata: If provided a valid JSON data node, the
                path components are successively verified on
                the provided document. If None the path pointer
                components are just iterated.
            parent: Uses the path pointer to parent node.
            rev: Reverse the order, start with last.

        Returns:
            Yields the iterator for the current path pointer
            component.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if self.ptr == []: # special RFC6901, whole document
            yield ''
        elif self.ptr == ['']: # special RFC6901, '/' empty top-tag
            yield '/'
        else:
            if jsondata and type(jsondata) not in (dict, list):
                # concrete info for debugging for type mismatch
                raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))
    
            if rev: # reverse
                if parent: # for parent
                    ptrpath = self.ptr[:-1:-1]
                else: # full path
                    ptrpath = self.ptr[::-1]
            else:
                if parent: # for parent
                    ptrpath = self.ptr[:-1]
                else: # full path
                    ptrpath = self.ptr
    
            try:
                x = ptrpath[0]
                for x in ptrpath:
                    if jsondata:
                        jsondata=jsondata[x] # want the exception, the keys within the process has to match
                        if type(jsondata) not in (dict, list):
                            # concrete info for debugging for type mismatch
                            raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
                    yield x
            except Exception as e:
                raise JSONPointerException("Node("+str(ptrpath.index(x))+"):"+str(x)+" of "+str(self.ptr)+":"+str(e)) 
            self.node = jsondata # cache for reuse

    def iter_path_nodes(self,jsondata,parent=False,rev=False):
        """Iterator for the elements the path pointer points to.

        Args:
            jsondata: A valid JSON data node.
            parent: Uses the path pointer to parent node.
            rev: Reverse the order, start with last.

        Returns:
            Yields the iterator of the current node reference.
            
        Raises:
            JSONPointerException:
            forwarded from json
        """
        if self.ptr == []: # special RFC6901, whole document
            yield jsondata
        elif self.ptr == ['']: # special RFC6901, '/' empty top-tag
            yield jsondata['']
        else:
            if type(jsondata) not in (dict, list):
                # concrete info for debugging for type mismatch
                raise JSONPointerException("Invalid nodetype parameter:"+str(type(jsondata)))
    
            if rev: # reverse
                if parent: # for parent
                    ptrpath = self.ptr[:-1:-1]
                else: # full path
                    ptrpath = self.ptr[::-1]
            else:
                if parent: # for parent
                    ptrpath = self.ptr[:-1]
                else: # full path
                    ptrpath = self.ptr
    
            try:
                x = ptrpath[0]
                for x in ptrpath:
                    jsondata=jsondata[x] # want the exception, the keys within the process has to match
                    if type(jsondata) not in (dict, list):
                        # concrete info for debugging for type mismatch
                        raise JSONPointerException("Invalid path nodetype:"+str(type(jsondata)))
                    yield jsondata
            except Exception as e:
                raise JSONPointerException("Node("+str(ptrpath.index(x))+"):"+str(x)+" of "+str(self.ptr)+":"+str(e)) 
            self.node = jsondata # cache for reuse
