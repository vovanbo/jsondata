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
    branchoperations:
        BRANCH_REPLACE_SET(0): Replace all previous loaded branches.

        BRANCH_SUPERPOSE(1): Creates, or maps onto present by replacing.

        BRANCH_ADD(2): Creates, does not branch_replace.

        BRANCH_REMOVE(3): Deletes.

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

                                      
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.4'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import os,sys
from jsondata.JSONPointer import JSONPointer 
version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

try:
    from urllib import unquote
    from itertools import izip
    #str = unicode
except ImportError: # Python 3
    from urllib.parse import unquote
    izip = zip

import re
import json, jsonschema
from StringIO import StringIO

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
"""The curren supported JSONSchema IETF-Draft."""


# Choices for branch operations
BRANCH_REPLACE = 0 
"""replaces the single branches."""

BRANCH_REPLACE_SET = 1 
"""replaces the complete set of branches."""

BRANCH_SUPERPOSE = 2
"""drops-in the child nodes of the source into the target, superposes complete branches only"""

BRANCH_SUPERPOSE_ITEMS = 3
"""drops-in the child nodes of the source into the target, superposes each item when present"""

BRANCH_ADD = 4
"""similar to branch_add, but does not branch_replace existing"""

BRANCH_REMOVE = 5
"""removes a node"""


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


# Sets display for inetractive JSON/JSONschema design.
_interactive = False

class JSONDataSerializerError(Exception):
    """JSONData Error."""
    def __init__(self,err):
        s="ERROR:"+str(err)
        Exception.__init__(self,s)

class JSONDataSerializerErrorTargetFile(Exception):
    """JSONData Error on writing a file."""
    def __init__(self,targetname):
        s="Failed on target file:"+str(targetname)
        Exception.__init__(self,s)

class JSONDataSerializerErrorTargetFileReason(Exception):
    """JSONData Error on writing a file with the reason from the original exception."""
    def __init__(self,targetname,reason):
        if _interactive:
            s="Failed on target file:\n  "+str(targetname)+":"+str(reason)
        else:
            s="Failed on target file:"+str(targetname)+":"+str(reason)
        Exception.__init__(self,s)

class JSONDataSerializerErrorSourceFile(Exception):
    """JSONData Error on reading a source file."""
    def __init__(self,sourcename,sources):
        if _interactive:
            s="Missing source file:\n  "+str(sourcename)+":"+str(sources)
        else:
            s="Missing source file:"+str(sourcename)+":"+str(sources)
        Exception.__init__(self,s)

class JSONDataSerializerErrorSourceFileReason(Exception):
    """JSONData Error on reading a source file with the reason from the original exception."""
    def __init__(self,sourcename,sources,reason):
        if _interactive:
            s="Missing source file:\n  "+str(sourcename)+":"+str(sources)+":"+str(reason)
        else:
            s="Missing source file:"+str(sourcename)+":"+str(sources)+":"+str(reason)
        Exception.__init__(self,s)

class JSONDataSerializerErrorSourceFromList(Exception):
    """JSONData Error on search for a source file by a provided list."""
    def __init__(self,sourcename,searched):
        if _interactive:
            s="Missing source file:\n  "+str(sourcename)+":searched:"+str(searched)
        else:
            s="Missing source file:"+str(sourcename)+":searched:"+str(searched)
        Exception.__init__(self,s)

class JSONDataSerializerErrorSourceFromAll(Exception):
    """JSONData Error on resolving a source file name from available parameters."""
    def __init__(self,sourcename,sources,*searched):
        if _interactive:
            s="Missing source filelist:\n  "+str(sourcename)+":"+str(sources)+"\n  pathlist:"
            for sx in searched:
                s += "\n    "+str(sx)
        else:
            s="Missing source filelist:"+str(sourcename)+":"+str(sources)+":pathlist"
            for sx in searched:
                s += ":"+str(sx)
        Exception.__init__(self,s)

class JSONDataSerializerErrorAmbiguity(Exception):
    """JSONData Error ambiguity of provided parameters."""
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

class JSONDataSerializerErrorAttribute(Exception):
    """JSONData Error on unknown and/or missing attribute."""
    def __init__(self,requested):
        s="Attribute unknown:"+str(requested)
        Exception.__init__(self,s)

class JSONDataSerializerErrorAttributeValue(Exception):
    """JSONData Error on unknown and/or missing attribute value."""
    def __init__(self,requested,val):
        s="Attribute value:"+str(requested)+":"+str(val)
        Exception.__init__(self,s)

class JSONDataSerializerErrorValue(Exception):
    """JSONData Error on a value."""
    def __init__(self,requested,val):
        s="Value:"+str(requested)+":"+str(val)
        Exception.__init__(self,s)
    
class JSONDataSerializer:
    """ Representation of a JSON based object data tree.
    
    This class provides for the handling of the in-memory data
    by the main hooks 'data', and 'schema'. This includes generic 
    methods for the advanced management of arbitrary 'branches'
    in extension to RCF6902, and additional methods strictly 
    compliant to RFC6902.

    Due to the pure in-memory support and addressing by the enclosed 
    module JSONPointer for RFC6901 compliant addressing by in memory
    caching, the JSONDataSerializer may outperform designs based on 
    operation on the native JSON representation.

    Attributes:
        data: The data tree of JSON based objects provided
            by the module 'json'.
        schema: The validator for 'data' provided by 
            the module 'jsonschema'.

    """
    def __init__(self,appname,*args,**kargs):
        """ Loads and validates a JSON definition with the corresponding schema file.

        Args:
            appname: Name of the application

            args*: Optional position parameters, these branch_replace corresponding key
                 parameters.
                filelist, pathlist, filepathlist, schemafile
            **kargs:
                branchoperations: [branch_add_only, branch_remove, branch_replace-set, branch_add, ]
                    Defines the behavior for for the load of data when redundant
                    tree parts exist.
                        set-branch_replace: BRANCH_REPLACE_SET(0)
                            Replace all previous loaded branches.
                        branch_add: BRANCH_SUPERPOSE(1)
                            Creates, or maps onto present by replacing.
                        branch_add_only: BRANCH_ADD(2)
                            Creates, does not branch_replace.
                        branch_remove: BRANCH_REMOVE(3)
                            Deletes.
                    default:= branch_replace-object
                datafile: Filepathname of JSON data file, when provided a further
                    search by pathlist, filelist, and filepathlist is suppressed.
                    Therefore it has to be a valid filepathname.
                    default:= <appname>.json
                filelist: List of valid filenames.
                    default:= <appname>.json
                filepathlist: List of filepathnames. These are not prefixed by search
                    path components, but made absolute.
                    default:= []
                filepriority: [firstonly, lastonly, all]
                    Defines the handling of multiple occurrences of a filename at varios
                    positions. This option thus may only be altered in conjunction with 'pathlist'.
                    default:= all
                indent_str: Defied the indentation of 'str'.
                    default:= 4
                loadcached: Caching of load for JSON data files.
                    Loads either completely into cache before transferring to
                    production entries, or immediately into production parameters,
                    which may take an effect on the remaining parameters to be loaded.
                    default:= False
                nodefaultpath: Ignores the default paths, the exception is the
                    base configuration, which still is searched within the default
                    paths exclusively.
                    default:= False
                nosubdata: Supresses the load of sub-data files.
                    default:= False
                pathlist: List of pathnames for search of a valid filename.
                    Either a PATH like string, or a list of single paths.
                    default:= ../dirname(__file__)/etc/:dirname(__file__)/:/etc/:$HOME/etc/
                requires: [all, base, one]
                    Defines how to handle missing or invalid files.
                    default:= all
                schema: A valid in-meory JSONschema.
                    default:= None
                schemafile: Filepathname of JSONschema file.
                    default:= <appname>.jsd
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator, off=None
                    default:= validate

                printdata: branch=None
                    Pretty print resulting final data of branch.
                    default:= top
                printschema: branch=None
                    Pretty print resulting schema.
                    default:= top

                debug: Displays extended state data for developers.
                    Requires __debug__==True.
                verbose: Extends the amount of the display of processing data.

        Returns:
            Results in an initialized object.

        Raises:
            NameError:

            JSONDataSerializerErrorSourceFile:

            JSONDataSerializerErrorSourceFromList:

            JSONDataSerializerErrorAmbiguity:

            JSONDataSerializerErrorAttribute:

            JSONDataSerializerErrorAttributeValue:


            jsonschema.ValidationError:

            jsonschema.SchemaError:

        """
        # set display mode for errors
        _interactive = kargs.get('interactive',False)

        afile=os.path.abspath(str(__file__))

        # JSON-Syntax modes
        self.mode_json = MODE_JSON_RF7951
        self.mode_schema = MODE_SCHEMA_DRAFT4
        self.mode_pointer = MODE_POINTER_RFC6901
        self.mode_patch = MODE_PATCH_RFC6902

        # The internal object schema for the framework - a fixed set of files as final MODE_SCHEMA_DRAFT4.
        self.schemafile = kargs.get('schemafile',None)
        self.schema = kargs.get('schema',None)
        if self.schema and self.schemafile:
            # When a schema/schema file is provided, it is the only and one
            # for the top-level,
            raise JSONDataSerializerErrorAmbiguity('schemafile/schema',
                "schemafile="+str(self.schemafile),
                "schema="+str(self.schema)
                )

        self.nodefaultpath = kargs.get('nodefaultpath',False)

        self.pathlist = kargs.get('pathlist','')

        self.filelist = kargs.get('filelist',None)
        if not self.filelist:
            self.filelist = [ appname+'.json', ]

        self.filepathlist = kargs.get('filepathlist',[])

        self.branch = None
        self.branchoperations = BRANCH_SUPERPOSE
        self.data = None
        self.schema = None
        self.nodefaultpath = False
        self.nodesubdata = False
        self.requires = False
        self.indent = 4
        self.validator = MODE_SCHEMA_DRAFT4

        # Either provided explicitly, or for search.
        self.datafile = None

        printschema = False
        printdata = False

        global _interactive
        
        if __debug__:
            self.debug = False
        self.verbose = False

        #
        #*** Fetch parameters
        #
        for k,v in kargs.items():
            if k == 'branch':
                self.branch = v
            elif k == 'branchoperations':
                if v == 'branch_replace-set' or v == BRANCH_REPLACE_SET:
                    self.branchoperations = BRANCH_REPLACE_SET
                elif v == 'branch_replace' or v == BRANCH_REPLACE:
                    self.branchoperations = BRANCH_REPLACE
                elif v == 'branch_add' or v == BRANCH_SUPERPOSE:
                    self.branchoperations = BRANCH_SUPERPOSE
                elif v == 'branch_add_only' or v == BRANCH_ADD:
                    self.branchoperations = BRANCH_ADD
                elif v == 'branch_remove' or v == BRANCH_REMOVE:
                    self.branchoperations = BRANCH_REMOVE
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'datafile':
                self.datafile = v
            elif k == 'filepathlist':
                self.filepathlist = v
            elif k == 'filepriority':
                self.filepriority = v
            elif k == 'indent_str':
                self.indent_str = v
            elif k == 'loadcached':
                self.loadcached = v
            elif k == 'nodefaultpath':
                self.nodefaultpath = v
            elif k == 'nodesubdata':
                self.nodesubdata = v
            elif k == 'printdata':
                printdata = v
            elif k == 'printschema':
                printschema = v
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
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'verbose':
                self.verbose = v
            elif __debug__:
                if k == 'debug':
                    self.debug = v
            elif k == 'interactive':
                _interactive = v
                
        # positional parameters dominate, remaining are MODE_SCHEMA_DRAFT4
        if args:
            for i in range(0,len(args)):
                if i == 0:
                    self.filelist = args[i]
                elif i == 1:
                    self.pathlist = args[i]
                elif i == 2:
                    self.filepathlist = args[i]
                elif i == 3:
                    self.schemafile = args[i]
                else:
                    raise JSONDataSerializerErrorAttributeValue(("args["+str(i)+"]",str(args)))

        if __debug__:
            if self.debug:
                print "DBG:self.pathlist=    "+str(self.pathlist)
                print "DBG:self.filelist=    "+str(self.filelist)
                print "DBG:self.filepathlist="+str(self.filepathlist)
                print "DBG:self.schemafile=  "+str(self.schemafile)
                print "DBG:self.schema=       #["+str(self.schema)+"]#"

        if type(self.pathlist) == list: # a list of single-paths
            if not self.nodefaultpath:
                # Fixed set of data files as final default.
                self.pathlist.extend(
                    [os.path.dirname(afile)+os.sep+'etc'+os.sep+appname+os.sep,
                    os.pathsep+os.sep+'etc'+os.sep,
                    os.pathsep+"$HOME"+os.sep+'etc'+os.sep])

            # expand all
            self.pathlist = [os.path.expandvars(os.path.expanduser(p)) for p in self.pathlist]

            #parts = [part.branch_replace('~', '~0') for part in self.parts]

        else: # a PATH like variable, so do it at once
            if not self.nodefaultpath:
                # Fixed set of data files as the final default.
                self.pathlist += os.path.dirname(afile)+os.sep+'etc'+os.sep+appname+os.sep+os.pathsep+os.sep+'etc'+os.sep+os.pathsep+"$HOME"+os.sep+'etc'+os.sep
            self.pathlist  = os.path.expandvars(os.path.expanduser(self.pathlist)).split(os.pathsep)
        
        # canonical
        self.pathlist = [os.path.realpath(os.path.abspath(p))+os.sep for p in self.pathlist]

        if not self.datafile: # No explicit given
            if self.filelist:
                for f in self.filelist:
                    if os.path.isabs(f):
                        self.filepathlist.append(f)
                        self.filelist.remove(f)
                    else:
                        for p in self.pathlist:
                            fx=p+os.sep+f
                            if os.path.isfile(fx):
                                self.filepathlist.append(fx)
                                if f in self.filelist: # could occur under multiple paths
                                    self.filelist.remove(f)

        elif not os.path.isfile(self.datafile): # a provided datafile has to exist
            raise JSONDataSerializerErrorSourceFile("datafile",str(self.datafile))

        if not self.filepathlist:
            if not self.datafile:
                raise JSONDataSerializerErrorSourceFromAll("datafile",
                    str(self.filelist), self.pathlist)

        # Check whether validation is requested.
        # If so, do a last trial for plausible construction.
        if not self.schema and self.validator != MODE_SCHEMA_OFF:
            # require schema for validation, no schema provided, now-than...
            if not self.schemafile: # do we have a file
                if self.datafile:
                    if os.path.isfile(os.path.splitext(self.datafile)[0]+'.jsd'): # coallocated pair - datafile+schemafile
                        self.schemafile = os.path.splitext(self.datafile)[0]+'.jsd'
                elif self.filepathlist: # search, use the first found
                    for f in self.filepathlist:
                        if os.path.isfile(f) and os.path.isfile(os.path.splitext(f)[0]+".jsd"):
                            self.schemafile = os.path.splitext(f)[0]+".jsd"
                            break # just use the first valid-pair
                        raise JSONDataSerializerErrorSourceFile("datafile",str(self.filepathlist))
                else:
                    raise JSONDataSerializerErrorSourceFromAll("datafile",
                        str(self.filelist), self.pathlist)

            # when defined => has to be present
            if self.schemafile and not os.path.isfile(self.schemafile):
                raise JSONDataSerializerErrorSourceFile("schemafile",str(self.schemafile))

            # initialize schema
            kargs['schemafile'] = self.schemafile
            self.set_schema(**kargs)

        if __debug__:
            if self.debug:
                print "DBG:self.pathlist=    "+str(self.pathlist)
                print "DBG:self.filelist=    "+str(self.filelist)
                print "DBG:self.filepathlist="+str(self.filepathlist)
                print "DBG:self.schemafile=  "+str(self.schemafile)
                print "DBG:self.schema=       #["+str(self.schema)+"]#"

        #
        # load data, therefore search data files within pathlist
        #
        confok=False
        onenok = False
        kx={'branchoperations':self.branchoperations}
        if not self.datafile: # No explicit given
            if self.filepathlist:
                for f in self.filepathlist:
                    if self.json_import(f,self.schemafile,self.branch,**kx):
                        confok=True
                    else:
                        onenok = True

                if not confok: # base loaded only
                    if not self.requires: # there is a rule
                        if self.requires == 'base': # is mandatory, reaching this means is OK
                            pass
                        else:
                            raise JSONDataSerializerErrorSourceFromAll("datafiles",
                                str(self.filepathlist),str(self.filelist),str(self.pathlist),
                                )

                else: # at least one application configuration loaded
                    if self.requires != False: # there is a rule
                        if self.requires == 'all': # no exeception allowed
                            if onenok: # one has failed
                                raise JSONDataSerializerErrorSourceFromAll("datafiles",
                                    str(self.filepathlist),str(self.filelist),str(self.pathlist),
                                    )
                        elif self.requires == 'base': # is mandatory, reaching this means is OK
                            pass
                        elif self.requires == 'one': # reaching this means is OK
                            pass

        else:
            if os.path.exists(self.datafile):
                self.json_import(self.datafile,self.schemafile,self.branch,**kx)

        # display data to stdout
        if printschema:
            self.printSchema()
        if printdata:
            self.printData()

    def __repr__(self):
        """Dump data.
        """
#         io = StringIO()
#         json.dump(self.data, io)
#         return io.getvalue()
        return repr(self.data)

    def __str__(self):
        """Dumps data by pretty print.
        """
        return json.dumps(self.data, indent=self.indent)

    def branch_add_only(self, targetnode, branch, matchcondition=None):
        """Adds a branch into a target structure.

        The present previous values are kept untouched, non-existent
        nodes are added.
        
        Args:
            targetnode: Target tree where the source is to be inserted.

            branch: Source branch to be inserted into target tree.

            matchcondition: Defines the condition for applicability
                of the branch_add_only method. For the provided values refer to
                the call 'isApplicable'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            JSONDataSerializerError:

        """
        ret = True
        if type(branch) == dict:

            # branch_add_only does not branch_replace, just adds non-present
            if not matchcondition:
                matchcondition = [MATCH_NO,MATCH_KEY]
            else:
                matchcondition.append(MATCH_NO)

            for k,v in branch.items():
                if self.isApplicable(targetnode, {k:v}, matchcondition):
                    targetnode[k] = v
                else:
                    ret = False
        elif type(branch) == list:
            for v in branch:
                if self.isApplicable(targetnode, [v], matchcondition):
                    targetnode.append(v)
                else:
                    ret = False
        else:
            raise JSONDataSerializerError("Type not supported:type="+str(branch))
        return ret

    def branch_add(self, targetnode, branch, matchcondition=None):
        """Superposes a complete branch into a target structure of type object.

        Present previous branches are replaced, non-existent
        branches are added.

        Args:
            target: Target tree the branch is to be inserted.

            branch: Source branch to be inserted into target tree.

            matchcondition: Defines the condition for applicability
                of the super positioning at the swallow level of
                immediate child-nodes. For the provided values refer
                to the call 'isApplicable'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Partial superposition is by definition success.

        Raises:
            JSONDataSerializerError:

        """
        ret = True

        if type(targetnode) == dict:
            for k,v in branch.items():
                # the container hook has to match for insertion
                if targetnode.get(k) and type(targetnode.get(k)) != type(v):
                    raise JSONDataSerializerError("Type-Mismatch:target="+str(type(targetnode))+" != branch"+str(type(branch)))
                if self.isApplicable(targetnode, {k:v}, matchcondition):
                    targetnode[k] = v
        elif type(targetnode) == list:
            for v in branch:
                if self.isApplicable(targetnode[k], [v], matchcondition):
                    targetnode.append(v)
        elif isinstance(targetnode,JSONPointer):
            x = targetnode.get_node(self.data,True) 
            ret = self.branch_add(x, branch, matchcondition)

            #= branch
            
        else:
            raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))

        return ret

    def branch_copy(self,sourcenode,targetnode,force=False,matchcondition=None):
        """Copies the source branch to the target node.

        Args:
            targetnode: Target tree the branch is to be inserted.

            sourcenode: Source branch to be inserted into target tree.

            force: If true present are replaced, else only non-present are copied.

            matchcondition: Defines the condition for applicability
                of the super positioning at the swallow level of
                immediate child-nodes. For the provided values refer
                to the call 'isApplicable'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Partial superposition is by definition success.

        Raises:
            JSONDataSerializerError:
        
        """
        if force:
            return self.branch_add(targetnode, sourcenode,matchcondition)
        else:
            return self.branch_add_only(targetnode, sourcenode,matchcondition)
        pass

    def branch_create(self,targetnode,branch,value=None):
        """Creates a branch located at targetnode.

        The requested branch as created as child value of provided 'targetnode'.
        'targetnode' is required to exist.
         
        **REMARK**: Current version relies for the created nodes on the
            content type of the key(str,unicode)/index(int), later 
            versions may use a provided schema.
  
        Args:
            targetnode: Base node for the insertion of branch.
                Supported input types are:
                An absolute pointer address path within current document.

                    JSONPointer: RFC6901 class representation.
                    <RFC6901-string>: A string in accordance 
                        to RFC6901.
                    <list-of-bath-components>: A list representation 
                        of a pointer path in accordance to RFC6901.
                    <node>: A node within a data tree based on the
                        package 'json'.

            branch: New branch to be inserted into target tree.
                A Pointer address path relative to the targetnode. 
    
                Supported input types are:
                    JSONPointer: RFC6901 class representation. 
                    <RFC6901-string>: A string in accordance 
                        to RFC6901.
                    <list-of-bath-components>: A list representation 
                        of a pointer path in accordance to RFC6901.
                    <node>: A node within a data tree based on the
                        package 'json'.

                **REMARK**: The address has to begin with 
                    a '/' in accordance to RFC6901.

            value: Optional value for the leaf.
            
        Returns:
            When successful returns the leaf node, else returns either 'False',
            or raises an exception.

        Raises:
            JSONDataSerializerError:

        """
        ret = targetnode

        def getNewNode(key):
            if key == '-':
                return []
            elif type(key) is int:
                return []
            elif type(key) in ( str, unicode, ):
                return {}
            elif not key:
                return None
            else:
                raise JSONDataSerializerError("Unknown key/index type:"+str(key))
            
        if isinstance(targetnode,JSONPointer):
            hook = targetnode.get_node(self.data)
        else:
            hook = targetnode
        if isinstance(branch,JSONPointer):
            
            #FIXME: iterator
            branch = branch.get_path_list()

        if not branch:
            raise JSONDataSerializerError("missing branch")
            
        if hook in ('', u''):
            hook = self.data
        
        if type(hook) == dict:
            if type(branch[0]) not in (str,unicode,):
                raise JSONDataSerializerError("branch not compatible with container:"+str(type(hook))+" / "+str(type(branch[0])))

#             if len(branch)>1:
#                 hook[unicode(branch[0])] = getNewNode(branch[1])
#                 ret = self.branch_create(hook[branch[0]], branch[1:], value)
#             if not hook.get(branch[0]): # if not present
#                 hook[unicode(branch[0])] = self.getValueNode(value)

            if len(branch)>1:
                if not hook.get(unicode(branch[0]),False):
                    hook[unicode(branch[0])] = getNewNode(branch[1])
                ret = self.branch_create(hook[branch[0]], branch[1:], value)
            else:
                hook[unicode(branch[0])] = self.getValueNode(value)
                                
        elif type(hook) == list:
            if type(branch[0]) in (int,) and branch[0] < len(hook): # see RFC6902 for '-'/append
                pass
            elif branch[0] == '-': # see RFC6902 for '-'/append
                pass
            else:
                raise JSONDataSerializerError("failed hook in branch:"+str(type(hook))+" / "+str(type(branch[0])))

            if len(branch) == 1:            
                if branch[0] == '-':
                    branch[0] = len(hook)
                    hook.append(self.getValueNode(value))
                else:
                    hook[branch[0]] = self.getValueNode(value)
                ret = hook
            else:
                if branch[0] == '-':
                    branch[0] = len(hook)
                    hook.append(getNewNode(branch[1]))
                ret = self.branch_create(hook[branch[0]], branch[1:], value)

        else:
            raise JSONDataSerializerError("Type not applicable:"+str(type(hook)))

        return ret
    
    def branch_delete(self, datafile=None, schemafile=None,targetnode=None, **kargs):
        """ Deletes branches from JSON based data trees with static and dynamic criteria.

        The 'branch_delete' function enables for extended checks of deletion, e.g the
        detection of modified data, whereas the 'branch_remove' function simply removes
        by a subset of some static checks with 'isApplicable' validation.

        Handles several scenarios of plausibility and applicability checks.

        0. Just do it:
            branch_delete(None, None,None)
                Deletes self.data
            branch_delete(None, None,targetnode)
                Deletes targetnode
        1. Check datafile for applicability, no schema validation:
            branch_delete(datafile, None,None)
                Deletes self.data
            branch_delete(datafile, None,targetnode)
                Deletes targetnode
        2. Check datafile for applicability, with schemafile validation:
            branch_delete(datafile, schemafile,None)
                Deletes self.data
            branch_delete(datafile, schemafile,targetnode)
                Deletes targetnode
        3. Check datafile for applicability, with schema validation:
            kargs={'schema':"<jsonschema-object>"}

            branch_delete(datafile, None,None,**kargs)
                Deletes self.data
            branch_delete(datafile, None,targetnode,**kargs)
                Deletes targetnode

        REMARK: Due to the huge amount of shared code with 'json_import',
            this function is internally mapped to 'json_import'.

        Args:
            datafile:
                JSON data filename containing the subtree for the target branch.
            schemafile:
                JSON-Schema filename for validation of the subtree/branch.
            targetnode:
                Target container hook for the inclusion of the loaded branch.
                The branch is treated as a child-branch, hooked into the
                provided container 'targetnode'. Therefore the parameter
                kargs['branchoperations'] defines the behaviour for the
                various scenarios.
                The default:='None', than 'self.data' is used as the MODE_SCHEMA_DRAFT4
                container.
            **kargs:
                branchoperations: [branch_remove,]
                    Definition of the handling of redundancies in case of
                    present previous object.
                    For additional information refer to the '__init__' method.
                matchcondition:
                    Defines the criteria for comparison of present child nodes
                    in the target container. The value is a list of critarias
                    combined by logical AND. The criteria may vary due to
                    the requirement and the type of applied container.

                    For information on applicable values refer to:
                        'JSONDataSerializer.isApplicable()'

                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    default:= validate

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataSerializerErrorAttributeValue:

        """
        if kargs.get('branchoperations',BRANCH_REMOVE) != BRANCH_REMOVE:
            raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))

        if __debug__:
            if self.debug:
                print "DBG:branch_delete:datafile=  "+str(datafile)
                print "DBG:branch_delete:schemafile="+str(schemafile)
        return self.json_import(datafile, schemafile, targetnode, **kargs)

    def branch_diff(self):
        """Creates a branch_diff branch for export and re-read by JSONPatch.
        
        #FIXME:
        """
        pass

    def branch_move(self,sourcenode,targetnode,force=False,matchcondition=None):
        """Moves a source branch to target node.
        """
        ret = self.branch_copy(sourcenode, targetnode, force, matchcondition)
        if ret:
            ret = self.branch_remove(targetnode, sourcenode, force, matchcondition)
        return ret
    
    def branch_remove(self, targetnode, branch=None, matchcondition=None):
        """Removes a branch from a target structure by basic static criteria.

        The corresponding elements of the 'targetnode' tree are removed from
        the tree 'targetnode'. The remaining are kept untouched. For tree
        nodes as leafs the whole corresponding subtree is deleted.

        REMARK: No reference checks are done, so the user is responsible
            for additional references.

        Args:
            targetnode: Targetnode where the branch is to be removed.
                When 'None' all child nodes are removed.

            branch: Branch to be removed from the target tree.

            matchcondition: Defines the condition for applicability
                of the branch_remove method. For the provided values refer
                to the call 'isApplicable'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataSerializerError:

        """
        ret = True

        if type(branch) == dict:
            for k,v in branch.items():
                if matchcondition:
                    if self.isApplicable(targetnode, {k:v}, matchcondition):
                        targetnode.pop(k)
                    else:
                        ret = False
                else:
                    targetnode.pop(k)

        elif type(branch) == list:
            for v in branch:
                if matchcondition:
                    if self.isApplicable(targetnode, [v], BRANCH_REMOVE):
                        targetnode.branch_remove(v)
                    else:
                        ret = False
                else:
                    targetnode.branch_remove(v)

        else:
            raise JSONDataSerializerError("Type not supported:type="+str(branch))
        return ret

    def branch_replace(self,targetnode,branch,matchcondition=None):
        """Replaces the target node by the source branch.
        """
        ret = self.branch_remove(targetnode, branch, matchcondition)
        if ret:
            ret = self.branch_copy(branch, targetnode, matchcondition)
        return ret
    
    def branch_replace_set(self, targetnode, branch, matchcondition=None):
        """Replaces the complete set of child branches by branch.

        All present previous branches are removed and replaced by
        provided branch. The replacement level is swallow, thus
        the scope is all matched immediate children.

        Args:
            target: Target tree the source is to be inserted.

            branch: Source branch to be inserted into target tree.

            matchcondition: The matchcondition is just present for
                interface unity with the other tree methods.
                Actually the value is ignored, the set is replaced
                in any case completely.

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataSerializerError:

        """
        ret = True

        # want to keep the container node address!!!
        if type(targetnode) == dict:
            targetnode.clear()
            targetnode.update(branch)

        elif type(targetnode) == list:
            for v in targetnode:
                targetnode.branch_remove(v)
            targetnode.extend(branch)

        else:
            raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
        return ret

    def branch_test(self,source,target):
        """Tests match in accordance to RFC6902.
        """
        pass    
    
    def getNodeForPointer(self,pointer):
        """Returns for a JSONPointer the reference to the according Node. 
        """
        #FIXME:
        pass

    def getPointerForNode(self,node):
        """Returns a JSONPointer for a provided Node. 
        """
        #FIXME:
        pass

    def getValueNode(self,value):
        """
        Args:
            value: Value pointer to be evaluated to the actual value.
                Valid input types are:
                    int: Integer, kept as integer. 
                    dict,list: Assumed to be a valid node for 'json' package.
                    str,unicode: Assumed to be a string representation of a
                        JSON type path or value.
                    JSONPointer: A JSON pointer compatible to RFC6901.

        Returns:
            When successful returns the value, else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataSerializerError:

        """
        if type(value) in (int,dict,list): # assumes a 'json' package type node
            return value
        elif type(value) in ( str, unicode, ): # assume a 'JSON' RFC7159 string
            if value[0].replace(" ","") in ('{','[',u'{',u'['):
                return json.loads(value) # a valid json object or array
            return unicode(value) # a simple value
        elif isinstance(value,JSONPointer): # assume the pointed value
            return value.get_node_or_value(self.data)
        elif not value:
            return None
        else:
            raise JSONDataSerializerError("Unknown value type:"+str(value))
    
    
    def isApplicable(self, targetnode, branch, matchcondition=None,**kargs):
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
            JSONDataSerializerError:

            JSONDataSerializerErrorAttributeValue:

        """

        #
        #*** Fetch parameters
        #
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
            else:
                raise JSONDataSerializerErrorAttributeValue("matchcondition",str(v))
        for k,v in kargs.items():
            if k == 'childattrlist': # provides a list of child attributes
                childattrlist = v
#TODO:
#             elif k == 'schema':
#                 sval = v

        retOK = True # return in case of no-defined-condition or no-failing-condition

        # The first mandatory requirement definition if the type compatibility
        # of the plug and the plugin-element.
        if type(targetnode) != type(branch):
            raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))

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
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
            elif m == MATCH_KEY:
                if type(targetnode) != dict:
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                for k in branch.keys():
                    if not targetnode.get(k):
                        return retFailed
            elif m == MATCH_CHLDATTR:
                if not type(targetnode) in (list,dict):
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                if childattrlist != None:
                    if type(branch) == dict:
                        for ca in childattrlist:
                            if not targetnode.get(ca):
                                return retFailed
                    elif type(branch) == list:
                        for l in targetnode:
                            if not type(l) is dict:
                                raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                            for ca in childattrlist:
                                if not type(ca) is dict:
                                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                                if not l.get(ca):
                                    return retFailed
                    else:
                        raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
            elif m == MATCH_INDEX:
                if type(targetnode) != list:
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                if len(targetnode) > len(branch):
                    return retFailed
            elif m == MATCH_MEM:
                if type(targetnode) == list:
                    if type(targetnode) != type(branch):
                        raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                    for l in branch:
                        try:
                            if not targetnode.index(l):
                                return retFailed
                        except:
                            return retFailed
                elif type(targetnode) == dict:
                    if type(targetnode) == type(branch):
                        raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                    for k,v in branch.items():
                        if id(v) != id(targetnode.get(k)):
                            return retFailed
                else:
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
            elif _matchcondition:
                raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
        return retOK

    def json_export(self, fname, base=None, **kargs):
        """ Exports current data for later import.

        The exported data is a snapshot of current state. This
        contains all manual set parameters for next start.

        Args:
            fname: File name for the exported data.

            base: Base of sub-tree for export.

            **kargs:
                branchdepth: [all, framework, plugins ]
                    Defines the scope of the dumped data.
                        all: The complete tree, including all loaded
                            additional branches.
                        framework: The data of the framework only, excluding
                            additional branches.
                        plugins: Additional branches only. The parameter
                            'plugins' or 'branches' defines the scope.
                plugins:
                    Lists the names of the additional branches to be contained
                    in the output.
                branches:
                    Lists the in memory reference pointers to the branch base.

        Returns:
            When successful returns 'True', else returns either 'False',
            or raises an exception.

        Raises:
            JSONDataSerializerErrorTargetFileReason:
        """
        if not base:
            base = self.data
        try:
            with open(fname, 'w') as fp:
                ret = json.dump(base, fp)
        except Exception as e:
            raise JSONDataSerializerErrorTargetFileReason(str(fname),str(e))
        return ret

    def json_import(self, datafile, schemafile=None,targetnode=None, **kargs):
        """ Imports and validates JSON based data.

        The contained data in 'datafile' could be either the initial data
        tree, or a new branch defined by a fresh tree structure. The
        'targetnode' defines the parent container where the new branch has
        to be hooked-in.

        Args:
            datafile:
                JSON data filename containing the subtree for the target branch.
            schemafile:
                JSON-Schema filename for validation of the subtree/branch.
            targetnode:
                Target container hook for the inclusion of the loaded branch.
                The branch is treated as a child-branch, hooked into the
                provided container 'targetnode'. Therefore the parameter
                kargs['branchoperations'] defines the behaviour for the
                various scenarios.
                The default:='None', than 'self.data' is used as the default
                container.
            **kargs:
                branchoperations: [branch_add_only, branch_replace-set, branch_add, branch_remove,]
                    Definition of the handling of redundancies in case of
                    present previous object.
                    For additional information refer to the '__init__' method.
                matchcondition:
                    Defines the criteria for comparison of present child nodes
                    in the target container. The value is a list of critarias
                    combined by logical AND. The criteria may vary due to
                    the requirement and the type of applied container.

                    For information on applicable values refer to:
                        'JSONDataSerializer.isApplicable()'

                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    default:= validate

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONDataSerializerError:

            JSONDataSerializerErrorAttributeValue:

            JSONDataSerializerErrorSourceFile:

            JSONDataSerializerErrorSourceFileReason:

        """
        if self.verbose:
            print "VERB:json_import:datafile=   "+str(datafile)
            print "VERB:json_import:schemafile= "+str(schemafile)

        jval = None
        sval = None
        matchcondition = []

        #
        #*** Fetch parameters
        #
        branchoperations = self.branchoperations # use class settings as MODE_SCHEMA_DRAFT4
        validator = self.validator # use class settings as MODE_SCHEMA_DRAFT4
        for k,v in kargs.items():
            if k == 'branchoperations':
                if v == 'branch_replace-set' or v == BRANCH_REPLACE_SET:
                    branchoperations = BRANCH_REPLACE_SET
                elif v == 'branch_replace' or v == BRANCH_REPLACE:
                    branchoperations = BRANCH_REPLACE
                elif v == 'branch_add' or v == BRANCH_SUPERPOSE:
                    branchoperations = BRANCH_SUPERPOSE
                elif v == 'branch_add_only' or v == BRANCH_ADD:
                    branchoperations = BRANCH_ADD
                elif v == 'branch_remove' or v == BRANCH_REMOVE:
                    branchoperations = BRANCH_REMOVE
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'matchcondition':
                #For now just passed through to self.isApplicable()
                if v == 'key' or v == MATCH_KEY:
                    matchcondition.append(MATCH_KEY)
                elif v == 'no' or v == MATCH_NO:
                    matchcondition.append(MATCH_NO)
                elif v == 'child_attr_list' or v == MATCH_CHLDATTR:
                    matchcondition.append(MATCH_CHLDATTR)
                elif v == 'index' or v == MATCH_INDEX:
                    matchcondition.append(MATCH_INDEX)
                elif v == 'mem' or v == MATCH_MEM:
                    matchcondition.append(MATCH_MEM)
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == MODE_SCHEMA_DRAFT4:
                    validator = MODE_SCHEMA_DRAFT4
                elif v == 'draft3' or v == MODE_SCHEMA_DRAFT3:
                    validator = MODE_SCHEMA_DRAFT3
                elif v == 'off' or v == MODE_SCHEMA_OFF:
                    validator = MODE_SCHEMA_OFF
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'schema':
                sval = v

        # INPUT-BRANCH: schema for validation
        if validator != MODE_SCHEMA_OFF: # validation requested, requires schema
            if not schemafile: # no new import, use present data
                if not self.schema: # no schema data present
                    raise JSONDataSerializerError("Missing JSONschema:info")
            else:
                schemafile = os.path.abspath(schemafile)
                if not os.path.isfile(schemafile):
                    raise JSONDataSerializerErrorSourceFile("schemafile",str(schemafile))
                with open(schemafile) as schema_file:
                    sval = json.load(schema_file)
                if not sval:
                    raise JSONDataSerializerErrorSourceFile("schemafile",str(schemafile))

        # INPUT-BRANCH: data
        datafile = os.path.abspath(datafile)
        if not os.path.isfile(datafile):
            raise JSONDataSerializerErrorSourceFile("datafile",str(datafile))
        try:
            with open(datafile) as data_file: # load data
                jval = json.load(data_file)
        except Exception as e:
            raise JSONDataSerializerErrorSourceFileReason("datafile",str(datafile),str(e))
        if not jval:
            raise JSONDataSerializerErrorSourceFile("datafile",str(datafile))

        # INPUT-BRANCH: validate data
        if validator == MODE_SCHEMA_DRAFT4:
            if self.verbose:
                print "VERB:Validate: draft4"
            jsonschema.validate(jval, sval)
        elif validator == MODE_SCHEMA_DRAFT3:
            if self.verbose:
                print "VERB:Validate: draft3"
            jsonschema.Draft3Validator(jval, sval)
        elif validator != MODE_SCHEMA_OFF:
            raise JSONDataSerializerErrorAttributeValue("validator",str(validator))

        #
        # TARGET-CONTAINER: manage new branch data
        #
        if not targetnode: # use defaults
            if not self.data: # the initial load, thus OK in any case
                self.data = jval
            targetnode = self.data
            ret = jval != None
        else: # data history present, so decide how to handle

            # Checks that the branch fits into the target container
            if not self.isApplicable(targetnode, jval, matchcondition):
                return False

            # The following branchoperations depend on the container type,
            # in some cases even are not applicable.
            if branchoperations == BRANCH_REPLACE_SET:
                ret = self.branch_replace_set(targetnode,jval,matchcondition)
            elif branchoperations == BRANCH_REPLACE:
                ret = self.branch_replace(targetnode,jval,matchcondition)
            elif branchoperations == BRANCH_SUPERPOSE:
                ret = self.branch_add(targetnode,jval,matchcondition)
            elif branchoperations == BRANCH_ADD:
                ret = self.branch_add_only(targetnode,jval,matchcondition)
            elif branchoperations == BRANCH_REMOVE:
                ret = self.branch_remove(targetnode,jval,matchcondition)
            else:
                raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))

        return ret # jval != None

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
            JSONDataSerializerErrorAmbiguity:

            forwarded from 'json'

        """
        source = kargs.get('source',None)
        sourcefile = kargs.get('sourcefile',None)
        if sourcefile and source:
            raise JSONDataSerializerErrorAmbiguity('sourcefile/source',
                "sourcefile="+str(sourcefile),
                "source="+str(source)
                )
        if sourcefile:
            source = open(sourcefile)
            source = json.load(source)
        elif not source:
            source = self.data # yes, almost the same...

        if pretty:
            print json.dumps(source,indent=self.indent)
        else:
            print json.dumps(source)

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
            JSONDataSerializerErrorAmbiguity:

            forwarded from 'json'

        """
        source = kargs.get('source',None)
        sourcefile = kargs.get('sourcefile',None)
        if sourcefile and source:
            raise JSONDataSerializerErrorAmbiguity('sourcefile/source',
                "sourcefile="+str(sourcefile),
                "source="+str(source)
                )
        if sourcefile:
            source = open(sourcefile)
            source = json.load(source)
        elif not source:
            source = self.schema # yes, almost the same...

        if pretty:
            print json.dumps(source,indent=self.indent)
        else:
            print json.dumps(source)

    def set_schema(self,schemafile=None, targetnode=None, **kargs):
        """Sets schema or inserts a new branch.

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
                branchoperations: [append, branch_add_only, prepend, branch_replace-object,
                    branch_replace-set, branch_add, ]
                    Definition of the handling of redundancies in case of
                    present previous object. For additional information refer
                    to the '__init__' method.
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

            JSONDataSerializerError:

            JSONDataSerializerErrorSourceFile:

            JSONDataSerializerErrorAttributeValue:

            JSONDataSerializerErrorValue:

        """
        if __debug__:
            if self.debug:
                print "DBG:set_schema:schemafile="+str(schemafile)

        #
        #*** Fetch parameters
        #
        datafile = None
        branchoperations = self.branchoperations # use class settings as MODE_SCHEMA_DRAFT4
        validator = self.validator # use class settings as MODE_SCHEMA_DRAFT4
        persistent = False
        schema = None
        for k,v in kargs.items():
            if k == 'branchoperations':
                if v == 'branch_replace-set' or v == BRANCH_REPLACE_SET:
                    branchoperations = BRANCH_REPLACE_SET
                elif v == 'branch_replace' or v == BRANCH_REPLACE:
                    branchoperations = BRANCH_REPLACE
                elif v == 'branch_add' or v == BRANCH_SUPERPOSE:
                    branchoperations = BRANCH_SUPERPOSE
                elif v == 'branch_add_only' or v == BRANCH_ADD:
                    branchoperations = BRANCH_ADD
                elif v == 'branch_remove' or v == BRANCH_REMOVE:
                    branchoperations = BRANCH_REMOVE
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == MODE_SCHEMA_DRAFT4:
                    validator = MODE_SCHEMA_DRAFT4
                elif v == 'draft3' or v == MODE_SCHEMA_DRAFT3:
                    validator = MODE_SCHEMA_DRAFT3
                elif v == 'off' or v == MODE_SCHEMA_OFF:
                    validator = MODE_SCHEMA_OFF
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
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
                raise JSONDataSerializerErrorValue("JSONSchemaFilename","")

        # schema for validation
        if schema: # use loaded
            pass

        elif schemafile: # load from file
            schemafile = os.path.abspath(schemafile)
            self.schemafile = schemafile
            if not os.path.isfile(schemafile):
                raise JSONDataSerializerErrorSourceFile("schemafile",str(schemafile))
            with open(schemafile) as schema_file:
                schema = json.load(schema_file)
            if schema == None:
                raise JSONDataSerializerErrorSourceFile("schemafile",str(schemafile))

        else: # missing at all
            raise JSONDataSerializerErrorSourceFile("schemafile",str(schemafile))
            pass

        #
        # manage new branch data
        #
        if not targetnode:
            self.schema = schema

        else: # data history present, so decide how to handle

            # the container hook has to match for insertion-
            if type(targetnode) != type(schema):
                raise JSONDataSerializerError("Type-Mismatch:target="+str(type(targetnode))+" != branch"+str(type(schema)))

            # The following branchoperations depend on the container type,
            # in some cases even are not applicable.

            if branchoperations == BRANCH_REPLACE_SET:
                # just accept any by simply removing previous
                if targetnode == self.schema: # it is a complete branch_replace
                    self.schema = schema
                    targetnode = schema
                else: # it is a partial branch_replace of a subset
                    targetnode = schema
            elif branchoperations == BRANCH_REPLACE:
                #FIXME:
                # just accept any by simply removing previous
                if targetnode == self.data: # it is a complete branch_replace
                    self.schema = schema
                    targetnode = schema
                else: # it is a partial branch_replace of a subset
                    targetnode = schema
            elif branchoperations == BRANCH_SUPERPOSE:
                self.branch_add(targetnode,schema)
            elif branchoperations == BRANCH_ADD:
                self.branch_add_only(targetnode,schema)
            elif branchoperations == BRANCH_REMOVE:
                self.branch_remove(targetnode,schema)
            else:
                raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))
        return schema != None
