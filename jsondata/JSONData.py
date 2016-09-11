# -*- coding:utf-8   -*-
""" Basic features for the persistence of JSON based in-memory data.

The management of modular applications based on plugins frequently requires the
incremental extension of data models. Therefore this package provides the load
of a master model from a JSON file, and the incremental addition and removal of
branches to the model by loading additional JSON modules into the master model.

The schemas for the main application data and the import API are provided by
the framework, whereas the plugins may provide their own means of validation
within the local namespace, and/or scope.

The implementation is based on the standard packages 'json' and 'jsonschema'.

The workflow provided by this package is:

  0. Create the initial in-memory data model by loading the master JSON data.
     Decide here to use validation or not.

     Even though the validation itself could be shifted to a later state,
     once the data is loaded it may alter the state of the application
     irreversible.

  1. Add/insert an arbitrary number of branches provided e.g. by plugins
     into an arbitrary position of the data model.

     Now for the branch decide whether to validate or not.

The data could be validated by provided JSONschema files. The interface
supports for various types of branch insertion and deletion.

The supported data resulting into a tree-structure could be depicted as::

    root-node
        |
    APP-schema
        +- <= import/export A-branches <-> API-schema + A-schema
        |
        +- <= import/export B-branches <-> API-schema + B-schema
        |
        `- <= import/export C-branches <-> API-schema + C-schema


In case of requested validation various schema files are required.
The main schema for the application 'APP-schema' has to be provided
for the core application.

The APP-schema provides in case of persistent configuration data the
structural model for the statically related data of the application
code. E.g. in case of the setup for the configuration of an implemented
view model, the APP-schema may contain the implemented data structure
of the application. The 'datafile' with values, e.g. altered by user
interaction, could be varied and superposed as required, as long
as the structure is valid.

The import interface represented in 'API-schema' is for the case of
validation mandatory too. This ensures valid interface data only is
imported into the application. Whereas the specific schema
files(A,B,C-schema) depend on the actual implementation and
requirements of the imported modules.

The resulting data could be saved for later reuse, what e.g. is
applicable for GUI front-ends, where complex configuration is
varied by user interaction.

The specific request for the development of this package originally
arose from the requirement of providing an customizable Data-Model
including a View-Model for a modular data browser GUI. For the
pattern refer to the project 'data-objects'.

Constants:
    Compliance modes:
        MODE_JSON_RFC4927(0): Compliant to IETF RFC4927.
                        
        MODE_JSON_RF7951(2): Compliant to IETF RF7951.
                        
        MODE_JSON_ECMA264(10): Compliant to ECMA-264, 
            refer to 5th.ed./Chapter 15.12 The JSON Object.
            
        MODE_POINTER_RFC6901(20): Compliant to IETF RFC6901.            
            
        MODE_PATCH_RFC6902(30): Compliant to IETF RFC6902.            
            
        MODE_SCHEMA_DRAFT3(43): Compliant to IETF MODE_SCHEMA_DRAFT3.            
            
        MODE_SCHEMA_DRAFT4(44): Compliant to IETF DRAFT4.            

    types of validator:
        MODE_SCHEMA_OFF(0): Validation disabled.

        MODE_SCHEMA_DRAFT4(1): Default validator, jsonchema.validator().

        MODE_SCHEMA_DRAFT3(2): Default validator, jsonchema.MODE_SCHEMA_DRAFT3validator().

    Match criteria for node comparison:
        MATCH_INSERT(0): Common, insertion is applicable.

        MATCH_NO(1): Negates all criteria. E.g. the condition
            [MATCH_NO, MATCH_KEY] matches when the keys are
            absent.

        MATCH_KEY(2): For dicts.

        MATCH_CHLDATTR(3): For dicts and lists.

        MATCH_INDEX(4): For lists.

        MATCH_MEM(5): For dicts(value) and lists.
        
        MATCH_NEW(6): If not present create a new only, else ignore and 
            keep present untouched.

        MATCH_PRESENT(7): Check all are present, else fails.


Setting of utilized **JSON** package:
    This module uses for the syntax of JSON data either a preloaded
    module, or loads the standard module by default. Current supported
    packages are:
    
    - **json**: The standard json package of the Python distribution.
    
    - **ujson**: 'Ultra-JSON', a wrapped C implementation with 
        high-performance conversion. 
    
    The current default module is 'json'.

Setting of utilized **JSONschema** package:
    This module uses for the optional validation of the JSON data 
    the standard package 'jsonschema' only.
    
    
**REMARK**: The API design is intentionally close to the related standards,
thus some method are quite close in their functionality with resulting
few differences if at all.

"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.12'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import os,sys
version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

import termcolor
import copy
from types import NoneType

#
# Check whether the application has selected a verified JSON package
if sys.modules.get('json'):
    import json as myjson #@UnusedImport
elif sys.modules.get('ujson'):
    import ujson as myjson
else:
    import json as myjson

# for now the only one supported
import jsonschema
from jsonschema import ValidationError,SchemaError
# Constants.
MODE_JSON_RFC4927 = 0
"""The first JSON RFC. """
    
MODE_JSON_RF7951 = 2            
"""The JSON RFC by 'now'. """

MODE_JSON_ECMA264 = 10
"""The first JSON EMCMA standard."""

MODE_POINTER_RFC6901 = 20    
"""JSONPointer first IETF RFC."""
    
MODE_PATCH_RFC6902 = 30
"""JSONPatch first IETF RFC."""
    
MODE_SCHEMA_OFF = 40
"""No validation."""

MODE_SCHEMA_DRAFT3 = 43
"""The first supported JSONSchema IETF-Draft."""

MODE_SCHEMA_DRAFT4 = 44
"""The current supported JSONSchema IETF-Draft."""

MODE_SCHEMA_ON = 44
"""The current default, DRAFT4."""


# match criteria for node comparison
MATCH_INSERT = 0
"""for dicts"""

MATCH_NO = 1
"""negates the whole set"""

MATCH_KEY = 2
"""for dicts"""

MATCH_CHLDATTR = 3
"""for dicts and lists"""

MATCH_INDEX = 4
"""for lists"""

MATCH_MEM = 5
"""for dicts(value) and lists"""

MATCH_NEW = 6
"""If not present create a new, else ignore and keep present untouched."""

MATCH_PRESENT = 7
"""Check all are present, else fails."""

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

# generic exceptions for 'jsondata'
from JSONDataExceptions import JSONDataParameter,JSONDataException,JSONDataValue,JSONDataKeyError,JSONDataSourceFile,JSONDataTargetFile,JSONDataNodeType

#
# special cases of exceptions
#
class JSONDataAmbiguity(Exception):
    """ Error ambiguity of provided parameters."""
    
    def __init__(self,requested,*sources):
        if _interactive:
            s="Ambiguious input for:\n  "+str(requested)
            for sx in sources:
                s+="\n    "+str(sx)
        else:
            s="Ambiguious input for:"+str(requested)
            for sx in sources:
                s+=":"+str(sx)
        Exception.__init__(self,s)

    def __str__(self):
        return "JSONDataAmbiguity:"+self.s

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
    def __init__(self,*args,**kargs):
        """Loads and validates a JSON definition with the corresponding schema file.

        Args:
            args*: Optional position parameters, these branch_replace corresponding key
                 parameters.
                data
                
            **kargs:
                data: JSON data within memory.
                    
                    default:= None
                indent_str: Defied the indentation of 'str'.
                    
                    default:= 4
                interactive: Hints on command line call for optional change of display format. 
                    
                    default:= False
                schema: A valid in-meory JSONschema.
                    
                    default:= None
                validator: [default, draft3, draft4, on, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None
                    
                    default:= off

                printdata: branch=None
                    Pretty print resulting final data of branch.
                    
                    default:= top
                printschema: branch=None
                    Pretty print resulting schema.
                    
                    default:= top

                debug: Displays extended state data for developers.
                    Requires __debug__==True.
                verbose: Extends the amount of the display of 
                    processing data.

        Returns:
            Results in an initialized object.

        Raises:
            NameError:

            JSONDataValue:

            jsonschema.ValidationError:

            jsonschema.SchemaError:

        """
        # static final defaults

        # prep import subcall
        kimp={}

        # JSON-Syntax modes
        self.mode_json = MODE_JSON_RF7951
        self.mode_schema = MODE_SCHEMA_DRAFT4
        self.mode_pointer = MODE_POINTER_RFC6901
        self.mode_patch = MODE_PATCH_RFC6902

        self.branch = None
        self.data = None
        self.schema = None
        self.indent = 4
        self.sort_keys = False
        self.validator = MODE_SCHEMA_OFF # default validator 

        if __debug__:
            self.debug = False
        self.verbose = False

        # set display mode for errors
        global _interactive
        _interactive = kargs.get('interactive',False)

        # The internal object schema for the framework - a fixed set of files as final MODE_SCHEMA_DRAFT4.
        self.schema = kargs.get('schema',None)

        # positional parameters dominate, remaining are MODE_SCHEMA_DRAFT4
        if args:
            for i in range(0,len(args)):
                if i == 0:
                    self.data = args[i]

        #
        #*** Fetch parameters
        #
        for k,v in kargs.items():
#             if k == 'branch':
#                 self.branch = v
            if k == 'data':
                self.data = v
            elif k == 'indent_str':
                self.indent_str = v
            elif k == 'loadcached':
                self.loadcached = v
            elif k == 'requires':
                self.requires = v
            elif k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == MODE_SCHEMA_DRAFT4:
                    self.validator = MODE_SCHEMA_DRAFT4
                elif v == 'draft3' or v == MODE_SCHEMA_DRAFT3:
                    self.validator = MODE_SCHEMA_DRAFT3
                elif v == 'off' or v == MODE_SCHEMA_OFF:
                    self.validator = MODE_SCHEMA_OFF
                else:
                    raise JSONDataValue("unknown",k,str(v))
            elif k == 'verbose':
                self.verbose = v
            elif __debug__:
                if k == 'debug':
                    self.debug = v
            elif k == 'interactive':
                _interactive = v
            

        if self.verbose:
                print "VERB:JSON=          "+str(myjson.__name__)+" / "+str(myjson.__version__)
        if __debug__:
            if self.debug:
                print "DBG:JSON=           "+str(myjson.__name__)+" / "+str(myjson.__version__)
                print "DBG:self.data=    #["+str(self.schemafile)+"]#"
                print "DBG:self.schema=  #["+str(self.schema)+"]#"


        # Check data.
        if type(self.data) is NoneType:
            raise JSONDataParameter("value","data",str(self.data))

        # Validate.
        if not self.schema and self.validator != MODE_SCHEMA_OFF:
            raise JSONDataParameter("value","schema",str(self.schema))

        # INPUT-BRANCH: validate data
        if self.validator != MODE_SCHEMA_OFF:
            self.validate(self.data,self.schema,self.validator)

        if __debug__:
            if self.debug:
                print "DBG:self.pathlist=    "+str(self.pathlist)
                print "DBG:self.filelist=    "+str(self.filelist)
                print "DBG:self.filepathlist="+str(self.filepathlist)
                print "DBG:self.schemafile=  "+str(self.schemafile)
                print "DBG:self.schema=       #["+str(self.schema)+"]#"

    def __call__(self, x):
        """Evaluates the pointed value from the document.

        Args:
            x: A valid JSONPointer.

        Returns:
            The pointed value, or None.

        Raises:
            JSONPointerException
        """
        if isinstance(x,JSONPointer):
            return x.get_node_or_value(self.data)
        return JSONPointer(x).get_node_or_value(self.data)

    def __eq__(self, x):
        """Compares this JSONData.data with x.

        Args:
            x: A valid JSONData.

        Returns:
            True or False

        Raises:
            JSONDataException
        """
        if not self.data and not x : # all None is equal, 
            return True
        return JSONData.getTreeDiff(self.data, x)

    def __repr__(self):
        """Dump data.
        """
#         io = StringIO()
#         myjson.dump(self.data, io)
#         return io.getvalue()
        return repr(self.data)

    def __str__(self):
        """Dumps data by pretty print.
        """
        return myjson.dumps(self.data, indent=self.indent, sort_keys=self.sort_keys)

    def __getitem__(self,key):
        """Support of slices, for 'iterator' refer to self.__iter__.
        """
        # self[key]
        # self[i:j:k]
        # x in self
        # for x in self
        if not self.data:
            return None 
        return self.data[key] 

    def __iter__(self):
        """Provides an iterator for data.
        """
        return iter(self.data)

    def __ne__(self, x):
        """Compares this JSONData with x.

        Args:
            x: A valid JSONData.

        Returns:
            True or False

        Raises:
            JSONDataException
        """
        return not self.__eq__(x)

    def branch_add(self, targetnode, key, sourcenode):
        """Add a complete branch into a target structure of type object.

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
            targetnode := nodereference
                Target container node where the branch is to be inserted.
            
            key := key-value
                Hook for the insertion within target node.
            
            sourcenode := nodereference
                Source branch to be inserted into the target tree.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataNodeType:
            JSONDataKeyError:

        """
        ret = False
        if isinstance(targetnode,JSONPointer):
            try:
                if not key:
                    targetnode,key  = targetnode.get_node_and_child(self.data)
                else:
                    targetnode  = targetnode.get_node(self.data,False)
            except:
                # requires some more of a new path than for the node-only
                self.branch_create('',targetnode)
                if not key:
                    targetnode,key  = targetnode.get_node_and_child(self.data)
                else:
                    targetnode  = targetnode.get_node(self.data,True)

        if type(targetnode) == dict:
            if key:
                targetnode[key] = copy.deepcopy(sourcenode)
            else:
                if type(sourcenode) != dict:
                    raise JSONDataNodeType("type","targetnode/sourcenode",type(targetnode)+"/"+type(sourcenode))
                targetnode.clear()
                for k,v in sourcenode.items():
                    targetnode[k]=copy.deepcopy(v)
            return True
                    
        elif type(targetnode) == list:
            if key == '-':
                targetnode.append(copy.deepcopy(sourcenode))
                ret = True
            elif 0 <= key < len(targetnode):
                targetnode[key] = copy.deepcopy(sourcenode)
            elif type(key) is NoneType: # 0 is valid
                if type(sourcenode) != list:
                    raise JSONDataNodeType("node/keys != type:does not match:",targetnode, sourcenode)
                for k in range(0,len(targetnode)):
                    targetnode.pop()
                for v in sourcenode:
                    targetnode.append(copy.deepcopy(v))
            else:
                raise JSONDataKeyError("mismatch:node:type", 'key', key, 'key-type', type(key),'node-type',type(targetnode))
            return True
                
        else:
            raise JSONDataNodeType("type","targetnode/sourcenode",str(type(targetnode))+"/"+str(type(sourcenode)))

        return ret

    def branch_copy(self, targetnode, key, sourcenode, force=True):
        """Copies the source branch to the target node.

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
            targetnode := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
            
            sourcenode := nodereference
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
        if force: # force replace of existing
            return self.branch_add(targetnode, key, sourcenode)
        elif self.isApplicable(targetnode, key, sourcenode, [MATCH_NEW]): # only new
            return self.branch_add(targetnode, key, sourcenode)
        else: # not applicable
            return False

    def branch_create(self, targetnode, branch, value=None):
        """Creates a branch located at targetnode.

        The requested branch as created as child value of provided 
        'targetnode'. 'targetnode' is required to exist.
         
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
            targetnode := nodereference
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

        def getNewNode(keytype):
            """Fetch the required new container."""
            if keytype == '-':
                return []
            elif type(keytype) is int:
                return []
            elif type(keytype) in ( str, unicode, ):
                return {}
            elif not keytype:
                return None
            else:
                raise JSONDataKeyError("type",'keytype',str(keytype))
            
        if isinstance(branch,JSONPointer):
            
            #FIXME: iterator
            branch = branch.get_path_list()

        if not type(branch) is list:
            raise JSONDataException("value","branch",branch)

        if targetnode == '': # RFC6901 - whole document
            targetnode = self.data
        
        if type(targetnode) == dict:
            # Be aware, the special '-' could be a valid key, thus cannot be prohibited!!! 
            if type(branch[0]) not in (str,unicode,):
                raise JSONDataException("value","container/branch",str(type(targetnode))+"/"+str(type(branch[0])))

            if len(branch)>1:
                if not targetnode.get(unicode(branch[0]),False):
                    targetnode[unicode(branch[0])] = getNewNode(branch[1])
                ret = self.branch_create(targetnode[branch[0]], branch[1:], value)
            else:
                if targetnode.get(branch[0],False):
                    raise JSONDataException("exists","branch",str(branch[0]))
                ret = targetnode[unicode(branch[0])] = self.getCanonical(value)
                
        elif type(targetnode) == list:
            if type(branch[0]) in (int,) and branch[0] < len(targetnode): # see RFC6902 for '-'/append
                raise JSONDataException("exists","branch",str(branch[0]))
            elif unicode(branch[0]) == u'-': # see RFC6902 for '-'/append
                pass
            else:
                raise JSONDataException("value","targetnode/branch:"+str(type(targetnode))+"/"+str(type(branch[0])))

            if len(branch) == 1:            
                if branch[0] == '-':
                    branch[0] = len(targetnode)
                    targetnode.append(self.getCanonical(value))
                else:
                    targetnode[branch[0]] = self.getCanonical(value)
                ret = targetnode
            else:
                if branch[0] == '-':
                    branch[0] = len(targetnode)
                    targetnode.append(getNewNode(branch[1]))
                ret = self.branch_create(targetnode[branch[0]], branch[1:], value)

        else:
            raise JSONDataException("type","targetnode",str(type(targetnode)))

        return ret

    def branch_move(self, targetnode, key, sourcenode, skey, force=True, forcext=False):
        """Moves a source branch to target node.

        Moves by default only when target is not yet present. The
        parameters for 'list', 'force' enabled to overwrite, whereas 
        the parameter 'forcext' enables to move all entries and 
        extend the target items.
        
        Due to the Python specific passing of flat parameters as
        a copy of the reference without access to the actual source
        entry, these are slightly different from the 'branch_copy'
        and 'branch_add' methods modifying the target only. Therefore 
        additional source keys 'skey' are required by 'move' in order
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
            targetnode := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
            
            sourcenode := nodereference
                Source branch to be inserted into target tree.
            
            skey := key-value
                Key of the source to be moved to target node.

            force: If true present are replaced, else only 
                non-present are moved.
                
                default:=True

            forcext: If true target size will be extended when 
                required. This is applicable on 'list' only, and
                extends RFC6902. The same effect is given for 
                a 'list' by one of:
                 
                * key:='-' 

                * key:=None and skey:='-'

        Returns:
            When successful returns 'True', else returns either 
            'False', or raises an exception.

        Raises:
            JSONData:
            JSONDataKey:
            KeyError:
        
        """
        ret = False

        if type(targetnode) is dict:

            if type(skey) is NoneType: # no source key provided
                if type(key) is NoneType: # no keys provided at all, use source
                    raise JSONDataKeyError("missing","key",str(key))

                else: # use target key for both
                    targetnode[key] = sourcenode[key]
            
            else:
                if type(key) is NoneType:
                    if targetnode.get(skey):
                        if not force:
                            raise JSONDataKeyError("present","skey",str(skey))
                    targetnode[skey] = sourcenode[skey]
                else:
                    if targetnode.get(key):
                        if not force:
                            raise JSONDataKeyError("present","key",str(key))
                    targetnode[key] = sourcenode[skey]
            
            sourcenode.pop(skey)
            ret = True

        elif type(targetnode) is list:

            if type(skey) is NoneType: # no source key provided
                if type(key) is NoneType: # no keys provided at all, use source
                    raise JSONDataKeyError("missing","key",str(key))
                
                elif key == '-': # append all, due to missing 'skey'
                    if type(sourcenode) is list: # list to list
                        for v in reversed(sourcenode):
                            targetnode.append(v)
                            sourcenode.pop()
                    else: # is dict, requires 'skey'
                        raise JSONDataKeyError("type/dict","key",str(key))

                elif key < len(sourcenode): # use target key for both
                    targetnode[key] = sourcenode[key]
                    sourcenode.pop(key)

                else:
                    raise JSONDataKeyError("key",str(key))
            
            elif skey == '-':
                raise JSONDataKeyError("type","skey",str(skey))

            else:
                if type(key) is NoneType:
                    if skey < len(targetnode):
                        if force:
                            targetnode[skey] = sourcenode[skey]
                        else:
                            raise JSONDataKeyError("present","skey",str(skey))
                    elif forcext:
                        targetnode.append(sourcenode[skey])
                    else:
                        raise JSONDataKeyError("value","skey",str(skey))
                else:
                    if type(key) is int and type(skey) is int and skey < len(sourcenode):
                        if key < len(targetnode):
                            if force:
                                targetnode[key] = sourcenode[skey]
                            else:
                                raise JSONDataKeyError("present","key",str(key))
                        elif forcext:
                            targetnode.append(sourcenode[skey])
                            
                    elif key == '-':
                        targetnode.append(sourcenode[skey])
                    else: # forcext is not applicable on explicit given keys
                        raise JSONDataKeyError("value","skey",str(skey))
                sourcenode.pop(skey)

            ret = True


        if not ret:
            raise JSONDataException("type","targetnode",str(type(targetnode)))
        
        return ret

    def branch_remove(self, targetnode, key):
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
            targetnode := nodereference
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
        ret = False

        if type(targetnode) == dict:
            if not key:
                targetnode.clear()
            else:
                targetnode.pop(key)
            ret = True

        elif type(targetnode) == list:
            if type(key) is NoneType:
                [targetnode.pop() for l in range(0,len(targetnode))]
            else:
                targetnode.pop(key)
            ret = True

        if not ret:
            raise JSONDataException("type","targetnode",str(targetnode))
        
        return ret

    def branch_replace(self,targetnode, key, sourcenode):
        """Replaces the value of the target node by the copy of the source branch.

        Requires in order to RFC6902, all items to be replaced has to be
        present. Thus fails if at least one is missing.
        
        Internally the 'branch_add()' call is used with a deep copy.
        When a swallow copy is required the 'branch_move()' has to be used. 

        Args:
            targetnode := nodereference
                Target tree the branch is to be inserted.
            
            key := key-value
                Key of insertion point within target node.
                If key==None, the whole set of keys is replaced by
                the content of the 'sourcenode'.
            
            sourcenode := nodereference
                Source branch to be inserted into target tree.
            
            force: If true present are replaced, else only non-present 
                are copied.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:
        
        """
        if not self.isApplicable(targetnode, key, sourcenode, [MATCH_PRESENT]):
            return False
        return self.branch_add(targetnode, key, sourcenode)

    @classmethod
    def branch_test(cls,targetnode, value):
        """Tests match in accordance to RFC6902.

        Args:
            targetnode := a valid node
                Node to be compared with the value. Due to
                ambiguity the automated conversion is not 
                reliable, thus it has to be valid. 

            value: Expected value for the given node.
            
        Returns:
            When successful returns 'True', else returns 'False'.

        Raises:
            JSONData:
        """
        if not targetnode and not value : # all None is equal, 
            return True
        return cls.getTreeDiff(targetnode, value) # value could be a branch itself

    @classmethod
    def getTreeDiff(cls, n0, n1, difflst=None, alldifs=False, dl=0, path=''):
        """Recursive tree compare for Python trees as used for the package 'json'.
        
        Finds diff in native Python trees assembled by the standard package 'json'
        and compatible, e.g. 'ujson'.
        """
        # assure JSON strings
        if type(n0) is str:
            n0 = unicode(n0)
        if type(n1) is str:
            n1 = unicode(n1)
        if type(n0) != type(n1):
            if type(difflst) != NoneType: 
                difflst.append({'n0'+path:n0,'n1'+path:n1,'dl':dl})
            return False

        if type(n0) is list:
            if len(n0) != len(n1):
                if type(difflst) != NoneType: 
                    difflst.append({'n0'+path:n0,'n1'+path:n1,'dl':dl})
                return False

            for ni in range(0,len(n0)):
                if type(n0[ni]) in (list,dict):
                    if not cls.getTreeDiff(n0[ni],n1[ni],difflst,alldifs,dl+1,path+'['+str(ni)+']'):
                        if not alldifs:
                            return False
                elif n0[ni] != n1[ni]:
                    if type(difflst) != NoneType: 
                        _path = path + '['+str(ni)+']'
                        difflst.append({'n0'+_path:n0[ni],'n1'+_path:n1[ni],'dl':dl})
                    if not alldifs:
                        return False

        elif type(n0) is dict:
            if len(n0.keys()) != len(n1.keys()):
                if type(difflst) != NoneType: 
                    difflst.append({'n0'+path:n0,'n1'+path:n1,'dl':dl})
                return False

            for ni,v in n0.items():
                if n1.get(ni):
                    if type(v) in (list,dict):
                        if not cls.getTreeDiff(v,n1[ni],difflst,alldifs,dl+1,path+'['+str(ni)+']'):
                            if not alldifs:
                                return False
                    else:
                        if v != n1[ni]:
                            if type(difflst) != NoneType:
                                _path = path + '['+str(ni)+']'
                                difflst.append({ 'n0'+_path:n0[ni],'n1'+_path:n1[ni],'dl':dl})
                            if not alldifs:
                                return False
                else:
                    if type(difflst) != NoneType: 
                        _path = path +'['+str(ni)+']'
                        difflst.append({'n0'+_path:n0[ni],'n1'+path:n1,'dl':dl})
                    if not alldifs:
                        return False

        else: # invalid types may have been eliminated already
            if n0 == n1:
                return True
            if type(difflst) != NoneType: 
                difflst.append({'n0'+path:n0,'n1'+path:n1,'dl':dl})
            return False
        if type(difflst) != NoneType: 
            return len(difflst) == 0
        return True

    FIRST = 1
    """First match only."""
    
    ALL = 3
    """All matches."""

    @classmethod
    def getPointerPath(cls,node,base,restype=FIRST):
        """Converts a node address into the corresponding pointer path.
        
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
        
        kl = 0
        kd = None
        
        
        if type(base) is list: # first layer - list of elements
            kl = 0
            if id(node) == id(base): # top node
                res.append([kl])
            else:
                for sx in base:
                    if id(node) == id(sx):
                        s = spath[:]
                        s.append(kl)
                        res.append(s)
                        
                    elif type(sx) in (dict,list):
                        sublst = cls.getPointerPath(node,sx,restype)
                        if sublst:
                            for slx in sublst:
                                s = spath[:]
                                s.append(kl)
                                s.extend(slx)
                                res.append(s)
                    kl += 1

        elif type(base) is dict: # first layer - dict of elements
            if id(node) == id(base): # top node
                res.append([''])
            else:
                for k,v in base.items():
                    if id(node) == id(v):
                        spath.append(k)
                        res.append(spath)
                        continue
                    elif type(v) in (list,dict):
                        sublst = cls.getPointerPath(node,v,restype)
                        if sublst:
                            for slx in sublst:
                                if slx:
                                    s = spath[:]
                                    s.append(k)
                                    s.extend(slx)
                                    res.append(s)

        #FIXME: for performance
        if res and restype == JSONData.FIRST:
            return [res[0]]
        return res

    def getCanonical(self,value):
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
        if type(value) in (dict,list): # assumes a 'json' package type node
            return value
        elif type(value) in ( int, float, ): # assume a 'JSON' RFC7159 int, float
            return value
        elif type(value) in ( str, unicode, ): # assume a 'JSON' RFC7159 string
            return unicode(value)
        elif isinstance(value,JSONPointer): # assume the pointed value
            return value.get_node_or_value(self.data)
        elif not value:
            return None
        else:
            raise JSONDataException("type","value",str(value))
    
    def isApplicable(self, targetnode, key, branch, matchcondition=None, **kargs):
        """ Checks applicability by validation of provided match criteria.

        The contained data in 'datafile' could be either the initial data
        tree, or a new branch defined by a fresh tree structure. The
        'targetnode' defines the parent container where the new branch has
        to be hooked-in.

        Args:
            targetnode:
                Target container hook for the inclusion of the loaded branch.
                The branch is treated as a child-branch, hooked into the
                provided container 'targetnode'.
            branch:
                Branch to be imported into the target container. The branch
                is treated as a child-branch.
            matchcondition:
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
            **kargs:
                childattrlist: A list of user defined child attributes which
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

        #
        #*** Fetch parameters
        #
        if not matchcondition:
            return True
        childattrlist = None
        _matchcondition = []
        for v in matchcondition:
            #For now just passed through to self.isApplicable()
            if v == 'key' or v == MATCH_KEY:
                _matchcondition.append(MATCH_KEY)
            elif v == 'no' or v == MATCH_NO:
                _matchcondition.append(MATCH_NO)
            elif v == 'child_attr_list' or v == MATCH_CHLDATTR:
                _matchcondition.append(MATCH_CHLDATTR)
            elif v == 'index' or v == MATCH_INDEX:
                _matchcondition.append(MATCH_INDEX)
            elif v == 'mem' or v == MATCH_MEM:
                _matchcondition.append(MATCH_MEM)
            elif v == 'new' or v == MATCH_NEW:
                _matchcondition.append(MATCH_NEW)
            elif v == 'present' or v == MATCH_PRESENT:
                _matchcondition.append(MATCH_PRESENT)
            else:
                raise JSONDataValue("value","matchcondition",str(v))
        for k,v in kargs.items():
            if k == 'childattrlist': # provides a list of child attributes
                childattrlist = v
#TODO:
#             elif k == 'schema':
#                 sval = v

        retOK = True # return in case of no-defined-condition or no-failing-condition

        if isinstance(targetnode, JSONData):
            targetnode = targetnode.data 
        if isinstance(branch, JSONData):
            branch = branch.data 

        # The first mandatory requirement definition if the type compatibility
        # of the plug and the plugin-element.
        if type(key) is NoneType and type(targetnode) != type(branch):
            raise JSONDataException("type","targetnode",str(type(targetnode)))

        # set default
        if not _matchcondition:
            _matchcondition = [MATCH_INSERT]

        if MATCH_NO in _matchcondition:
            retFailed = True
            retOK = False
        else:
            retFailed = False
            retOK = True

        for m in _matchcondition:
            if m == MATCH_NO: # handles multiple, does not need alist.branch_remove()
                continue
            elif m == MATCH_INSERT:
                if not type(targetnode) in (dict,list):
                    raise JSONDataException("type","targetnode",str(type(targetnode)))
            elif m == MATCH_KEY:
                if type(targetnode) != dict:
                    raise JSONDataException("type","targetnode",str(type(targetnode)))
                for k in branch.keys():
                    if not targetnode.get(k):
                        return retFailed
            elif m == MATCH_CHLDATTR:
                if not type(targetnode) in (list,dict):
                    raise JSONDataException("type","targetnode",str(type(targetnode)))
                if childattrlist != None:
                    if type(branch) == dict:
                        for ca in childattrlist:
                            if not targetnode.get(ca):
                                return retFailed
                    elif type(branch) == list:
                        for l in targetnode:
                            if not type(l) is dict:
                                raise JSONDataException("type","targetnode",str(type(targetnode)))
                            for ca in childattrlist:
                                if not type(ca) is dict:
                                    raise JSONDataException("type","targetnode",str(type(targetnode)))
                                if not l.get(ca):
                                    return retFailed
                    else:
                        raise JSONDataException("type","targetnode",str(type(targetnode)))
            elif m == MATCH_INDEX:
                if type(targetnode) != list:
                    raise JSONDataException("type","targetnode",str(type(targetnode)))
                if len(targetnode) > len(branch):
                    return retFailed
            elif m == MATCH_NEW:
                if type(targetnode) == list:
                    if key == '-':
                        pass
                    elif not type(key) is NoneType:
                        if 0 <= key < len(targetnode):
                            if targetnode[key]:
                                return retFailed
                        if len(targetnode) > len(branch):
                            return retFailed
                    else:
                        if type(branch) is list:
                            if targetnode:
                                return retFailed

                elif type(targetnode) == dict:
                    if key:
                        if not targetnode.get(key,None):
                            return retFailed
                    else:
                        if type(branch) is dict:
                            if targetnode:
                                return retFailed
                        
            elif m == MATCH_PRESENT:
                if type(targetnode) == list:
                    if not type(key) is NoneType:
                        if 0 <= key < len(targetnode):
                            return retOK
                        else:
                            return retFailed
                    else:
                        return retFailed

                elif type(targetnode) == dict:
                    if key:
                        if not targetnode.get(key,None):
                            return retFailed
                        return retOK
                    else:
                        return retFailed

            elif m == MATCH_MEM:
                if type(targetnode) == list:
                    if type(targetnode) != type(branch):
                        raise JSONDataException("type","targetnode",str(type(targetnode)))
                    for l in branch:
                        try:
                            if not targetnode.index(l):
                                return retFailed
                        except:
                            return retFailed
                elif type(targetnode) == dict:
                    if type(targetnode) == type(branch):
                        raise JSONDataException("type","targetnode",str(type(targetnode)))
                    for k,v in branch.items():
                        if id(v) != id(targetnode.get(k)):
                            return retFailed
                else:
                    raise JSONDataException("type","targetnode",str(type(targetnode)))
            elif _matchcondition:
                raise JSONDataException("type","targetnode",str(type(targetnode)))
        return retOK

    def pop(self,key):
        """Transparently passes the 'pop()' call to 'self.data'."""
        return self.data.pop(key)
    
    def printData(self, pretty=True, **kargs):
        """Prints structured data.

        Args:
            pretty: Activates pretty printer for treeview, else flat.

            sourcefile: Loads data from 'sourcefile' into 'source'.
                
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
        source = kargs.get('source',None)
        sourcefile = kargs.get('sourcefile',None)
        if sourcefile and source:
            raise JSONDataAmbiguity('sourcefile/source',
                "sourcefile="+str(sourcefile),
                "source="+str(source)
                )
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.data # yes, almost the same...

        if pretty:
            print myjson.dumps(source,indent=self.indent)
        else:
            print myjson.dumps(source)

    def printSchema(self, pretty=True, **kargs):
        """Prints structured schema.

        Args:
            pretty: Activates pretty printer for treeview, else flat.

            sourcefile: Loads schema from 'sourcefile' into 'source'.
                
                default:=None
            source: Prints schema within 'source'.
                
                default:=self.schema

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataAmbiguity:

            forwarded from 'json'

        """
        source = kargs.get('source',None)
        sourcefile = kargs.get('sourcefile',None)
        if sourcefile and source:
            raise JSONDataAmbiguity('sourcefile/source',
                "sourcefile="+str(sourcefile),
                "source="+str(source)
                )
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.schema # yes, almost the same...

        if pretty:
            print myjson.dumps(source,indent=self.indent)
        else:
            print myjson.dumps(source)

    def set_schema(self,schemafile=None, targetnode=None, **kargs):
        """Sets schema or inserts a new branch into the current assigned schema.

        The main schema(targetnode==None) is the schema related to the current
        instance. Additional branches could be added by importing the specific
        schema definitions into the main schema. These could either kept
        volatile as a temporary runtime extension, or stored into a new schema
        file in order as extension of the original for later combined reuse.

        Args:
            schemafile:
                JSON-Schema filename for validation of the subtree/branch.
                See also **kargs['schema'].
            targetnode:
                Target container hook for the inclusion of the loaded branch.
            **kargs:
                schema:
                    In-memory JSON-Schema as an alternative to schemafile.
                    When provided the 'schemafile' is ignored.
                    
                    default:=None
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    
                    default:= validate
                persistent:
                    Stores the 'schema' persistently into 'schemafile' after
                    completion of update including addition of branches.
                    Requires valid 'schemafile'.
                    
                    default:=False

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:

            JSONData:

            JSONDataSourceFile:

            JSONDataValue:

        """
        if __debug__:
            if self.debug:
                print "DBG:set_schema:schemafile="+str(schemafile)

        #
        #*** Fetch parameters
        #
        datafile = None
        validator = self.validator # use class settings as MODE_SCHEMA_DRAFT4
        persistent = False
        schema = None
        for k,v in kargs.items():
            if k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == MODE_SCHEMA_DRAFT4:
                    validator = MODE_SCHEMA_DRAFT4
                elif v == 'draft3' or v == MODE_SCHEMA_DRAFT3:
                    validator = MODE_SCHEMA_DRAFT3
                elif v == 'off' or v == MODE_SCHEMA_OFF:
                    validator = MODE_SCHEMA_OFF
                else:
                    raise JSONDataValue("unknown",k,str(v))
            elif k == 'schema':
                schema = v
            elif k == 'datafile':
                datafile = v
            elif k == 'persistent':
                persistent = v

        if schemafile != None: # change filename
            self.schemafile = schemafile
        elif self.schemafile != None: # use present
            schemafile = self.schemafile
        elif datafile != None: # derive coallocated from config
            schemafile = os.path.splitext(self.datafile)[0]+'.jsd'
            if not os.path.isfile(schemafile):
                schemafile = None
            else:
                self.schemafile = schemafile

        if not schemafile:
            if persistent: # persistence requires storage
                raise JSONDataTargetFile("open","JSONSchemaFilename",schemafile)

        # schema for validation
        if schema: # use loaded
            pass

        elif schemafile: # load from file
            schemafile = os.path.abspath(schemafile)
            self.schemafile = schemafile
            if not os.path.isfile(schemafile):
                raise JSONDataSourceFile("open","schemafile",str(schemafile))
            with open(schemafile) as schema_file:
                schema = myjson.load(schema_file)
            if schema == None:
                raise JSONDataSourceFile("read","schemafile",str(schemafile))

        else: # missing at all
            raise JSONDataSourceFile("open","schemafile",str(schemafile))
            pass

        #
        # manage new branch data
        #
        if not targetnode:
            self.schema = schema

        else: # data history present, so decide how to handle

            # the container hook has to match for insertion-
            if type(targetnode) != type(schema):
                raise JSONDataException("type","target!=branch",str(type(targetnode))+"!="+str(type(schema)))
        
            self.branch_add(targetnode,schema)

        return schema != None

    def validate(self,data,schema,validator=None):
        """Validate data with schema by selected validator.

        Args:
            data:
                JSON-Data.
            schema:
                JSON-Schema for validation.
            validator:
                Validator to be applied, current supported:
                
                schema:
                    In-memory JSON-Schema as an alternative to schemafile.
                    When provided the 'schemafile' is ignored.
                    
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
        
        if validator == MODE_SCHEMA_DRAFT4:
            if self.verbose:
                print "VERB:Validate: draft4"
            try:
                jsonschema.validate(data, schema)
                
            #FIXME:
            
            except ValidationError as e:
                print "ValidationError"
                print e
                print "#---"
                print dir(e)
                print "#---"
                print str(e)
                print "#---"
                print repr(e)
                print "#---"
                raise
            except SchemaError as e:
                print "SchemaError"
                print e
                print "#---"
                print dir(e)
                print "#---"
                print str(e)
                print "#---"
                print repr(e)
                print "#---"
                print "path:"+str(e.path)
                print "schema_path:"+str(e.schema_path)
                print "#---"
                raise
            
        elif validator == MODE_SCHEMA_DRAFT3:
            if self.verbose:
                print "VERB:Validate: draft3"
            jsonschema.Draft3Validator(data, schema)
        elif validator != MODE_SCHEMA_OFF:
            raise JSONDataValue("unknown","validator",str(validator))
        
        pass

   
from jsondata.JSONPointer import JSONPointer 
# avoid nested recursion problems
