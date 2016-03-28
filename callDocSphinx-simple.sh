PROJECT='jsondata'
VERSION="0.2.0"
RELEASE="0.2.0"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'

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

.. jsondata documentation master file, created by
   sphinx-quickstart on `date`.
   You can adapt this file completely to your liking, but it should at least
   contain the root \`toctree\` directive.

'jsondata' - Modular JSON by trees and branches 
===============================================

This document provides the developer information for the API of the runtime
package and the included PyUnit tests.
The Unit tests here serve in particular as examples and application pattern.
Therefore these are included in the developer documentation.

.. toctree::
   :maxdepth: 4

   jsondata
   tests

Indices and tables
==================

* :ref:\`genindex\`
* :ref:\`modindex\`
* :ref:\`search\`


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
