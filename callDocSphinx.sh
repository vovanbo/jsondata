PROJECT='jsondata'
VERSION="0.2.0"
RELEASE="0.2.0"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='alpha'
MISSION='Provide and extend JSONPointer and JSONPatch - RFC6901, RFC6902'

# the absolute pathname for this source
MYPATH=${BASH_SOURCE%/*}/
if [ "X${MYPATH#.}" != "X$MYPATH" ];then
	MYPATH=${PWD}/${MYPATH#.};MYPATH=${MYPATH//\/\//\/}
fi

# input base directory
INDIR=${INDIR:-$MYPATH}
if [ "X${INDIR#.}" != "X$INDIR" ];then
	INDIR=${PWD}/${INDIR#.};INDIR=${INDIR//\/\//\/}
fi

echo "MYPATH=$MYPATH"
echo "INDIR=$INDIR"
 
# output base directory
OUTDIR=${OUTDIR:-build/}
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}"
fi
export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH

# import directory for entries of static reference 
STATIC="${OUTDIR}/apidoc/sphinx/_static"

# source entities
FILEDIRS=""
FILEDIRS="${INDIR}jsondata"
FILEDIRS="$FILEDIRS ${INDIR}bin"
FILEDIRS="$FILEDIRS ${INDIR}tests"

CALL=""
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
CALL="$CALL sphinx-apidoc "
CALL="$CALL -A '$AUTHOR'"
CALL="$CALL -H '$PROJECT'"
CALL="$CALL -V '$VERSION'"
CALL="$CALL -R '$RELEASE'"
CALL="$CALL -o ${OUTDIR}/apidoc/sphinx"
CALL="$CALL -f -F "
CALL="$CALL $@"

#
#build=patches
bin_jsondatacheck=bin/jsondatacheck
cp $bin_jsondatacheck  ${bin_jsondatacheck}.py

DOCHTML=${OUTDIR}apidoc/sphinx/_build/html/index.html
cat <<EOF
#
# Create apidoc builder...
#
EOF
IFSO=$IFS
IFS=';'
FX=( ${FILEDIRS} )
IFS=$IFSO
for fx in ${FX[@]};do
	echo "CALL=<$CALL '$fx'>"
	eval $CALL "$fx"
done

echo "extensions.append('sphinx.ext.intersphinx.')" >> ${OUTDIR}/apidoc/sphinx/conf.py
echo "sys.path.insert(0, os.path.abspath('$PWD/..'))" >> ${OUTDIR}/apidoc/sphinx/conf.py

# put the packages together
{
cat <<EOF

jsondatacheck
#############

The *jsondatacheck* commandline interface provides access to several 
tasks of the *jsondata* package, which internally rely on the standard 
packages 'json' and 'jsonschema'.
It offers access to the API of the classes and provides a selftest
option for the quick verification of the package state.
The runtime contained selftest class including it's test data serve
as an example in addition to the unit test data.

The interface provides a callable generic validator(default:=Draft4) for arbitrary
JSON data files. The validation is performed with a main JSON schema file linking 
additional sub-configuration for an optional set of an arbitrary number of branches.
It provides the validation of JSON based data/files by their corresponding JSONschemas.
The call interface is Linux/Unix command line standard - on other supported OS too - 
with a few conventions related to default values of file names and paths.

The application of this call interface is mainly intended for the purposes:

1. as a developer utility for the development of JSON based data

2. as a user tool in order to enumerate the list of actually 
   used JSON sources

3. as a user tools in order to verify the present JSON data

4. as a automation and test tool for various JSON specifications,
   and JSON based applications

5. as a selftest and environment verification for the processing
   of complex JSON data.
 
Therefore the assembly of data tree models with basic branch functions 
in accordance/complance to RFC6901 and RFC6902 is provided for the 
incremental setup, continous modification, and serialization of JSON data.

When no explicit filenames are provided the following convention is applied
as default::

    appname: "-a"
        "JSONobjects"

    JSON-schema: "-s"
        dirname(__file__)/<appname>.jsd ("jsondata.jsd")

    JSON-data: "-c"
        <appname>.json ("jsondata.json")

    Search-path-data: "-p"
        Search path for JSON-data - refer to __file__=JSONData/Serializer.py:
        default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/

**SYNOPSIS:**::

  jsondatacheck [OPTIONS]

**OPTIONS:**::
  -a --appname= <appname>
     Name of application.
     default: jsondatacheck
  -c --configfile= <configfile>
     A single configuration file including path with JSON data.

     default: jsondatacheck.json
  -D --print-data
     Pretty print data.
  -d --debug
     Debug entries, does NOT work with 'python -O ...'.
     Developer output, aimed for filtering.
  -f --filelist= <list-of-filenames>
     List of colon seperated filenames to be searched for. These 
     could be relative pathnames too.

     default:=[<appname>.json]
  -h --help
     This help.
  -i --interactive
     Dialog mode, displays formatted for interactive JSON and 
     JSONschema design.
  -n --no-default-path
     Supress load of default path.

     default: False
  -N --no-sub-data
     Supress load of sub-data files, e.g. from plugins.

     default: False
  -p --pathlist= <search-path-JSON-data>
     Search path for JSON data file(s), standard list for current platform.

     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -P --plugins-pathlist= <search-path-JSON-data-branches>
     Search path for JSON data file(s) to be inserted as additional branches,
     standard list for current platform.

     default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
  -s --schemafile= <schemafile>
     Schema file - JSONschema.

     default: jsondatacheck.jsd
  -S --print-schema
     Pretty print schema.
  -selftest --selftest

     Performs a basic functional selftest by load, verify, and validate.

     0. jsondata/data.json + jsondata/schema.jsd
     1. jsondata/selftest.json + jsondata/selftest.jsd

  -V --validator= <validator>
     Alternate validator provided by module 'jsonschema'
     - default: validate
     - draft3: Draft3Validator
     - off: None

    default:= validate
  -Version --Version
     Current version - detailed.
  -v --verbose
     Verbose, some relevant states for basic analysis.
     When '--selftest' is set, repetition raises the display level.
  -version --version
     Current version - terse.

**ENVIRONMENT**::
  * PYTHON OPTIONS:
    -O, -OO: Eliminates '__debug__' code.
 
EOF
} > ${OUTDIR}/apidoc/sphinx/jsondatacheck_doc.rst

{
cat <<EOF

'jsondata' - package
####################

.. toctree::
   :maxdepth: 4

.. automodule:: jsondata

**Sources**

* \`jsondata.JSONDataSerializer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>\`_

* \`jsondata.JSONPointer [source] <_modules/jsondata/JSONPointer.html#JSONPointer>\`_
	
* \`jsondata.JSONPatch [source] <_modules/jsondata/JSONPatch.html#JSONPatch>\`_

* \`jsondata.JSONDataExceptions [source] <_modules/jsondata/JSONDataExceptions.html#>\`_

* \`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#>\`_
		

'jsondata.JSONDataSerializer' - Module
**************************************

.. automodule:: jsondata.JSONDataSerializer

Constants:
----------

  **Compliance modes**:

    * MODE_JSON_RFC4927 = 0: Compliant to IETF RFC4927.

    * MODE_JSON_RF7951 = 2: Compliant to IETF RF7951.

    * MODE_JSON_ECMA264 = 10: Compliant to ECMA-264, refer to Chapter 15.12 The JSON Object.

    * MODE_POINTER_RFC6901 = 20: Compliant to IETF RFC6901.            

    * MODE_PATCH_RFC6902 = 30: Compliant to IETF RFC6902.            

    * MODE_SCHEMA_DRAFT3 = 43: Compliant to IETF DRAFT3.            

    * MODE_SCHEMA_DRAFT4 = 44: Compliant to IETF DRAFT4.            

  **Types of validator**:

    * OFF = 0: No validation.

    * *DEFAULT* = *DRAFT4* = 1: Default 

    * DRAFT4 = 1: Use draft4: jsonschema.validator(Draft4Validator)

    * DRAFT3 = 2: Use draft3:jsonschema.Draft3Validator

  **Match criteria for node comparison**:

   * MATCH_INSERT = 0: for dicts

   * MATCH_NO = 1: negates the whole set

   * MATCH_KEY = 2: for dicts

   * MATCH_CHLDATTR = 3: for dicts and lists

   * MATCH_INDEX = 4: for lists

   * MATCH_MEM = 5: for dicts(value) and lists

   * MATCH_NEW = 6: for the creation of new

Class: JSONDataSerializer
-------------------------
		
.. autoclass:: JSONDataSerializer

Attributes
^^^^^^^^^^

   * JSONDataSerializer.data: JSON object data tree.

   * JSONDataSerializer.schema: JSONschema object data tree.


Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONDataSerializer.__init__

__str__
"""""""
	.. automethod:: JSONDataSerializer.__str__

__repr__
""""""""
	.. automethod:: JSONDataSerializer.__repr__

branch_add
""""""""""
	.. automethod:: JSONDataSerializer.branch_add

branch_copy
"""""""""""
	.. automethod:: JSONDataSerializer.branch_copy

branch_create
"""""""""""""
	.. automethod:: JSONDataSerializer.branch_create

branch_move
"""""""""""
	.. automethod:: JSONDataSerializer.branch_move

branch_remove
"""""""""""""
	.. automethod:: JSONDataSerializer.branch_remove

branch_replace
""""""""""""""
	.. automethod:: JSONDataSerializer.branch_replace

branch_test
"""""""""""
	.. automethod:: JSONDataSerializer.branch_test

getValueNode
""""""""""""
	.. automethod:: JSONDataSerializer.getValueNode

isApplicable
""""""""""""
	.. automethod:: JSONDataSerializer.isApplicable

json_export
"""""""""""
	.. automethod:: JSONDataSerializer.json_export

json_import
"""""""""""
	.. automethod:: JSONDataSerializer.json_import

printData
"""""""""
	.. automethod:: JSONDataSerializer.printData

printSchema
"""""""""""
	.. automethod:: JSONDataSerializer.printSchema

set_schema
""""""""""
	.. automethod:: JSONDataSerializer.set_schema

Operators:
^^^^^^^^^^

'[]'
""""
	.. automethod:: JSONDataSerializer.__getitem__

Iterators:
^^^^^^^^^^

__iter__
""""""""
	.. automethod:: JSONDataSerializer.__iter__

Exceptions
----------

* \`jsondata.JSONDataAmbiguity [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataAmbiguity>\`_


'jsondata.JSONPointer' - Module
*******************************

.. automodule:: jsondata.JSONPointer

Class: JSONPointer
-------------------
.. autoclass:: JSONPointer

Attributes
^^^^^^^^^^

**JSONPointer**:

* JSONPointer.ptr: JSONPointer data.

* JSONPointer.raw: Raw input string for JSONPointer.

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONPointer.__init__

__repr__
""""""""
	.. automethod:: JSONPointer.__repr__

__str__
"""""""
	.. automethod:: JSONPointer.__str__

copy_path_list
""""""""""""""
	.. automethod:: JSONPointer.copy_path_list

get_node
""""""""
	.. automethod:: JSONPointer.get_node

get_path_list
"""""""""""""
	.. automethod:: JSONPointer.get_path_list

get_pointer
"""""""""""
	.. automethod:: JSONPointer.get_pointer

get_raw
"""""""
	.. automethod:: JSONPointer.get_raw

get_node_or_value
"""""""""""""""""
	.. automethod:: JSONPointer.get_node_or_value

Operators:
^^^^^^^^^^

    The syntax displayed for provided operators is::

      S: self
      x: parameter
      n: numerical parameter for shift operators.

    Thus the position of the opreator and parameteres is defined as follows::

      z = S + x: LHS: __add__
      z = x + S: RHS: __radd__
      S += x:    LHS: __iadd__


  
'S+x'
"""""
	.. automethod:: JSONPointer.__add__

'S==x'
""""""
	.. automethod:: JSONPointer.__eq__

'S>=x'
""""""
	.. automethod:: JSONPointer.__ge__

'S>x'
"""""
	.. automethod:: JSONPointer.__gt__

'S+=x'
""""""
	.. automethod:: JSONPointer.__iadd__

'S<x'
"""""
	.. automethod:: JSONPointer.__le__

'S<x'
"""""
	.. automethod:: JSONPointer.__lt__

'S!=x'
""""""
	.. automethod:: JSONPointer.__ne__

'x+S'
"""""
	.. automethod:: JSONPointer.__radd__

Iterators:
^^^^^^^^^^

iter_path
"""""""""
	.. automethod:: JSONPointer.iter_path

iter_path_nodes
"""""""""""""""
	.. automethod:: JSONPointer.iter_path_nodes

Exceptions
----------
* \`jsondata.JSONPointerException [source] <_modules/jsondata/JSONPointer.html#JSONPointerException>\`_


'jsondata.JSONPatch' - Module
******************************

.. automodule:: jsondata.JSONPatch

Functions:
----------

getOp
^^^^^

	.. autofunction:: getOp

Class: JSONPatch
----------------
.. autoclass:: JSONPatch

Attributes
^^^^^^^^^^

**JSONPatch**:

* JSONPatch.data: JSONPatch object data tree.

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONPatch.__init__

__str__
"""""""
	.. automethod:: JSONPatch.__str__

                                
__repr__
""""""""
	.. automethod:: JSONPatch.__repr__

__len__
"""""""
	.. automethod:: JSONPatch.__len__

apply
"""""
	.. automethod:: JSONPatch.apply

get
"""
	.. automethod:: JSONPatch.get

patch_export
""""""""""""
	.. automethod:: JSONPatch.patch_export

patch_import
""""""""""""
	.. automethod:: JSONPatch.patch_import

Operators:
^^^^^^^^^^

'[]'
""""
	.. automethod:: JSONPatch.__getitem__

'S+x'
"""""
	.. automethod:: JSONPatch.__add__

'S+=x'
""""""
	.. automethod:: JSONPatch.__iadd__

'S-=x'
""""""
	.. automethod:: JSONPatch.__isub__

'S-x'
"""""""
	.. automethod:: JSONPatch.__sub__

Iterators:
^^^^^^^^^^

__iter__
""""""""
	.. automethod:: JSONPatch.__iter__


Class: JSONPatchItem
--------------------
.. autoclass:: JSONPatchItem

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONPatchItem.__init__

__repr__
""""""""
	.. automethod:: JSONPatchItem.__repr__

__str__
"""""""
	.. automethod:: JSONPatchItem.__str__

apply
"""""
	.. automethod:: JSONPatchItem.apply


Class: JSONPatchItemRaw
-----------------------
.. autoclass:: JSONPatchItemRaw

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONPatchItemRaw.__init__


Class: JSONPatchFilter
----------------------
.. autoclass:: JSONPatchFilter

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONPatchFilter.__init__

Exceptions
----------

* \`jsondata.JSONPatchException [source] <_modules/jsondata/JSONPatch.html#JSONPatchException>\`_

* \`jsondata.JSONPatchItemException [source] <_modules/jsondata/JSONPatch.html#JSONPatchItemException>\`_


'jsondata.JSONDataExceptions' - Module
**************************************

This module contains the generic exceptions for the package 'jsondata'.

* \`jsondata.JSONDataException [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataException>\`_


* \`jsondata.JSONDataAmbiguity [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataAmbiguity>\`_

* \`jsondata.JSONDataKeyError [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataKeyError>\`_

* \`jsondata.JSONDataNodeType [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataNodeType>\`_

* \`jsondata.JSONDataSourceFile [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataSourceFile>\`_

* \`jsondata.JSONDataTargetFile [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataTargetFile>\`_

* \`jsondata.JSONDataValue [source] <_modules/jsondata/JSONDataExceptions.html#JSONDataValue>\`_



'jsondata.Selftest' - Module
****************************

.. automodule:: jsondata.Selftest

Functions:
^^^^^^^^^^

runselftest
"""""""""""
	.. autofunction:: runselftest

case00
""""""
	.. autofunction:: case00

case01
""""""
	.. autofunction:: case01

case02
""""""
	.. autofunction:: case02

case03
""""""
	.. autofunction:: case03

case04
""""""
	.. autofunction:: case04

case05
""""""
	.. autofunction:: case05

case06
""""""
	.. autofunction:: case06

 
EOF
} > ${OUTDIR}/apidoc/sphinx/jsondata_doc.rst



#
# static - literal data
cp ArtisticLicense20.html "${STATIC}"
cp licenses-amendments.txt "${STATIC}"

#
# put the packages together
{
cat <<EOF

.. jsondata documentation master file, created by
   sphinx-quickstart on `date`.
   You can adapt this file completely to your liking, but it should at least
   contain the root \`toctree\` directive.

'jsondata' - Modular processing of JSON data by trees and branches, pointers and patches 
========================================================================================

The 'jsondata' package provides the management of modular data structures based on JSON. 
The data is represented by in-memory tree structures with dynamically added
and/or removed branches. The data could be validated by JSON schemas, and stored 
for the later reuse.

The 'jsondata' package provides a standards conform layer for the processing
with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces of Python(>=2.7),
whereas higher level features of additional standards and extensions are introduced
on top. The main interface classes are:

* **JSONDataSerializer** - Core for RFC7159/RFC4627 based data structures and persistency

* **JSONPointer** - RFC6901 for addressing nodes and values

* **JSONPatch** - RFC6902 for modification of branches and values 

The syntax primitives of underlying layers are provided 
by the imported packages 'json' and 'jsonschema' in conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

Therefore the designed architecture is based on the interfaces of the packages 'json' and
'jsonschema', and compatible packages::


                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
    Data              |   +----------+     |         RFC6901
    Structures        |   | jsondata |     |         RFC6902
                      |   +----------+     |         +extensions
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+       RFC7159/RFC4267
    JSON           |    json    | jsonschema |       ECMA-262/ECMA-404    
    Syntax         |    ujson   |            |       draft-zyp-json-schema-04   
                   +------------+------------+ 
                                                     Support/verified: json, ujson
                                                        simply import package 
                                                        before 'jsondata'


The examples from the standards with some extensions, are included in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.
The current version is verified at the JSON-Syntax layer for the packages 
'json' and 'ujson'.

Current state of main features:

* RFC7159/RFC4627: Wrapper for 'json' and 'jsonschema' with file management, Alpha.

* RFC6901: JSONPointer - JSON notation, Alpha.

* RFC6901: JSONPointer - HTTP-Fragments notation(RFC3986), Alpha.

* RFC6902: JSONPatch - dynamic JSON data modification, Alpha.

* Extensions for RFC6901: Extended pointer expressions - JSON notation, Alpha.

* Extensions for RFC6902: Extended branch management, Alpha.

* Interactive JSON data design, current min-cli only, Alpha.

This document provides the developer information for the API, and the 
documentation of the PyUnit tests as examples and application patterns.

* Commandline tools.
 
  * \`jsondatacheck <jsondatacheck_doc.html>\`_ : validates and presents JSON data

  * jsondatadiff: displays the differences, similar to 'diff'

  * jsondatapatch: applies patches, similar to 'patch'

  For help on the command line tools call e.g.:: 

    jsondatacheck --help

  For quick verification of the setup and basic features call:: 

    jsondatacheck --selftest



.. toctree::
   :maxdepth: 3

   jsondata_doc.rst
   tests

* setup.py

  For help on extensions to standard options call onlinehelp:: 

    python setup.py --help-jsondata



Indices and tables
==================

* :ref:\`genindex\`
* :ref:\`modindex\`
* :ref:\`search\`


Resources
=========

For available downloads refer to:

* Python Package Index: https://pypi.python.org/pypi/jsondata

* Sourceforge.net: https://sourceforge.net/projects/jsondata/

* github.com: https://github.com/ArnoCan/jsondata/

For Licenses refer to enclosed documents:

* Artistic-License-2.0(base license): \`ArtisticLicense20.html <_static/ArtisticLicense20.html>\`_

* Forced-Fairplay-Constraints(amendments): \`licenses-amendments.txt <_static/licenses-amendments.txt>\`_ / \`Protect OpenSource Authors <http://xkcd.com/1303/>\`_

Project data summary:

* PROJECT=${PROJECT}

* MISSION=${MISSION}

* AUTHOR=${AUTHOR}

* COPYRIGHT=${COPYRIGHT}

* LICENSE=${LICENSE}

* VERSION=${VERSION}

* RELEASE=${RELEASE}

* STATUS=${STATUS}

*REMARK*: The master format of current documentation is PyDoc, thus the HTML formatting
is supported with a few inline macros only.

EOF
} > ${OUTDIR}/apidoc/sphinx/index.rst

#CALL="SPHINXOPTS= "
CALL=" "
#CALL="SPHINXBUILD=sphinx-build PYTHONPATH=$PYTHONPATH "
CALL="export SPHINXBUILD=sphinx-build; "
CALL="$CALL cd ${OUTDIR}/apidoc/sphinx;"
#CALL="$CALL export PYTHONPATH=$PYTHONPATH "
CALL="$CALL export PYTHONPATH=$PWD:$MYPATH:$PYTHONPATH;"
#CALL="$CALL export PYTHONPATH=$PYTHONPATH; "
CALL="$CALL make html ;"
CALL="$CALL cd - "
cat <<EOF
#
# Build apidoc...
#
EOF
echo "CALL=<$CALL>"
eval $CALL

echo
echo "display with: firefox -P preview.simple ${DOCHTML}"
echo

#build=patches
rm ${bin_jsondatacheck}.py
