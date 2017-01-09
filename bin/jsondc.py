# -*- coding: utf-8 -*-
"""A command line interface for the validation of JSON based data.

The command line interface is implemented as a front-end for the package
'jsondata'.

The interface provides a callable generic validator(default:=Draft4) for arbitrary
JSON data files. The validation is performed with a main JSON schema file linking 
additional sub-configuration for an optional set of an arbitrary number of branches.
It provides the validation of JSON based data/files by their corresponding JSONschemas.
The call interface is Linux/Unix command line standard - on other supported OS too - 
with a few conventions related to default values of file names and paths.

The application of this call interface is mainly intended for the purposes::
1. as a developer utility for the development of JSON based data
2. as a user tool in order to enumerate the list of actually 
   used JSON sources
3. as a user tools in order to verify the present JSON data
4. as a automation and test tool for various JSON specifications,
   and JSON based applications

Therefore the assembly of data tree models with basic branch functions 
in accordance/complance to RFC6901 and RFC6902 is provided for the 
incremental setup and serialization of JSON data.

When no explicit filenames are provided the following convention is applied
as default:

    appname: "-a"
        "JSONobjects"

    JSON-schema: "-s"
        dirname(__file__)/<appname>.jsd ("jsondata.jsd")

    JSON-data: "-c"
        <appname>.json ("jsondata.json")

    Search-path-data: "-p"
        Search path for JSON-data - refer to __file__=JSONData/Serializer.py:
        default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/

SYNOPSIS:
  jsondc [OPTIONS]

OPTIONS:
  -a, --appname= <appname>
     Name of application.
     default: jsondc
  -c, --configfile= <configfile>
     A single configuration file including path with JSON data.
     default: jsondc.json
  -D, --print-data
     Pretty print data.
  -f --filelist= <list-of-filenames>
     List of colon seperated filenames to be searched for. These 
     could be relative pathnames too.
     default:=[<appname>.json]
  -j, --json= (json|ujson)
      Use as scanner and parser one of the verified packages:
          'json': standard package
          'ujson': ultra-json for performance, check platform availability,
              and eventually run unit tests.
  -n, --no-default-path
     Supress load of default path.
     default: False
  -N, --no-sub-data
     Supress load of sub-data files, e.g. from plugins.
     default: False
  -p, --pathlist= <search-path-JSON-data>
     Search path for JSON data file(s), standard list for current platform.
     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -P, --plugins-pathlist= <search-path-JSON-data-branches>
     Search path for JSON data file(s) to be inserted as additional branches,
     standard list for current platform.
     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -s, --schemafile= <schemafile>
     Schema file - JSONschema.
     default: jsondc.jsd
  -S, --print-schema
     Pretty print schema.
  -V, --validator= <validator>
     Alternate validator provided by module 'jsonschema'
     - default: validate
     - draft3: Draft3Validator
     - off: None
    default:= validate

  -i, --interactive
     Dialog mode, displays formatted for interactive JSON and 
     JSONschema design.
      
  -d, --debug
     Debug entries, does NOT work with 'python -O ...'.
     Developer output, aimed for filtering.
  -v, --verbose
     Verbose, some relevant states for basic analysis.
     When '--selftest' is set, repetition raises the display level.
     
  --selftest
     Performs a basic functional selftest by load, verify, and validate.
     0. jsondata/data.json + jsondata/schema.jsd
     1. jsondata/selftest.json + jsondata/selftest.jsd

  --version
     Current version - terse.
  --Version
     Current version - detailed.

  -h, --help
     This help.

PYTHON OPTIONS:
  -O, -OO
   Eliminates '__debug__' code.
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.12'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'


try:
    from jsondata.JSONDataSerializer import JSONDataSerializer as ConfigData
except Exception as e:
    print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+")\n#\n"
    import sys
    sys.exit(1)
# name of application, used for several filenames as default
_APPNAME = "jsondc"

#
#--- fetch options
#
import getopt, sys, os
 
def usage():
    if __name__ == '__main__':
        import pydoc
        #FIXME: literally displayed '__main__'
        print pydoc.help(__name__)
    else:
        help(str(os.path.basename(sys.argv[0]).split('.')[0]))

_kargs={}
try:
    _longopts = [
        "help","debug","verbose","version","Version",
        "appname=", "configfile=","schemafile=","validator=","no-default-path",
        "no-sub-data","pathlist=","plugins-pathlist=","print-schema","print-data",
        "interactive", "filelist=",
        "selftest", "json="
    ]
    _opts, _args = getopt.getopt(sys.argv[1:], "a:c:f:j:is:np:P:NDShdvV:", _longopts)
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

_appname = _APPNAME

_selftest = False
_verbose = 0

for _o,_a in _opts:
    if _o == "--selftest":
        _selftest = True
    elif _o in ("-a","--appname"):
        _appname = _a
    elif _o in ("-c","--configfile"):
        _kargs['configfile'] = _a
    elif _o in ("-D","--print-data"):
        _kargs['printdata'] = True
    elif _o in ("-f","--filelist"):
        _kargs['filelist'] = _a.split(":")

    elif _o in ("-j","--json"):
        if _a == 'ujson':
            import ujson as myjson
            #_myjson = 'ujson'
        else:
            import json as myjson
            #_myjson = 'json'
        #import importlib
        #i = importlib.import_module(_myjson)

    elif _o in ("-n","--no-default-path"):
        _kargs['nodefaultpath'] = True
    elif _o in ("-N","--no-sub-data"):
        _kargs['nosubdata'] = True
    elif _o in ("-p","--pathlist"):
        _kargs['pathlist'] = _a
    elif _o in ("-P","--plugins-pathlist"):
        _kargs['pluginspathlist'] = _a
    elif _o in ("-s","--schemafile"):
        _kargs['schemafile'] = _a
    elif _o in ("-S","--print-schema"):
        _kargs['printschema'] = True
    elif _o in ("-V","--validator"):
        _kargs['validator'] = _a

    elif _o in ("-i", "--interactive"):
        _kargs['interactive'] = True

    elif _o in ("-d","--debug"):
        _kargs['debug'] = True
    elif _o in ("-v","--verbose"):
        _verbose += 1
        
    elif _o in ("-h","--help"):
        usage()
        sys.exit()

    elif _o in ("--version"):
        print str(__version__)
        sys.exit()
    elif _o in ("--Version"):
        print "app:      "+str(_APPNAME)
        print "version:  "+str(__version__)
        print "author:   "+str(__author__)
        print "copyright:"+str(__copyright__)
        print "license:  "+str(__license__)
        print "file:     "+str(os.path.basename(__file__))
        sys.exit()

    else:
        assert False, "unhandled option"

if _selftest:
    try:
        from jsondata.Selftest import runselftest
    except Exception as e:
        print "\n#\n#*** Set 'PYTHONPATH' ("+str(e)+"\n"
        print "\n#sys.path="+str(sys.path)+"\n#\n"

    # name of application, used for several filenames as default
    _appname = "selftest"
    if _verbose>0:
        _kargs['_verbose'] = _verbose 
    stest = runselftest(_appname,**_kargs)
else:
    if _verbose>0:
        _kargs['verbose'] = True 
    configdata = ConfigData(_appname,**_kargs)
