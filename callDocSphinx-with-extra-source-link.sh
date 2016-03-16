PROJECT='jsondata'
VERSION="0.0.8"
RELEASE="0.0.8"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='pre-alpha'
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

echo "sys.path.insert(0, os.path.abspath('$PWD/..'))" >> ${OUTDIR}/apidoc/conf.py

# put the packages together
{
cat <<EOF

'jsondata' - package
********************

.. toctree::
   :maxdepth: 4

.. automodule:: jsondata

'jsondata.JSONDataSerializer' - Module 
======================================

.. automodule:: jsondata.JSONDataSerializer
Constants:
----------

  **Choices for branch operations**:

    * BRANCH_SET_REPLACE = 0: replaces the complete set of branches.
    
    * BRANCH_SUPERPOSE = 1: drops-in the child nodes of the source into the target

    * BRANCH_ADD = 2: similar to superpose, but does not replace existing

    * BRANCH_REMOVE = 3: removes a node

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

    * DEFAULT = 1: Use default: jsonschema.validator(Draft4Validator)

    * DRAFT3 = 2: Use draft3:jsonschema.Draft3Validator

  **Match criteria for node comparison**:

   * MATCH_INSERT = 0: for dicts

   * MATCH_NO = 1: negates the whole set

   * MATCH_KEY = 2: for dicts

   * MATCH_CHLDATTR = 3: for dicts and lists

   * MATCH_INDEX = 4: for lists

   * MATCH_MEM = 5: for dicts(value) and lists


Class: JSONDataSerializer
-------------------------
\`jsondata.JSONDataSerializer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>\`_
		
.. autoclass:: JSONDataSerializer

Attributes
^^^^^^^^^^

   * JSONDataSerializer.data: JSON object data tree.

   * JSONDataSerializer.schema: JSONschema object data tree.


Methods:
^^^^^^^^

__init__
""""""""
	\`jsondata.JSONDataSerializer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>\`_

	.. automethod:: JSONDataSerializer.__init__

__str__
"""""""
	.. automethod:: JSONDataSerializer.__str__
                                                                                                                                                                                                
__repr__
""""""""
	.. automethod:: JSONDataSerializer.__repr__

add
"""
	\`jsondata.JSONDataSerializerError.add [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.add>\`_
		
	.. automethod:: JSONDataSerializer.add
		
copy
""""
	\`jsondata.JSONDataSerializerError.copy [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.copy>\`_

	.. automethod:: JSONDataSerializer.copy

diff
""""
	\`jsondata.JSONDataSerializerError.diff [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.diff>\`_

	.. automethod:: JSONDataSerializer.diff

delete_data
"""""""""""
	\`jsondata.JSONDataSerializerError.delete_data [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.delete_data>\`_

	.. automethod:: JSONDataSerializer.delete_data

export_data
"""""""""""
	\`jsondata.JSONDataSerializerError.export_data [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.export_data>\`_
	
	.. automethod:: JSONDataSerializer.export_data

getNodeForPointer
"""""""""""""""""
	\`jsondata.JSONDataSerializerError.getNodeForPointer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.getNodeForPointer>\`_

	.. automethod:: JSONDataSerializer.getNodeForPointer

getPointerForNode
"""""""""""""""""
	\`jsondata.JSONDataSerializerError.getPointerForNode [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.getPointerForNode>\`_

	.. automethod:: JSONDataSerializer.getPointerForNode

import_data
"""""""""""
	\`jsondata.JSONDataSerializerError.import_data [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.import_data>\`_

	.. automethod:: JSONDataSerializer.import_data

isApplicable
""""""""""""
	\`jsondata.JSONDataSerializerError.isApplicable [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.isApplicable>\`_

	.. automethod:: JSONDataSerializer.isApplicable

printData
"""""""""
	\`jsondata.JSONDataSerializerError.printData [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.printData>\`_

	.. automethod:: JSONDataSerializer.printData

printSchema
"""""""""""
	\`jsondata.JSONDataSerializerError.printSchema [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.printSchema>\`_

	.. automethod:: JSONDataSerializer.printSchema
        
remove
""""""
	\`jsondata.JSONDataSerializerError.remove [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.remove>\`_

	.. automethod:: JSONDataSerializer.remove

replace
"""""""
	\`jsondata.JSONDataSerializerError.replace [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.replace>\`_

	.. automethod:: JSONDataSerializer.replace

replace_set
"""""""""""
	\`jsondata.JSONDataSerializerError.replace_set [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.replace_set>\`_

	.. automethod:: JSONDataSerializer.replace_set

set_schema
""""""""""
	\`jsondata.JSONDataSerializerError.set_schema [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.set_schema>\`_

	.. automethod:: JSONDataSerializer.set_schema

superpose
"""""""""
	\`jsondata.JSONDataSerializerError.superpose [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.superpose>\`_

	.. automethod:: JSONDataSerializer.superpose

test
""""
	\`jsondata.JSONDataSerializerError.test [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.test>\`_

	.. automethod:: JSONDataSerializer.test


'jsondata.JSONPointer' - Module 
======================================

.. automodule:: jsondata.JSONPointer

Class: JSONPointer
-------------------
\`jsondata.JSONPointer [source] <_modules/jsondata/JSONPointer.html#JSONPointer>\`_
		
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
	\`jsondata.JSONPointer [source] <_modules/jsondata/JSONPointer.html#JSONPointer>\`_

	.. automethod:: JSONPointer.__init__

get_node
""""""""
	.. automethod:: JSONPointer.get_node

get_path
""""""""
	.. automethod:: JSONPointer.get_path

get_raw
"""""""
	.. automethod:: JSONPointer.get_raw

__repr__
""""""""
	.. automethod:: JSONPointer.__repr__

__str__
"""""""
	.. automethod:: JSONPointer.__str__


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


'jsondata.JSONDataPatch' - Module 
======================================

.. automodule:: jsondata.JSONDataPatch

Class: JSONDataPatch
--------------------
\`jsondata.JSONDataPatch [source] <_modules/jsondata/JSONDatapatch.html#JSONDataPatch>\`_
		
.. autoclass:: JSONDataPatch

Class: JSONPatch
----------------
\`jsondata.JSONPatch [source] <_modules/jsondata/JSONPatch.html#JSONPatch>\`_
		
.. autoclass:: JSONPatch

Attributes
^^^^^^^^^^

**JSONPatch**:

* JSONDataPatch.data: JSONPatch object data tree.

Methods:
^^^^^^^^

__init__
""""""""
	\`jsondata.JSONPatch [source] <_modules/jsondata/JSONPatch.html#JSONPatch>\`_

	.. automethod:: JSONPatch.__init__

__str__
"""""""
	.. automethod:: JSONPatch.__str__
                                                                                                                                                                                                
__repr__
""""""""
	.. automethod:: JSONPatch.__repr__

add_item
""""""""
	\`jsondata.JSONPatch.add_item [source] <_modules/jsondata/JSONPatch.html#JSONPatch.add_item>\`_

	.. automethod:: JSONPatch.add_item

add_patch
"""""""""
	\`jsondata.JSONPatch.add_patch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.add_patch>\`_

	.. automethod:: JSONPatch.add_patch

apply_patch
"""""""""""
	\`jsondata.JSONPatch.apply_patch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.apply_patch>\`_

	.. automethod:: JSONPatch.apply_patch

createPatch
"""""""""""
	\`jsondata.JSONPatch.createPatch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.createPatch>\`_

	.. automethod:: JSONPatch.createPatch

export_patch
""""""""""""
	\`jsondata.JSONPatch.export_patch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.export_patch>\`_

	.. automethod:: JSONPatch.export_patch

import_patch
""""""""""""
	\`jsondata.JSONPatch.import_patch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.import_patch>\`_

	.. automethod:: JSONPatch.import_patch

merge_patch
"""""""""""
	\`jsondata.JSONPatch,merge_patch [source] <_modules/jsondata/JSONPatch.html#JSONPatch.merge_patch>\`_

	.. automethod:: JSONPatch.merge_patch


'jsondata.Selftest' - Module 
============================

.. automodule:: jsondata.Selftest

Functions:
^^^^^^^^^^

runselftest
"""""""""""
	\`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#runselftest>\`_

	.. autofunction:: runselftest

case00
""""""
	\`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#case00>\`_

	.. autofunction:: case00

case01
""""""
	\`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#case01>\`_

	.. autofunction:: case01

case02
""""""
	\`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#case02>\`_

	.. autofunction:: case02

case03
""""""
	\`jsondata.Selftest [source] <_modules/jsondata/Selftest.html#case03>\`_

	.. autofunction:: case03


Exceptions: JSONDataSerializerError*
------------------------------------

The current implementation is not hierarchical, thus does not
fully provide the advances of inherited exception types. 

Error
^^^^^
\`jsondata.JSONDataSerializerError [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerError>\`_

.. autoclass:: JSONDataSerializerError

ErrorAmbiguity
^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorAmbiguity [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorAmbiguity>\`_

.. autoclass:: JSONDataSerializerErrorAmbiguity

ErrorAttribute
^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorAttribute [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorAttribute>\`_

.. autoclass:: JSONDataSerializerErrorAttribute 

ErrorAttributeValue
^^^^^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorAttributeValue [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorAttributeValue>\`_

.. autoclass:: JSONDataSerializerErrorAttributeValue 

ErrorSourceFile
^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorSourceFile [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorSourceFile>\`_

.. autoclass:: JSONDataSerializerErrorSourceFile 

ErrorSourceFileReason
^^^^^^^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorSourceFileReason [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorSourceFileReason>\`_

.. autoclass:: JSONDataSerializerErrorSourceFileReason

ErrorSourceFromAll
^^^^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorSourceFromAll [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorSourceFromAll>\`_

.. autoclass:: JSONDataSerializerErrorSourceFromAll 

ErrorSourceFromList
^^^^^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorSourceFromList [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorSourceFromList>\`_

.. autoclass:: JSONDataSerializerErrorSourceFromList

ErrorTargetFile
^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorTargetFile [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorTargetFile>\`_

.. autoclass:: JSONDataSerializerErrorTargetFile

ErrorTargetFileReason
^^^^^^^^^^^^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorTargetFileReason [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorTargetFileReason>\`_

.. autoclass:: JSONDataSerializerErrorTargetFileReason 

ErrorValue
^^^^^^^^^^
\`jsondata.JSONDataSerializerErrorValue [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializerErrorValue>\`_

.. autoclass:: JSONDataSerializerErrorValue 

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

'jsondata' - Modular JSON by trees and branches - JSONPointer and JSONPatch 
===========================================================================

The 'jsondata' package provides the management of modular data structures based on JSON. 
The data is represented by in-memory tree structures with dynamically added
and/or removed branches. The data could be validated by JSON schemas, and stored 
for later reuse.

Current version supports for first features of JSONPointer and JSONPatch. 
The following versions are going to support the full scope in accordance 
RFC6901, and RFC6902. The syntax primitives of underlying layers are provided 
by the imported packages 'json' and 'jsonschema' in conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

This document provides the developer information for the API, and the 
documentation of the PyUnit tests as examples and application patterns.

* Commandline tools.

  * jsondatacheck: validates and presents JSON data

  * jsondiff: displays the differences, similar to 'diff'

  * jsonpatch: applies patches, similar to 'patch'

  For help on the command line tools call e.g.:: 

    jsondatacheck --help



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
echo "display with: firefox ${DOCHTML}"
echo
