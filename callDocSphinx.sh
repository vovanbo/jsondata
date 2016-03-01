PROJECT='jsondata'
VERSION="00.00.003"
RELEASE="00.00.003"
AUTHOR='Arno-Can Uestuensoez'

MYPATH=${BASH_SOURCE%/*}/
INDIR=${MYPATH}/
#OUTDIR=~/tmp/bld/data-objects/data-objects-core/doc/sphinx/
OUTDIR=build/sphinx/
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}" 
fi
export PYTHONPATH=$PYTHONPATH:$PWD:$MYPATH


FILEDIRS=""
FILEDIRS="${INDIR}jsondata"
FILEDIRS="$FILEDIRS ${INDIR}bin"
FILEDIRS="$FILEDIRS ${INDIR}tests"

CALL=""
CALL="$CALL export PYTHONPATH=$PYTHONPATH;"
CALL="$CALL sphinx-apidoc "
CALL="$CALL -A '$AUTHOR'"
CALL="$CALL -H '$PROJECT'"
CALL="$CALL -V '$VERSION'"
CALL="$CALL -R '$RELEASE'"
CALL="$CALL -o ${OUTDIR}/apidoc"
CALL="$CALL -f -F "
CALL="$CALL $@"

DOCHTML=${OUTDIR}apidoc/_build/html/index.html
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

Welcome to jsondata's documentation!
====================================

This document provides the developer information for the API of the runtime package
and the included PyUnit tests. 
The Unit tests here serve in particular as examples and application pattern.
Therefore these are included in the developer documentation. 

Contents:

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
} > ${OUTDIR}/apidoc/index.rst


#CALL="SPHINXOPTS= "
CALL=" "
#CALL="SPHINXBUILD=sphinx-build PYTHONPATH=$PYTHONPATH "
CALL="$CALL cd ${OUTDIR}/apidoc;"
CALL="$CALL export PYTHONPATH=$PYTHONPATH "
CALL="$CALL ;make html "
CALL="$CALL ;cd - "
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
