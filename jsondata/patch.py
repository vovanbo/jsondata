# -*- coding:utf-8   -*-
"""The JSONPatch module provides for the alteration of JSON data compliant to RFC6902.

The emphasis of the design combines low resource requirement with features
designed for the application of large filters onto large JSON based data 
structures.

The patch list itself is defined by RFC6902 as a JSON array. The entries 
could be either constructed in-memory, or imported from a persistent storage.
The export feature provides for the persistent storage of a modified patch
list for later reuse.

The module contains the following classes:

* **JSONPatch**:
    The controller for the application of patches on in-memory
    data structures provided by the package 'json'.
    
* **JSONPatchItem**:
    Representation of one patch entry in accordance to RFC6902.

* **JSONPatchItemRaw**:
    Representation of one patch entry read as a raw entry in accordance to RFC6902.

* **JSONPatchFilter**:
    Selection filter for the application on the current patch list
    entries JSONPatchItem.

* **JSONPatchException**:
    Specific exception for this module.


The address of the the provided 'path' components for the entries are managed
by the class JSONPointer in accordance to RFC6901. 
"""
from enum import unique, Enum

try:
    import ujson as myjson
except ImportError:
    import json as myjson

from .exceptions import JSONPatchException, JSONPatchItemException
from .pointer import JSONPointer
from .serializer import JSONDataSerializer
from .data import SchemaMode

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'


@unique
class Op(str, Enum):
    """
    Operations in accordance to RFC6902
    """
    ADD = 'add'
    COPY = 'copy'
    MOVE = 'move'
    REMOVE = 'remove'
    REPLACE = 'replace'
    TEST = 'test'


def get_op(x):
    """
    Converts input into corresponding enumeration.
    """
    if isinstance(x, Op):
        return x
    elif isinstance(x, str):
        return Op(x)
    else:
        return None


class JSONPatchItem(object):
    """Record entry for list of patch tasks.
    
    Attributes:
        op: operations:
                add, copy, move, remove, replace, test
        
        target: JSONPointer for the modification target, see RFC6902.
        
        value: Value, either a branch, or a leaf of the JSON data structure.
        src:  JSONPointer for the modification source, see RFC6902.
        
    """

    def __init__(self, op, target, param=None):
        """Create an entry for the patch list.

        Args:
            op: Operation: add, copy, move, remove, replace, test

            target: Target node.
                    
            param: Parameter specific for the operation:
                value: add,replace, test
                src: copy, move
                param:=None for 'remove'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            JSONDataSerializerError:
        
        """
        self.value = None
        self.src = None

        self.op = get_op(op)
        self.target = JSONPointer(target)

        if self.op in (Op.ADD, Op.REPLACE, Op.TEST):
            self.value = param
        elif self.op is Op.REMOVE:
            pass
        elif self.op in (Op.COPY, Op.MOVE):
            self.op = op
            self.src = param
        else:
            raise JSONPatchItemException("Unknown operation.")

    def __call__(self, j):
        """Evaluates the related task for the provided data.

        Args:
            j: JSON data the task has to be 
                applied on.

        Returns:
            Returns a tuple of:
                0: len of the job list
                1: list of the execution status for 
                    the tasks

        Raises:
            JSONPatchException:
        """
        return self.apply(j)

    def __eq__(self, x):
        """Compares this pointer with x.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        ret = True

        if isinstance(x, dict):
            ret &= self.target == x['path']
        else:
            ret &= self.target == x['target']

        if self.op is Op.ADD:
            ret &= x['op'] == Op.ADD
            ret &= self.value == x['value']
        elif self.op is Op.REMOVE:
            ret &= x['op'] == Op.REMOVE
        elif self.op is Op.REPLACE:
            ret &= x['op'] == Op.REPLACE
            ret &= self.value == x['value']
        elif self.op is Op.MOVE:
            ret &= x['op'] == Op.MOVE
            ret &= self.src == x['from']
        elif self.op is Op.COPY:
            ret &= x['op'] == Op.COPY
            ret &= self.src == x['from']
        elif self.op is Op.TEST:
            ret &= x['op'] == Op.TEST
            ret &= self.value == x['value']

        return ret

    def __getitem__(self, key):
        """Support of various mappings.
        
            #. self[key]
            
            #. self[i:j:k]
            
            #. x in self
            
            #. for x in self

        """
        if key in ('path', 'target',):
            return self.target
        elif key in ('op',):
            return self.op
        elif key in ('value', 'param',):
            return self.value
        elif key in ('from', 'src',):
            return self.src

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

    def __repr__(self):
        """Prints the patch string in accordance to RFC6901.
        """
        ret = "{'op': '%s', 'path': '%s'" % (self.op.value, self.target)
        if self.op in (Op.ADD, Op.REPLACE, Op.TEST):
            if isinstance(self.value, (int, float)):
                ret += ", 'value': %s" % self.value
            elif type(self.value) in (dict, list):
                ret += ", 'value': %r" % self.value
            else:
                ret += ", 'value': '%s'" % self.value

        elif self.op is Op.REMOVE:
            pass

        elif self.op in (Op.COPY, Op.MOVE):
            ret += ", 'from': '%s'" % self.src
        ret += "}"
        return ret

    def __str__(self):
        """Prints the patch string in accordance to RFC6901.
        """
        ret = "{'op': '%s', 'target': '%s'" % (self.op.value, self.target)
        if self.op in (Op.ADD, Op.REPLACE, Op.TEST):
            if type(self.value) in (int, float):
                ret += '", "value": %s }' % self.value
            else:
                ret += '", "value": "%s" }' % self.value

        elif self.op is Op.REMOVE:
            ret += '" }'

        elif self.op in (Op.COPY, Op.MOVE):
            ret += '", "src": "%s" }' % self.src
        return ret

    def apply(self, jsondata):
        """Applies the present patch list on the provided JSON document.

        Args:
            jsondata: Document to be patched.
        Returns:
            When successful returns 'True', else raises an exception.
            Or returns a tuple:
              (n,lerr): n:    number of present active entries
                        lerr: list of failed entries
        Raises:
            JSONPatchException:
        """

        if self.op is Op.ADD:
            # n,b = self.target.get_node_and_child(jsondata)

            nbranch = jsondata.branch_add(self.target, None, self.value)
            return True

        if isinstance(jsondata, JSONDataSerializer):
            jsondata = jsondata.data

        if self.op is Op.REPLACE:
            n, b = self.target.get_node_and_child(jsondata)
            n[str(b)] = str(self.value)

        elif self.op is Op.TEST:
            n, b = JSONPointer(self.target, False).get_node_and_child(jsondata)
            if isinstance(self.value, str):
                self.value = str(self.value)
            if isinstance(n, list):
                return n[b] == self.value
            return n[str(b)] == self.value
        elif self.op is Op.COPY:
            val = JSONPointer(self.src).get_node_or_value(jsondata)
            tn, tc = self.target.get_node_and_child(jsondata)
            tn[tc] = val

        elif self.op is Op.MOVE:
            val = JSONPointer(self.src).get_node_or_value(jsondata)
            sn, sc = JSONPointer(self.src).get_node_and_child(jsondata)
            sn.pop(sc)
            tn, tc = self.target.get_node_and_child(jsondata)
            if isinstance(tn, list):
                if len(tn) <= tc:
                    tn.append(val)
                else:
                    tn[tc] = val
            else:
                tn[tc] = val

        elif self.op is Op.REMOVE:
            n, b = self.target.get_node_and_child(jsondata)
            n.pop(b)

        return True

    def repr_export(self):
        """Prints the patch string for export in accordance to RFC6901.
        """
        ret = '{"op": "%s", "path": "%s"' % (self.op.value, self.target)
        if self.op in (Op.ADD, Op.REPLACE, Op.TEST):
            if isinstance(self.value, (int, float)):
                ret += ', "value": %s' % self.value
            elif isinstance(self.value, (dict, list)):
                ret += ', "value": %s' % self.value
            else:
                ret += ', "value": "%s"' % self.value

        elif self.op is Op.REMOVE:
            pass

        elif self.op in (Op.COPY, Op.MOVE):
            ret += ', "from": "%s"' % self.src
        ret += '}'
        return ret


class JSONPatchItemRaw(JSONPatchItem):
    """Adds native patch strings or an unsorted dict for RFC6902.
    """

    def __init__(self, patch_string):
        """
        Parse a raw patch string in accordance to RFC6902.
        """
        if isinstance(patch_string, str):
            ps = myjson.loads(patch_string)
            sx = myjson.dumps(ps)
            # print "<"+str(sx)+">"
            # print "<"+str(patch_string)+">"
            # l0 = len(sx.replace(" ",""))
            # l1 = len(patch_string.replace(" ",""))
            if len(sx.replace(" ", "")) != len(patch_string.replace(" ", "")):
                raise JSONPatchItemException(
                    "Repetition is not compliant to RFC6902: %s" % patch_string
                )
        elif isinstance(patch_string, dict):
            ps = patch_string
        else:
            raise JSONPatchItemException(
                "Type not supported: %s" % patch_string
            )

        try:
            target = ps['path']
            op = get_op(ps['op'])

            if op in (Op.ADD, Op.REPLACE, Op.TEST):
                param = ps['value']
            elif op is Op.REMOVE:
                param = None
            elif op in (Op.COPY, Op.MOVE):
                param = ps['from']
        except Exception as e:
            raise JSONPatchItemException(e)

        super(JSONPatchItemRaw, self).__init__(op, target, param)


class JSONPatchFilter(object):
    """
    Filtering capabilities on the entries of patch lists.
    """

    def __init__(self, prefix=None, branch=None):
        """
        Args:
            **kwargs: Filter parameters:
                Common:

                    contain=(True|False): Contain, else equal.

                    type=<node-type>: Node is of type.
                
                Paths:

                    branch=<branch>: 

                    deep=(): Determines the depth of comparison.

                    prefix=<prefix>: Any node of prefix. If prefix is
                        absolute: the only and one, else None.
                        relative: any node prefixed by the path fragment.
                
                Values:
                    val=<node-value>: Node ha the value.
                
    
        Returns:
            True or False
    
        Raises:
            JSONPointerException:
        """
        self.prefix = prefix
        self.branch = branch

    def __eq__(self, x):
        pass

    def __ne__(self, x):
        pass


class JSONPatch(object):
    """
    Representation of a JSONPatch task list for RFC6902.
    
    Contains the defined methods from standards:

    * add
    * remove
    * replace
    * move
    * copy
    * test
     
    Attributes:
        patch: List of patch items.
        
    """

    def __init__(self, patch=None):
        self.patch = patch or []
        """List of patch tasks. """

        self.deep = False
        """Defines copy operations, True:=deep, False:=swallow"""

    #
    # --- RFC6902 JSON patch files
    #

    def __add__(self, x=None):
        """
        Creates a copy of 'self' and adds a patch jobs to the task queue.
        """
        if not x:
            raise JSONPatchException("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            return JSONPatch(self.patch).patch.append(x)
        elif isinstance(x, JSONPatch):
            return JSONPatch(self.patch).patch.extend(x.patch)
        else:
            raise JSONPatchException("Unknown input" + type(x))

    def __call__(self, j, x=None):
        """
        Evaluates the related task for the provided index.

        Args:
            x: Task index.

            j: JSON data the task has to be 
                applied on.

        Returns:
            Returns a tuple of:
                0: len of the job list
                1: list of the execution status for 
                    the tasks

        Raises:
            JSONPatchException:
        """
        if x is None:
            return self.apply(j)
        if self.patch[x](j):
            return 1, []
        return 1, [0]

    def __eq__(self, x):
        """
        Compares this pointer with x.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        match = len(self.patch)
        if match != len(x):
            return False

        for p in sorted(self.patch):
            for xi in sorted(x):
                if p == xi:
                    match -= 1
                    continue
        return match == 0

    def __getitem__(self, key):
        """
        Support of slices, for 'iterator' refer to self.__iter__.
        
            #. self[key]
            
            #. self[i:j:k]
            
            #. x in self
            
            #. for x in self

        """
        return self.patch[key]

    def __iadd__(self, x=None):
        """
        Adds patch jobs to the task queue in place.
        """
        if not x:
            raise JSONPatchException("Missing patch entry/patch")
        if isinstance(x, JSONPatchItem):
            self.patch.append(x)
        elif isinstance(x, JSONPatch):
            self.patch.extend(x.patch)
        else:
            raise JSONPatchException("Unknown input" + type(x))
        return self

    def __isub__(self, x):
        """
        Removes the patch job from the task queue in place.
        
        Removes one of the following type(x) variants:
        
            int: The patch job with given index.
             
            JSONPatchItem: The first matching entry from 
                the task queue. 

        Args:
            x: Item to be removed.

        Returns:
            Returns resulting list without x.

        Raises:
            JSONPatchException:
        """
        if isinstance(x, int):
            self.patch.pop(x)
        else:
            self.patch.remove(x)
        return self

    def __iter__(self):
        """
        Provides an iterator foreseen for large amounts of in-memory patches.
        """
        return iter(self.patch)

    def __len__(self):
        """
        The number of outstanding patches.
        """
        return len(self.patch)

    def __ne__(self, x):
        """
        Compares this pointer with x.

        Args:
            x: A valid Pointer.

        Returns:
            True or False

        Raises:
            JSONPointerException
        """
        return not self.__eq__(x)

    def __repr__(self):
        """
        Prints the representation format of a JSON patch list.
        """
        ret = "["
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += '%r,' % p
            ret += repr(self.patch[-1])
        ret += "]"
        return str(ret)

    def __str__(self):
        """
        Prints the display format.
        """
        ret = "[\n"
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += "  %r,\n" % p
            ret += "  %r\n" % self.patch[-1]
        ret += "]"
        return str(ret)

    def __sub__(self, x):
        """
        Removes the patch job from the task queue.
        
        Removes one of the following type(x) variants:
        
            int: The patch job with given index.
             
            JSONPatchItem: The first matching entry from 
                the task queue. 

        Args:
            x: Item to be removed.

        Returns:
            Returns resulting list without x.

        Raises:
            JSONPatchException:
        """
        ret = JSONPatch()
        if self.deep:
            ret.patch = self.patch[:]
        else:
            ret.patch = self.patch
        if type(x) is int:
            ret.patch.pop(x)
        else:
            ret.patch.remove(x)
        return ret

    def apply(self, jsondata):
        """
        Applies the JSONPatch task.

        Args:
            jsondata: JSON data the job list has to be applied on.

        Returns:
            Returns a tuple of:
                0: len of the job list
                1: list of the execution status for the tasks

        Raises:
            JSONPatchException:
        """
        status = []
        for p in self.patch:
            if not p.apply(jsondata):
                status.append(
                    self.patch.index(p))  # should not be called frequently
        return len(self.patch), status

    def get(self, x=None):
        ret = self.patch

        # FIXME:
        return ret

    def patch_export(self, patch_file, schema=None, **kwargs):
        """Exports the current task list.
        
        Provided formats are:
            RFC6902

        Supports the formats:
            RFC6902

        Args:
            patch_file:
                JSON patch for export.
            schema:
                JSON-Schema for validation of the patch list.
            **kwargs:
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    default:= validate

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            JSONPatchException:

        """
        try:
            with open(patch_file, 'w') as fp:
                fp.writelines(self.repr_export())
        except Exception as e:
            raise JSONPatchException("open-" + str(e), "data.dump",
                                     str(patch_file))
        return True

    def patch_import(self, patch_file, schema_file=None, appname='jsonpatch',
                     validator=SchemaMode.OFF, no_default_path=True,
                     path_list=None,):
        """
        Imports a task list.

        Supports the formats:
            RFC6902

        Args:
            patch_file:
                JSON patch filename containing the list of patch operations.
            schema_file:
                JSON-Schema filename for validation of the patch list.
            **kwargs:
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    default:= validate

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            JSONPatchException:

        """
        patch_data = JSONDataSerializer(
            appname, data_file=patch_file, schema_file=schema_file,
            validator=validator, no_default_path=no_default_path,
            path_list=path_list
        )

        for pi in patch_data.data:
            self += JSONPatchItemRaw(pi)
        return True

    def repr_export(self):
        """
        Prints the export representation format of a JSON patch list.
        """
        ret = "["
        if self.patch:
            if len(self.patch) > 1:
                for p in self.patch[:-1]:
                    ret += p.repr_export() + ", "
            ret += self.patch[-1].repr_export()
        ret += "]"
        return ret
