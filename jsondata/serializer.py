# -*- coding:utf-8   -*-
"""Basic features for the persistence of JSON based in-memory data.
"""
import logging
import os

from pathlib import Path

try:
    import ujson as myjson
except ImportError:
    import json as myjson

from .data import JSONData, SchemaMode, Match
from .exceptions import (
    JSONDataException, JSONDataValue, JSONDataSourceFile, JSONDataTargetFile,
    JSONDataAmbiguity
)

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


class JSONDataSerializer(JSONData):
    """
    Persistency of JSON based data for the class jsondata.JSONData.
    
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

    def __init__(self, appname, data_file=None, file_list=None,
                 file_path_list=None, file_priority=None, indent_str=4,
                 load_cached=False, no_default_path=False, no_sub_data=False,
                 path_list=None, requires=None, schema=None, schema_file=None,
                 validator=SchemaMode.OFF):
        """
        Loads and validates a JSON definition with the corresponding
        schema file.

        Args:
            appname: Name of the application. An arbitrary string representing
                the name of an application. The name is mainly used for
                the default name prefix of the JSON data and schema.

            data_file: Filepathname of JSON data file, when provided a further
                search by path_list, file_list, and file_path_list is suppressed.
                Therefore it has to be a valid filepathname.

                default:= <appname>.json
            file_list: List of valid file names.

                default:= <appname>.json
            file_path_list: List of file path names. These are not prefixed
                by search path components, but made absolute.

                default:= []
            file_priority: [firstonly, lastonly, all]
                Defines the handling of multiple occurrences of a filename
                at various positions. This option thus may only be altered
                in conjunction with 'path_list'.

                default:= all
            indent_str: Defied the indentation of 'str'.

                default:= 4
            load_cached: Caching of load for JSON data files.
                Loads either completely into cache before transferring to
                production entries, or immediately into production parameters,
                which may take an effect on the remaining parameters
                to be loaded.

                default:= False
            no_default_path: Ignores the default paths, the exception is the
                base configuration, which still is searched within the default
                paths exclusively.

                default:= False
            no_sub_data: Supresses the load of sub-data files.
                default:= False
            path_list: List of path names for search of a valid filename.
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
        super(JSONDataSerializer, self).__init__(
            [], schema=schema, indent_str=indent_str, load_cached=load_cached,
            requires=requires, validator=SchemaMode.OFF
        )

        self.no_default_path = no_default_path
        self.no_sub_data = no_sub_data
        self.requires = requires

        # Either provided explicitly, or for search.
        self.data_file = Path(data_file) if data_file is not None else None

        file_ = Path(__file__).resolve()

        # The internal object schema for the framework -
        # a fixed set of files as final MODE_SCHEMA_DRAFT4.
        self.schema_file = schema_file
        if self.schema and self.schema_file:
            # When a schema/schema file is provided, it is the only and one
            # for the top-level,
            raise JSONDataAmbiguity('schema_file/schema',
                                    "schema_file=" + str(self.schema_file),
                                    "schema=" + str(self.schema)
                                    )

        self.path_list = path_list
        self.file_list = [Path(f) for f in file_list] \
            if file_list \
            else [Path('%s.json' % appname)]
        self.file_path_list = file_path_list or []
        self.file_priority = file_priority
        self.indent_str = indent_str
        self.load_cached = load_cached
        self.validator = validator

        logger.debug("self.path_list=%s", self.path_list)
        logger.debug("self.file_list=%s", self.file_list)
        logger.debug("self.file_path_list=%s", self.file_path_list)
        logger.debug("self.schema_file=%s", self.schema_file)

        if isinstance(self.path_list, str):
            self.path_list = self.path_list.split(os.pathsep)
        elif isinstance(self.path_list, Path):
            self.path_list = [self.path_list,]

        # a list of single-paths
        if not self.no_default_path:
            # Fixed set of data files as final default.
            self.path_list.extend([
                file_.parent / 'etc' / appname,
                Path('/etc/'),
                Path('$HOME/etc/'),
                file_.parent
            ])

        # expand all
        self.path_list = [
            Path(os.path.expandvars(os.path.expanduser(p))).resolve()
            for p in self.path_list
        ]

        if self.data_file is None or not self.data_file.exists():
            # No explicit given
            self.file_path_list = []
            for path in self.path_list:
                self.file_path_list.extend((path / f).resolve()
                                           for f in self.file_list)
            self.file_list = []
        elif self.data_file and not self.data_file.is_file():
            # a provided data_file has to exist
            raise JSONDataSourceFile("open", "data_file", str(self.data_file))

        if not self.file_path_list and not self.data_file:
            raise JSONDataSourceFile(
                "value", "datasource",
                '%s:%s' % (self.file_list, self.path_list)
            )

        # Check whether validation is requested.
        # If so, do a last trial for plausible construction.
        if not self.schema and self.validator is not SchemaMode.OFF:
            # require schema for validation, no schema provided, now-than...
            if not self.schema_file:  # do we have a file
                if self.data_file:
                    # co-allocated pair: data_file + schema_file
                    if self.data_file.with_suffix('.jsd').exists():
                        self.schema_file = self.data_file.with_suffix('.jsd')
                elif self.file_path_list:  # search, use the first found
                    for f in self.file_path_list:
                        if f.is_file() and f.with_suffix('.jsd').is_file():
                            self.schema_file = f.with_suffix('.jsd')
                            break  # just use the first valid-pair
                        raise JSONDataSourceFile("open", "schema_file",
                                                 str(self.file_path_list))
                else:
                    raise JSONDataSourceFile(
                        "value", "datasource",
                        '%s:%s' % (self.file_list, self.path_list)
                    )

            # when defined => has to be present
            if self.schema_file:
                if not self.schema_file.is_file():
                    raise JSONDataSourceFile("open", "schema_file",
                                             str(self.schema_file))

                self.set_schema(schema_file=self.schema_file)

        logger.debug("self.path_list=%s", self.path_list)
        logger.debug("self.file_list=%s", self.file_list)
        logger.debug("self.file_path_list=%s", self.file_path_list)
        logger.debug("self.schema_file=%s", self.schema_file)

        #
        # load data, therefore search data files within path_list
        #
        configuration_ok = False
        onenok = False
        import_kwargs = {}

        if not self.data_file:  # No explicit given
            if self.file_path_list:
                for f in self.file_path_list:
                    if self.json_import(self.branch, None, f, self.schema_file,
                                        **import_kwargs):
                        configuration_ok = True
                    else:
                        onenok = True

                if not configuration_ok:  # base loaded only
                    if not self.requires:  # there is a rule
                        if self.requires == 'base':
                            # is mandatory, reaching this means is OK
                            pass
                        else:
                            raise JSONDataSourceFile(
                                "value", "datasource",
                                '%s:%s:%s' % (self.file_path_list,
                                              self.file_list,
                                              self.path_list)
                            )

                else:  # at least one application configuration loaded
                    if self.requires:
                        # there is a rule
                        if self.requires == 'all':
                            # no exeception allowed
                            if onenok:
                                # one has failed
                                raise JSONDataSourceFile(
                                    "value", "datasource",
                                    '%s:%s:%s' % (self.file_path_list,
                                                  self.file_list,
                                                  self.path_list)
                                )
                        elif self.requires == 'base':
                            # is mandatory, reaching this means is OK
                            pass
                        elif self.requires == 'one':
                            # reaching this means is OK
                            pass

        else:
            if self.data_file.exists():
                if not self.schema_file and self.schema:
                    import_kwargs['schema'] = self.schema
                self.json_import(self.branch, None, self.data_file,
                                 self.schema_file, **import_kwargs)

    def json_export(self, source_node, filename, **kwargs):
        """
        Exports current data for later import.

        The exported data is a snapshot of current state.

        Args:
            filename: File name for the exported data.

            source_node: Base of sub-tree for export.
                None for complete JSON document.

            **kwargs:
                JSON dump keyword arguments.

        Returns:
            When successful returns 'True', else returns either 'False',
            or raises an exception.

        Raises:
            JSONDataTargetFile:
        """
        if not source_node:
            source_node = self.data

        try:
            with open(filename, 'w') as fp:
                myjson.dump(source_node, fp, **kwargs)
        except Exception as e:
            raise JSONDataTargetFile("open-%s" % e, "data.dump", str(filename))

        return True

    def json_import(self, target_node, key, data_file, schema_file=None,
                    validator=None, schema=None, match_condition=(), **kwargs):
        """
        Imports and validates JSON based data.

        The contained data in 'data_file' could be either the initial data
        tree, or a new branch defined by a fresh tree structure. The
        'targetnode' defines the parent container where the new branch has
        to be hooked-in.

        Args:
            target_node:
                Target container for the inclusion of the loaded branch.
                For the default:='None' the 'self.data' is used.
            key:
                The hook within the targetnode,
            data_file:
                JSON data filename containing the subtree for the target branch.
            schema_file:
                JSON-Schema filename for validation of the subtree/branch.
            validator: [default, draft3, off, ]
                Sets schema validator for the data file.
                The values are: default=validate, draft3=Draft3Validator,
                off=None.

                default:= validate
            match_condition:
                Defines the criteria for comparison of present child nodes
                in the target container. The value is a list of criteria
                combined by logical AND. The criteria may vary due to
                the requirement and the type of applied container.

                For information on applicable values refer to:
                    'JSONDataSerializer.is_applicable()'

        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.

        Raises:
            JSONData:

            JSONDataValue:

            JSONDataSourceFile:

        """
        logger.debug("json_import:data_file=%s", data_file)
        logger.debug("json_import:schema_file=%s", schema_file)

        validator = validator or self.validator

        if validator is not SchemaMode.OFF:
            # validation requested, requires schema
            if not schema_file:  # no new import, use present data
                if not self.schema:  # no schema data present
                    raise JSONDataException("value", "schema", self.schema)
            else:
                schema_file = Path(schema_file).resolve()
                if not schema_file.is_file():
                    raise JSONDataSourceFile("open", "schema_file",
                                             str(schema_file))
                with open(schema_file) as schema_file:
                    schema = myjson.load(schema_file)
                if not schema:
                    raise JSONDataSourceFile("read", "schema_file",
                                             str(schema_file))

        # INPUT-BRANCH: data
        data_file = Path(data_file).resolve()
        if not data_file.is_file():
            raise JSONDataSourceFile("open", "data_file", str(data_file))
        try:
            with open(data_file) as data_file:  # load data
                json_data = myjson.load(data_file)
        except Exception as e:
            raise JSONDataSourceFile("open", "data_file",
                                     str(data_file), str(e))
        if not json_data:
            raise JSONDataSourceFile("read", "data_file", str(data_file))

        # INPUT-BRANCH: validate data
        self.validate(json_data, schema, validator)

        #
        # TARGET-CONTAINER: manage new branch data
        #
        if not target_node:  # use defaults
            if not self.data:  # the initial load, thus OK in any case
                self.data = json_data
            ret = json_data is not None
        else:  # data history present, so decide how to handle
            # Checks that the branch fits into the target container
            if not self.is_applicable(target_node, key, json_data,
                                      match_condition):
                return False

            ret = self.branch_add(target_node, key, json_data)

        return ret  # json_data != None

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
                                    "source_file=%s" % source_file,
                                    "source=%s" % source)
        if source_file:
            with open(source_file) as f:
                source = myjson.load(f)
        elif not source:
            source = self.data  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def print_schema(self, pretty=True, source_file=None, source=None):
        """Prints structured schema.

        Args:
            pretty: Activates pretty printer for treeview, else flat.

            source_file: Loads schema from 'source_file' into 'source'.
                
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
        if source_file and source:
            raise JSONDataAmbiguity('source_file/source',
                                    "source_file=%s" % source_file,
                                    "source=%s" % source)
        if source_file:
            with open(source_file) as f:
                source = myjson.load(f)
        elif not source:
            source = self.schema  # yes, almost the same...

        if pretty:
            print(myjson.dumps(source, indent=self.indent))
        else:
            print(myjson.dumps(source))

    def set_schema(self, schema_file=None, target_node=None, data_file=None,
                   validator=None, schema=None, persistent=False):
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
        logger.debug("set_schema:schema_file=%s" % schema_file)

        data_file = Path(data_file).resolve() if data_file else None
        validator = validator or self.validator

        if schema_file is not None:  # change filename
            self.schema_file = Path(schema_file).resolve()
        elif self.schema_file is not None:  # use present
            schema_file = self.schema_file
        elif data_file is not None:  # derive coallocated from config
            schema_file = self.data_file.with_suffix('.jsd').resolve()
            if not schema_file.is_file():
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
            self.schema_file = schema_file
            if not schema_file.is_file():
                raise JSONDataSourceFile("open", "schema_file",
                                         str(schema_file))
            with open(schema_file) as schema_file:
                schema = myjson.load(schema_file)
            if schema is None:
                raise JSONDataSourceFile("read", "schema_file",
                                         str(schema_file))

        else:  # missing at all
            raise JSONDataSourceFile("open", "schema_file", str(schema_file))

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
                    '%s!=%s' % (type(target_node), type(schema))
                )
            self.branch_add(target_node, schema)

        return schema is not None

from .pointer import JSONPointer
# avoid nested recursion problems
