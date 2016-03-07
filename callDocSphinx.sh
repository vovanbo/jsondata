PROJECT='jsondata'
VERSION="0.0.7"
RELEASE="0.0.7"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='pre-alpha'
MISSION='Provide and extend JSONPointer and JSONPatch - RFC6901, RFC6902'
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

'jsondata' - Modul 
==================

.. toctree::
   :maxdepth: 4

.. automodule:: jsondata

Class: JSONDataSerializer
-------------------------
\`jsondata.JSONDataSerializer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>\`_
		
.. autoclass:: JSONDataSerializer

Attributes
^^^^^^^^^^

**JSON and JSONschema**:

* JSONDataSerializer.data: JSON object data tree.

* JSONDataSerializer.schema: JSONschema object data tree.

**Choices for branch operations**:

* BRANCH_SET_REPLACE = 0: replaces the complete set of branches.
    
* BRANCH_SUPERPOSE = 1: drops-in the child nodes of the source into the target

* BRANCH_ADD = 2: similar to superpose, but does not replace existing

* BRANCH_REMOVE = 3: removes a node

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
		
delete_data
"""""""""""
	\`jsondata.JSONDataSerializerError.delete_data [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.delete_data>\`_

	.. automethod:: JSONDataSerializer.delete_data

export_data
"""""""""""
	\`jsondata.JSONDataSerializerError.export_data [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer.export_data>\`_
	
	.. automethod:: JSONDataSerializer.export_data

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

Exceptions: JSONDataSerializerError*
------------------------------------

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


Indices and tables
==================

* :ref:\`genindex\`
* :ref:\`modindex\`
* :ref:\`search\`


*REMARK*: The master format of current documentation is PyDoc, thus the HTML formatting
is supported with a few inline macros only.


EOF
} > ${OUTDIR}/apidoc/sphinx/jsondata_doc.rst

#
# static - literal data
STATIC="${OUTDIR}/apidoc/sphinx/_static"
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

This document provide the developer information for the API, and the 
PyUnit tests as examples and application patterns.

* jsondatacheck

  For help on the command line interface call onlinehelp:: 

    jsondatacheck --help


.. toctree::
   :maxdepth: 4

   jsondata_doc.rst
   tests

* setup.py

  For help on extensions to standard options call onlinehelp:: 

    python setup.py --help-jsondata


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



Indices and tables
==================

* :ref:\`genindex\`
* :ref:\`modindex\`
* :ref:\`search\`


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
