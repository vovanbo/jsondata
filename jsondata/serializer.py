# -*- coding:utf-8   -*-
"""Basic features for the persistence of JSON based in-memory data.
"""
import logging
import os

try:
    import ujson as myjson
except ImportError:
    import json as myjson

from .data import SchemaMode, Match
from .exceptions import (
    JSONDataException, JSONDataValue, JSONDataSourceFile, JSONDataTargetFile
)
from .data import JSONData
from jsondata.exceptions import JSONDataAmbiguity

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


class JSONDataSerializer(JSONData):
    """Persistency of JSON based data for the class jsondata.JSONData.
    
    This class provides for persistency of data managed by jsondata.JSONData.

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

    def __init__(self, appname, *args, **kwargs):
        """Loads and validates a JSON definition with the corresponding schema file.

        Args:
            appname: Name of the application. An arbitrary string representing the
                name of an application. The name is mainly used for the default
                name prefix of the JSON data and schema.

            args*: Optional position parameters, these branch_replace corresponding key
                parameters.
                filelist, pathlist, filepathlist, schema_file
            **kwargs:
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
                interactive: Hints on command line call for optional change of display format. 
                    
                    default:= False
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
                schema_file: Filepathname of JSONschema file.
                    
                    default:= <appname>.jsd
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None
                    
                    default:= validate

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

            JSONDataSourceFile:

            JSONDataAmbiguity:

            JSONDataValue:

            jsonschema.ValidationError:

            jsonschema.SchemaError:

        """
        # Init basic data, control actions not to be repeated
        _validate = kwargs.get('validator', False)
        if _validate:
            kwargs['validator'] = SchemaMode.OFF
        JSONData.__init__(self, [], **kwargs)
        if _validate:
            kwargs['validator'] = _validate

        #
        # static final defaults
        #

        # prep import subcall
        kimp = {}

        self.nodefaultpath = False
        self.nodesubdata = False
        self.requires = False

        # Either provided explicitly, or for search.
        self.datafile = None

        afile = os.path.abspath(str(__file__))

        # The internal object schema for the framework - a fixed set of files as final MODE_SCHEMA_DRAFT4.
        self.schemafile = kwargs.get('schema_file', None)
        if self.schema and self.schemafile:
            # When a schema/schema file is provided, it is the only and one
            # for the top-level,
            raise JSONDataAmbiguity('schema_file/schema',
                                    "schema_file=" + str(self.schemafile),
                                    "schema=" + str(self.schema)
                                    )

        self.nodefaultpath = kwargs.get('nodefaultpath', False)

        self.pathlist = kwargs.get('pathlist', '')

        self.filelist = kwargs.get('filelist', None)
        if not self.filelist:
            self.filelist = [appname + '.json', ]

        self.filepathlist = kwargs.get('filepathlist', [])

        # positional parameters dominate, remaining are MODE_SCHEMA_DRAFT4
        if args:
            for i in range(0, len(args)):
                if i == 0:
                    self.filelist = args[i]
                elif i == 1:
                    self.pathlist = args[i]
                elif i == 2:
                    self.filepathlist = args[i]
                elif i == 3:
                    self.schemafile = args[i]
                else:
                    raise JSONDataValue("unknown", "args[" + str(i) + "]",
                                        str(args))

        #
        # *** Fetch parameters
        #
        for k, v in list(kwargs.items()):
            #             if k == 'branch':
            #                 self.branch = v
            if k == 'datafile':
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
            elif k == 'requires':
                self.requires = v
            elif k == 'schema_file':
                self.schemafile = v
            elif k == 'validator':
                self.validator = v

        if __debug__:
            if self.debug:
                print("DBG:self.pathlist=    " + str(self.pathlist))
                print("DBG:self.filelist=    " + str(self.filelist))
                print("DBG:self.filepathlist=" + str(self.filepathlist))
                print("DBG:self.schema_file=  " + str(self.schemafile))

        if type(self.pathlist) == list:  # a list of single-paths
            if not self.nodefaultpath:
                # Fixed set of data files as final default.
                self.pathlist.extend(
                    [os.path.dirname(
                        afile) + os.sep + 'etc' + os.sep + appname + os.sep,
                     os.pathsep + os.sep + 'etc' + os.sep,
                     os.pathsep + "$HOME" + os.sep + 'etc' + os.sep,
                     os.pathsep + os.path.dirname(__file__) + os.sep,
                     ])

            # expand all
            self.pathlist = [os.path.expandvars(os.path.expanduser(p)) for p in
                             self.pathlist]
            # parts = [part.branch_replace('~', '~0') for part in self.parts]

        else:  # a PATH like variable, so do it at once
            if not self.nodefaultpath:
                # Fixed set of data files as the final default.
                self.pathlist += os.path.dirname(
                    afile) + os.sep + 'etc' + os.sep + appname + os.sep + os.pathsep + os.sep + 'etc' + os.sep + os.pathsep + "$HOME" + os.sep + 'etc' + os.sep + os.pathsep + os.path.dirname(
                    __file__) + os.sep
            self.pathlist = os.path.expandvars(
                os.path.expanduser(self.pathlist)).split(os.pathsep)

        # canonical
        self.pathlist = [os.path.realpath(os.path.abspath(p)) + os.sep for p in
                         self.pathlist]

        if not self.datafile:  # No explicit given
            if self.filelist:
                for f in self.filelist:
                    if os.path.isabs(f):
                        self.filepathlist.append(f)
                        self.filelist.remove(f)
                    else:
                        for p in self.pathlist:
                            fx = p + os.sep + f
                            if os.path.isfile(fx):
                                self.filepathlist.append(fx)
                                if f in self.filelist:  # could occur under multiple paths
                                    self.filelist.remove(f)

        elif not os.path.isfile(
                self.datafile):  # a provided datafile has to exist
            raise JSONDataSourceFile("open", "datafile", str(self.datafile))

        if not self.filepathlist:
            if not self.datafile:
                raise JSONDataSourceFile("value", "datasource",
                                         str(self.filelist) + ":" + str(
                                             self.pathlist))

        # Check whether validation is requested.
        # If so, do a last trial for plausible construction.
        if not self.schema and self.validator is not SchemaMode.OFF:
            # require schema for validation, no schema provided, now-than...
            if not self.schemafile:  # do we have a file
                if self.datafile:
                    if os.path.isfile(os.path.splitext(self.datafile)[
                                          0] + '.jsd'):  # coallocated pair - datafile+schema_file
                        self.schemafile = os.path.splitext(self.datafile)[
                                              0] + '.jsd'
                elif self.filepathlist:  # search, use the first found
                    for f in self.filepathlist:
                        if os.path.isfile(f) and os.path.isfile(
                                        os.path.splitext(f)[0] + ".jsd"):
                            self.schemafile = os.path.splitext(f)[0] + ".jsd"
                            break  # just use the first valid-pair
                        raise JSONDataSourceFile("open", "schema_file",
                                                 str(self.filepathlist))
                else:
                    raise JSONDataSourceFile("value", "datasource",
                                             str(self.filelist) + ":" + str(
                                                 self.pathlist))

            # when defined => has to be present
            if self.schemafile:
                if not os.path.isfile(self.schemafile):
                    raise JSONDataSourceFile("open", "schema_file",
                                             str(self.schemafile))

                # initialize schema
                kwargs['schema_file'] = self.schemafile
                self.set_schema(**kwargs)

        if __debug__:
            if self.debug:
                print("DBG:self.pathlist=    " + str(self.pathlist))
                print("DBG:self.filelist=    " + str(self.filelist))
                print("DBG:self.filepathlist=" + str(self.filepathlist))
                print("DBG:self.schema_file=  " + str(self.schemafile))

        #
        # load data, therefore search data files within pathlist
        #
        confok = False
        onenok = False
        if not self.datafile:  # No explicit given
            if self.filepathlist:
                for f in self.filepathlist:
                    if self.json_import(self.branch, None, f, self.schemafile,
                                        **kimp):
                        confok = True
                    else:
                        onenok = True

                if not confok:  # base loaded only
                    if not self.requires:  # there is a rule
                        if self.requires == 'base':  # is mandatory, reaching this means is OK
                            pass
                        else:
                            raise JSONDataSourceFile("value", "datasource", str(
                                self.filepathlist) + ":" + str(
                                self.filelist) + ":" + str(self.pathlist))

                else:  # at least one application configuration loaded
                    if self.requires != False:  # there is a rule
                        if self.requires == 'all':  # no exeception allowed
                            if onenok:  # one has failed
                                raise JSONDataSourceFile("value", "datasource",
                                                         str(
                                                             self.filepathlist) + ":" + str(
                                                             self.filelist) + ":" + str(
                                                             self.pathlist))
                        elif self.requires == 'base':  # is mandatory, reaching this means is OK
                            pass
                        elif self.requires == 'one':  # reaching this means is OK
                            pass

        else:
            if os.path.exists(self.datafile):
                if not self.schemafile and self.schema:
                    kimp['schema'] = self.schema
                self.json_import(self.branch, None, self.datafile,
                                 self.schemafile, **kimp)

    def json_export(self, sourcenode, fname, **kargs):
        """ Exports current data for later import.

        The exported data is a snapshot of current state.

        Args:
            fname: File name for the exported data.

            sourcenode: Base of sub-tree for export.
                None for complete JSON document.

            **kargs:
                ffs.

        Returns:
            When successful returns 'True', else returns either 'False',
            or raises an exception.

        Raises:
            JSONDataTargetFile:
        """
        if not sourcenode:
            sourcenode = self.data
        try:
            with open(fname, 'w') as fp:
                # ret =
                myjson.dump(sourcenode, fp)
        except Exception as e:
            raise JSONDataTargetFile("open-" + str(e), "data.dump", str(fname))
        return True

    def json_import(self, targetnode, key, datafile, schemafile=None, **kargs):
        """ Imports and validates JSON based data.

        The contained data in 'datafile' could be either the initial data
        tree, or a new branch defined by a fresh tree structure. The
        'targetnode' defines the parent container where the new branch has
        to be hooked-in.

        Args:
            targetnode:
                Target container for the inclusion of the loaded branch.
                For the default:='None' the 'self.data' is used.
            key:
                The hook within the targetnode,
            datafile:
                JSON data filename containing the subtree for the target branch.
            schemafile:
                JSON-Schema filename for validation of the subtree/branch.
            **kargs:
                matchcondition:
                    Defines the criteria for comparison of present child nodes
                    in the target container. The value is a list of criteria
                    combined by logical AND. The criteria may vary due to
                    the requirement and the type of applied container.

                    For information on applicable values refer to:
                        'JSONDataSerializer.is_applicable()'

                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    
                    default:= validate

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:

            JSONDataValue:

            JSONDataSourceFile:

        """
        if self.verbose:
            print("VERB:json_import:datafile=   " + str(datafile))
            print("VERB:json_import:schema_file= " + str(schemafile))

        jval = None
        sval = None
        matchcondition = []

        #
        # *** Fetch parameters
        #
        validator = self.validator  # use class settings as MODE_SCHEMA_DRAFT4
        for k, v in list(kargs.items()):
            if k == 'matchcondition':
                # For now just passed through to self.is_applicable()
                if v == 'key' or v == Match.KEY:
                    matchcondition.append(Match.KEY)
                elif v == 'no' or v is Match.NO:
                    matchcondition.append(Match.NO)
                elif v == 'child_attr_list' or v == Match.CHLDATTR:
                    matchcondition.append(Match.CHLDATTR)
                elif v == 'index' or v == Match.INDEX:
                    matchcondition.append(Match.INDEX)
                elif v == 'mem' or v == Match.MEM:
                    matchcondition.append(Match.MEM)
                else:
                    raise JSONDataValue(k, str(v))
            elif k == 'validator':  # controls validation by JSONschema
                if v == 'default' or v is SchemaMode.DRAFT4:
                    validator = SchemaMode.DRAFT4
                elif v == 'draft3' or v is SchemaMode.DRAFT3:
                    validator = SchemaMode.DRAFT3
                elif v == 'off' or v is SchemaMode.OFF:
                    validator = SchemaMode.OFF
                else:
                    raise JSONDataValue("unknown", k, str(v))
            elif k == 'schema':
                sval = v

        # INPUT-BRANCH: schema for validation
        if validator is not SchemaMode.OFF:  # validation requested, requires schema
            if not schemafile:  # no new import, use present data
                if not self.schema:  # no schema data present
                    raise JSONDataException("value", "schema", self.schema)
            else:
                schemafile = os.path.abspath(schemafile)
                if not os.path.isfile(schemafile):
                    raise JSONDataSourceFile("open", "schema_file",
                                             str(schemafile))
                with open(schemafile) as schema_file:
                    sval = myjson.load(schema_file)
                if not sval:
                    raise JSONDataSourceFile("read", "schema_file",
                                             str(schemafile))

        # INPUT-BRANCH: data
        datafile = os.path.abspath(datafile)
        if not os.path.isfile(datafile):
            raise JSONDataSourceFile("open", "datafile", str(datafile))
        try:
            with open(datafile) as data_file:  # load data
                jval = myjson.load(data_file)
        except Exception as e:
            raise JSONDataSourceFile("open", "datafile", str(datafile), str(e))
        if not jval:
            raise JSONDataSourceFile("read", "datafile", str(datafile))

        # INPUT-BRANCH: validate data
        self.validate(jval, sval, validator)

        #
        # TARGET-CONTAINER: manage new branch data
        #
        if not targetnode:  # use defaults
            if not self.data:  # the initial load, thus OK in any case
                self.data = jval
            targetnode = self.data
            ret = jval != None
        else:  # data history present, so decide how to handle

            # Checks that the branch fits into the target container
            if not self.is_applicable(targetnode, key, jval):
                return False

            ret = self.branch_add(targetnode, key, jval)

        return ret  # jval != None

    def print_data(self, pretty=True, **kwargs):
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
        source = kwargs.get('source', None)
        sourcefile = kwargs.get('sourcefile', None)
        if sourcefile and source:
            raise JSONDataAmbiguity('sourcefile/source',
                                    "sourcefile=" + str(sourcefile),
                                    "source=" + str(source)
                                    )
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.data  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def print_schema(self, pretty=True, **kwargs):
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
        source = kwargs.get('source', None)
        sourcefile = kwargs.get('sourcefile', None)
        if sourcefile and source:
            raise JSONDataAmbiguity('sourcefile/source',
                                    "sourcefile=" + str(sourcefile),
                                    "source=" + str(source)
                                    )
        if sourcefile:
            source = open(sourcefile)
            source = myjson.load(source)
        elif not source:
            source = self.schema  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def set_schema(self, schema_file=None, target_node=None, **kwargs):
        """Sets schema or inserts a new branch into the current assigned schema.

        The main schema(targetnode==None) is the schema related to the current
        instance. Additional branches could be added by importing the specific
        schema definitions into the main schema. These could either kept
        volatile as a temporary runtime extension, or stored into a new schema
        file in order as extension of the original for later combined reuse.

        Args:
            schema_file:
                JSON-Schema filename for validation of the subtree/branch.
                See also **kargs['schema'].
            target_node:
                Target container hook for the inclusion of the loaded branch.
            **kwargs:
                schema:
                    In-memory JSON-Schema as an alternative to schema_file.
                    When provided the 'schema_file' is ignored.
                    
                    default:=None
                validator: [default, draft3, off, ]
                    Sets schema validator for the data file.
                    The values are: default=validate, draft3=Draft3Validator,
                    off=None.
                    
                    default:= validate
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
        if __debug__:
            if self.debug:
                print("DBG:set_schema:schema_file=" + str(schema_file))

        #
        # *** Fetch parameters
        #
        datafile = None
        validator = self.validator  # use class settings as MODE_SCHEMA_DRAFT4
        persistent = False
        schema = None
        for k, v in list(kwargs.items()):
            if k == 'validator':  # controls validation by JSONschema
                if v == 'default' or v is SchemaMode.DRAFT4:
                    validator = SchemaMode.DRAFT4
                elif v == 'draft3' or v is SchemaMode.DRAFT3:
                    validator = SchemaMode.DRAFT3
                elif v == 'off' or v is SchemaMode.OFF:
                    validator = SchemaMode.OFF
                else:
                    raise JSONDataValue("unknown", k, str(v))
            elif k == 'schema':
                schema = v
            elif k == 'datafile':
                datafile = v
            elif k == 'persistent':
                persistent = v

        if schema_file != None:  # change filename
            self.schemafile = schema_file
        elif self.schemafile != None:  # use present
            schema_file = self.schemafile
        elif datafile != None:  # derive coallocated from config
            schema_file = os.path.splitext(self.datafile)[0] + '.jsd'
            if not os.path.isfile(schema_file):
                schema_file = None
            else:
                self.schemafile = schema_file

        if not schema_file:
            if persistent:  # persistence requires storage
                raise JSONDataTargetFile("open", "JSONSchemaFilename",
                                         schema_file)

        # schema for validation
        if schema:  # use loaded
            pass

        elif schema_file:  # load from file
            schema_file = os.path.abspath(schema_file)
            self.schemafile = schema_file
            if not os.path.isfile(schema_file):
                raise JSONDataSourceFile("open", "schema_file", str(schema_file))
            with open(schema_file) as schema_file:
                schema = myjson.load(schema_file)
            if schema == None:
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
            if type(target_node) != type(schema):
                raise JSONDataException("type", "target!=branch",
                                        str(type(target_node)) + "!=" + str(
                                            type(schema)))

            self.branch_add(target_node, schema)

        return schema is not None


from .pointer import JSONPointer
# avoid nested recursion problems
