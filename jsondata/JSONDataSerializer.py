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

"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.7'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import os,sys

version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

import json, jsonschema
from StringIO import StringIO

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
    the main hooks 'data', and 'schema'.

    Attributes:
        data: The data tree of JSON based objects provided by the
            module 'json'.
        schema: The validator for 'data' provided by the module
            'jsonschema'.

    Attribute-Constants:
        branchoperations:
            BRANCH_SET_REPLACE(0):    Replace all previous loaded branches.

            BRANCH_SUPERPOSE(1):      Creates, or maps onto present by
                                      replacing.

            BRANCH_ADD(2):            Creates, does not replace.

            BRANCH_REMOVE(3):         Deletes.

        types of validator:
            OFF(0):                   Validation disabled.

            DEFAULT(1):               Default validator, jsonchema.validator().

            DRAFT3(2):                Default validator, jsonchema.draft3validator().

        match criteria for node comparison:
            MATCH_INSERT(0):          Common, insertion is applicable.

            MATCH_NO(1):              Negates all criteria. E.g. the condition
                                        [MATCH_NO, MATCH_KEY]
                                      matches when the keys are absent.

            MATCH_KEY(2):             For dicts.

            MATCH_CHLDATTR(3):        For dicts and lists.

            MATCH_INDEX(4):           For lists.

            MATCH_MEM(5):             For dicts(value) and lists.
    """

    # Choices for branch operations
    BRANCH_SET_REPLACE = 0 
    """replaces the complete set of branches."""
    
    BRANCH_SUPERPOSE = 1
    """drops-in the child nodes of the source into the target"""
    
    BRANCH_ADD = 2
    """similar to superpose, but does not replace existing"""

    BRANCH_REMOVE = 3
    """removes a node"""

    # types of validator
    OFF = 0
    """No validation."""
    
    DEFAULT = 1
    """Use default: jsonschema.validator"""
    
    DRAFT3 = 2
    """Use draft3:jsonschema.Darft3Validator"""
    
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

    def __init__(self,appname,*args,**kargs):
        """ Loads and validates a JSON definition with the corresponding schema file.

        Args:
            appname: Name of the application

            args*: Optional position parameters, these replace corresponding key
                 parameters.
                filelist, pathlist, filepathlist, schemafile
            **kargs:
                branchoperations: [add, remove, replace-set, superpose, ]
                    Defines the behavior for for the load of data when redundant
                    tree parts exist.
                        set-replace: BRANCH_SET_REPLACE(0)
                            Replace all previous loaded branches.
                        superpose: BRANCH_SUPERPOSE(1)
                            Creates, or maps onto present by replacing.
                        add: BRANCH_ADD(2)
                            Creates, does not replace.
                        remove: BRANCH_REMOVE(3)
                            Deletes.
                    default:= replace-object
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

        # The internal object schema for the framework - a fixed set of files as final default.
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
        self.branchoperations = JSONDataSerializer.BRANCH_SUPERPOSE
        self.data = None
        self.schema = None
        self.nodefaultpath = False
        self.nodesubdata = False
        self.requires = False
        self.indent = 4
        self.validator = JSONDataSerializer.DEFAULT

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
                if v == 'replace-set' or v == JSONDataSerializer.BRANCH_SET_REPLACE:
                    self.branchoperations = JSONDataSerializer.BRANCH_SET_REPLACE
                elif v == 'superpose' or v == JSONDataSerializer.BRANCH_SUPERPOSE:
                    self.branchoperations = JSONDataSerializer.BRANCH_SUPERPOSE
                elif v == 'add' or v == JSONDataSerializer.BRANCH_ADD:
                    self.branchoperations = JSONDataSerializer.BRANCH_ADD
                elif v == 'remove' or v == JSONDataSerializer.BRANCH_REMOVE:
                    self.branchoperations = JSONDataSerializer.BRANCH_REMOVE
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
                if v == 'default' or v == JSONDataSerializer.DEFAULT:
                    self.validator = JSONDataSerializer.DEFAULT
                elif v == 'draft3' or v == JSONDataSerializer.DRAFT3:
                    self.validator = JSONDataSerializer.DRAFT3
                elif v == 'off' or v == JSONDataSerializer.OFF:
                    self.validator = JSONDataSerializer.OFF
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'verbose':
                self.verbose = v
            elif __debug__:
                if k == 'debug':
                    self.debug = v
            elif k == 'interactive':
                _interactive = v
                
        # positional parameters dominate, remaining are default
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
            for i in range(0,len(self.pathlist)):
                self.pathlist[i]  = os.path.expanduser(self.pathlist[i])
                self.pathlist[i]  = os.path.expandvars(self.pathlist[i])

        else: # a PATH like variable
            if not self.nodefaultpath:
                # Fixed set of data files as the final default.
                self.pathlist += os.path.dirname(afile)+os.sep+'etc'+os.sep+appname+os.sep+os.pathsep+os.sep+'etc'+os.sep+os.pathsep+"$HOME"+os.sep+'etc'+os.sep
            self.pathlist  = os.path.expanduser(self.pathlist)
            self.pathlist  = os.path.expandvars(self.pathlist)
            self.pathlist  = self.pathlist.split(os.pathsep)

        for i in range(0,len(self.pathlist)):
            self.pathlist[i]  = os.path.abspath(self.pathlist[i])
            self.pathlist[i]  = os.path.realpath(self.pathlist[i])

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
        if not self.schema and self.validator != JSONDataSerializer.OFF:
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
                    if self.import_data(f,self.schemafile,self.branch,**kx):
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
                self.import_data(self.datafile,self.schemafile,self.branch,**kx)

        # display data to stdout
        if printschema:
            self.printSchema()
        if printdata:
            self.printData()

    def __repr__(self):
        """Dump data.
        """
        io = StringIO()
        json.dump(self.data, io)
        return io.getvalue()

    def __str__(self):
        """Dumps data by pretty print.
        """
        return json.dumps(self.data, indent=self.indent)

    def add(self, targetnode, branch, matchcondition=None):
        """Adds a branch into a target structure.

        The present previous values are kept untouched, non-existent
        nodes are added.

        Args:
            targetnode: Target tree where the source is to be inserted.

            branch: Source branch to be inserted into target tree.

            matchcondition: Defines the condition for applicability
                of the add method. For the provided values refer to
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

            # add does not replace, just adds non-present
            if not matchcondition:
                matchcondition = [JSONDataSerializer.MATCH_NO,JSONDataSerializer.MATCH_KEY]
            else:
                matchcondition.append(JSONDataSerializer.MATCH_NO)

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

    def delete_data(self, datafile=None, schemafile=None,targetnode=None, **kargs):
        """ Deletes branches from JSON based data trees with static and dynamic criteria.

        The 'delete_data' function enables for extended checks of deletion, e.g the
        detection of modified data, whereas the 'remove' function simply removes
        by a subset of some static checks with 'isApplicable' validation.

        Handles several scenarios of plausibility and applicability checks.

        0. Just do it:
            delete_data(None, None,None)
                Deletes self.data
            delete_data(None, None,targetnode)
                Deletes targetnode
        1. Check datafile for applicability, no schema validation:
            delete_data(datafile, None,None)
                Deletes self.data
            delete_data(datafile, None,targetnode)
                Deletes targetnode
        2. Check datafile for applicability, with schemafile validation:
            delete_data(datafile, schemafile,None)
                Deletes self.data
            delete_data(datafile, schemafile,targetnode)
                Deletes targetnode
        3. Check datafile for applicability, with schema validation:
            kargs={'schema':"<jsonschema-object>"}

            delete_data(datafile, None,None,**kargs)
                Deletes self.data
            delete_data(datafile, None,targetnode,**kargs)
                Deletes targetnode

        REMARK: Due to the huge amount of shared code with 'import_data',
            this function is internally mapped to 'import_data'.

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
                branchoperations: [remove,]
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
        if kargs.get('branchoperations',JSONDataSerializer.BRANCH_REMOVE) != JSONDataSerializer.BRANCH_REMOVE:
            raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))

        if __debug__:
            if self.debug:
                print "DBG:delete_data:datafile=  "+str(datafile)
                print "DBG:delete_data:schemafile="+str(schemafile)
        return self.import_data(datafile, schemafile, targetnode, **kargs)

    def export_data(self, fname, base=None, **kargs):
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

    def import_data(self, datafile, schemafile=None,targetnode=None, **kargs):
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
                branchoperations: [add, replace-set, superpose, remove,]
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
        if __debug__:
            if self.debug:
                print "DBG:import_data:datafile=  "+str(datafile)
                print "DBG:import_data:schemafile="+str(schemafile)

        jval = None
        sval = None
        matchcondition = []

        #
        #*** Fetch parameters
        #
        branchoperations = self.branchoperations # use class settings as default
        validator = self.validator # use class settings as default
        for k,v in kargs.items():
            if k == 'branchoperations':
                if v == 'replace-set' or v == JSONDataSerializer.BRANCH_SET_REPLACE:
                    branchoperations = JSONDataSerializer.BRANCH_SET_REPLACE
                elif v == 'superpose' or v == JSONDataSerializer.BRANCH_SUPERPOSE:
                    branchoperations = JSONDataSerializer.BRANCH_SUPERPOSE
                elif v == 'add' or v == JSONDataSerializer.BRANCH_ADD:
                    branchoperations = JSONDataSerializer.BRANCH_ADD
                elif v == 'remove' or v == JSONDataSerializer.BRANCH_REMOVE:
                    branchoperations = JSONDataSerializer.BRANCH_REMOVE
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'matchcondition':
                #For now just passed through to self.isApplicable()
                if v == 'key' or v == JSONDataSerializer.MATCH_KEY:
                    matchcondition.append(JSONDataSerializer.MATCH_KEY)
                elif v == 'no' or v == JSONDataSerializer.MATCH_NO:
                    matchcondition.append(JSONDataSerializer.MATCH_NO)
                elif v == 'child_attr_list' or v == JSONDataSerializer.MATCH_CHLDATTR:
                    matchcondition.append(JSONDataSerializer.MATCH_CHLDATTR)
                elif v == 'index' or v == JSONDataSerializer.MATCH_INDEX:
                    matchcondition.append(JSONDataSerializer.MATCH_INDEX)
                elif v == 'mem' or v == JSONDataSerializer.MATCH_MEM:
                    matchcondition.append(JSONDataSerializer.MATCH_MEM)
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == JSONDataSerializer.DEFAULT:
                    validator = JSONDataSerializer.DEFAULT
                elif v == 'draft3' or v == JSONDataSerializer.DRAFT3:
                    validator = JSONDataSerializer.DRAFT3
                elif v == 'off' or v == JSONDataSerializer.OFF:
                    validator = JSONDataSerializer.OFF
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'schema':
                sval = v

        # INPUT-BRANCH: schema for validation
        if validator != JSONDataSerializer.OFF: # validation requested, requires schema
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
        if validator == JSONDataSerializer.DEFAULT:
            jsonschema.validate(jval, sval)
        elif validator == JSONDataSerializer.DRAFT3:
            jsonschema.Draft3Validator(jval, sval)
        elif validator != JSONDataSerializer.OFF:
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
            if branchoperations == JSONDataSerializer.BRANCH_SET_REPLACE:
                ret = self.replace_set(targetnode,jval,matchcondition)
            elif branchoperations == JSONDataSerializer.BRANCH_SUPERPOSE:
                ret = self.superpose(targetnode,jval,matchcondition)
            elif branchoperations == JSONDataSerializer.BRANCH_ADD:
                ret = self.add(targetnode,jval,matchcondition)
            elif branchoperations == JSONDataSerializer.BRANCH_REMOVE:
                ret = self.remove(targetnode,jval,matchcondition)
            else:
                raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))

        if self.verbose:
            print "VALID: json.datafile:   '"+str(datafile)+"'"
            print "VALID: json.schemafile: '"+str(schemafile)+"'"

        return ret # jval != None

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
            if v == 'key' or v == JSONDataSerializer.MATCH_KEY:
                _matchcondition.append(JSONDataSerializer.MATCH_KEY)
            elif v == 'no' or v == JSONDataSerializer.MATCH_NO:
                _matchcondition.append(JSONDataSerializer.MATCH_NO)
            elif v == 'child_attr_list' or v == JSONDataSerializer.MATCH_CHLDATTR:
                _matchcondition.append(JSONDataSerializer.MATCH_CHLDATTR)
            elif v == 'index' or v == JSONDataSerializer.MATCH_INDEX:
                _matchcondition.append(JSONDataSerializer.MATCH_INDEX)
            elif v == 'mem' or v == JSONDataSerializer.MATCH_MEM:
                _matchcondition.append(JSONDataSerializer.MATCH_MEM)
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
            _matchcondition = [JSONDataSerializer.MATCH_INSERT]

        if JSONDataSerializer.MATCH_NO in _matchcondition:
            retFailed = True
            retOK = False
        else:
            retFailed = False
            retOK = True

        for m in _matchcondition:
            if m == JSONDataSerializer.MATCH_NO: # handles multiple, does not need alist.remove()
                continue
            elif m == JSONDataSerializer.MATCH_INSERT:
                if not type(targetnode) in (dict,list):
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
            elif m == JSONDataSerializer.MATCH_KEY:
                if type(targetnode) != dict:
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                for k in branch.keys():
                    if not targetnode.get(k):
                        return retFailed
            elif m == JSONDataSerializer.MATCH_CHLDATTR:
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
            elif m == JSONDataSerializer.MATCH_INDEX:
                if type(targetnode) != list:
                    raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
                if len(targetnode) > len(branch):
                    return retFailed
            elif m == JSONDataSerializer.MATCH_MEM:
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

    def replace_set(self, targetnode, branch, matchcondition=None):
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
                targetnode.remove(v)
            targetnode.extend(branch)

        else:
            raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))
        return ret

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
                branchoperations: [append, add, prepend, replace-object,
                    replace-set, superpose, ]
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
        branchoperations = self.branchoperations # use class settings as default
        validator = self.validator # use class settings as default
        persistent = False
        schema = None
        for k,v in kargs.items():
            if k == 'branchoperations':
                if v == 'replace-set' or v == JSONDataSerializer.BRANCH_SET_REPLACE:
                    branchoperations = JSONDataSerializer.BRANCH_SET_REPLACE
                elif v == 'superpose' or v == JSONDataSerializer.BRANCH_SUPERPOSE:
                    branchoperations = JSONDataSerializer.BRANCH_SUPERPOSE
                elif v == 'add' or v == JSONDataSerializer.BRANCH_ADD:
                    branchoperations = JSONDataSerializer.BRANCH_ADD
                elif v == 'remove' or v == JSONDataSerializer.BRANCH_REMOVE:
                    branchoperations = JSONDataSerializer.BRANCH_REMOVE
                else:
                    raise JSONDataSerializerErrorAttributeValue(k,str(v))
            elif k == 'validator': # controls validation by JSONschema
                if v == 'default' or v == JSONDataSerializer.DEFAULT:
                    validator = JSONDataSerializer.DEFAULT
                elif v == 'draft3' or v == JSONDataSerializer.DRAFT3:
                    validator = JSONDataSerializer.DRAFT3
                elif v == 'off' or v == JSONDataSerializer.OFF:
                    validator = JSONDataSerializer.OFF
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

            if branchoperations == JSONDataSerializer.BRANCH_SET_REPLACE:
                # just accept any by simply removing previous
                if targetnode == self.data: # it is a complete replace
                    self.data = schema
                    targetnode = schema
                else: # it is a partial replace of a subset
                    targetnode = schema
            elif branchoperations == JSONDataSerializer.BRANCH_SUPERPOSE:
                self.superpose(targetnode,schema)
            elif branchoperations == JSONDataSerializer.BRANCH_ADD:
                self.add(targetnode,schema)
            elif branchoperations == JSONDataSerializer.BRANCH_REMOVE:
                self.remove(targetnode,schema)
            else:
                raise JSONDataSerializerErrorAttributeValue("branchoperations",str(self.branchoperations))

        if self.verbose:
            print "VALID: json.schemafile: '"+str(schemafile)+"'"

        return schema != None

    def superpose(self, targetnode, branch, matchcondition=None):
        """Superposes a complete branch into a target structure.

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
        else:
            raise JSONDataSerializerError("Type not applicable:"+str(type(targetnode)))

        return ret

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

    def remove(self, targetnode, branch, matchcondition=None):
        """Removes a branch from a target structure by basic static criteria.

        The corresponding elements of the 'source' tree are removed from
        the tree 'targetnode'. The remaining are kept untouched. For tree
        nodes as leafs the whole corresponding subtree is deleted.

        REMARK: No reference checks are done, so the user is responsible
            for additional references.

        Args:
            targetnode: Target tree where the source is to be removed.

            branch: Source branch to be removed from the target tree.

            matchcondition: Defines the condition for applicability
                of the remove method. For the provided values refer
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
                    if self.isApplicable(targetnode, [v], JSONDataSerializer.BRANCH_REMOVE):
                        targetnode.remove(v)
                    else:
                        ret = False
                else:
                    targetnode.remove(v)

        else:
            raise JSONDataSerializerError("Type not supported:type="+str(branch))
        return ret
