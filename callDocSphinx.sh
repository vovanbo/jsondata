PROJECT='jsondata'
VERSION="0.2.3"
RELEASE="0.2.3"
NICKNAME="Mafumo"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'
STATUS='alpha'
MISSION='Provide and extend a comprising JSON Toolset including a JSON-DSL for computing - RFC7159, RFC6901, RFC6902, ...'

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
FILEDIRS="$FILEDIRS ${INDIR}UseCases"
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
bin_jsonproc=bin/jsonproc
cp $bin_jsonproc  ${bin_jsonproc}.py

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

# put the docs together
#
cat docsrc/index.rst                     > ${OUTDIR}/apidoc/sphinx/index.rst
{
cat <<EOF
Project data summary:

* PROJECT=${PROJECT}

* MISSION=${MISSION}

* AUTHOR=${AUTHOR}

* COPYRIGHT=${COPYRIGHT}

* LICENSE=${LICENSE}

* VERSION=${VERSION}

* RELEASE=${RELEASE}

* STATUS=${STATUS}

* NICKNAME=${NICKNAME}

  |kevinr|  \`Save the Lions <https://www.youtube.com/watch?v=0XZQYC1lHr4>\`_  

.. |kevinr| image:: _static/lionwhisperer.png 
    :target: https://www.youtube.com/watch?v=0XZQYC1lHr4
    :width: 32
    :height: 32


*REMARK*: The master format of current documentation is PyDoc, thus the HTML formatting
is supported with a few inline macros only.


EOF
} >> ${OUTDIR}/apidoc/sphinx/index.rst 

#
cat docsrc/jsondata_compute_syntax.rst   > ${OUTDIR}/apidoc/sphinx/jsondata_compute_syntax.rst
cat docsrc/jsondata_compute_syntax_examples.rst  > ${OUTDIR}/apidoc/sphinx/jsondata_compute_syntax_examples.rst
#
cat docsrc/jsondatacheck.rst             > ${OUTDIR}/apidoc/sphinx/jsondatacheck.rst
cat docsrc/jsonproc.rst                  > ${OUTDIR}/apidoc/sphinx/jsonproc.rst
#
cat docsrc/jsondata.rst                  > ${OUTDIR}/apidoc/sphinx/jsondata.rst
#
cat docsrc/jsondata_m_data.rst           > ${OUTDIR}/apidoc/sphinx/jsondata_m_data.rst
cat docsrc/jsondata_m_serializer.rst     > ${OUTDIR}/apidoc/sphinx/jsondata_m_serializer.rst
cat docsrc/jsondata_m_pointer.rst        > ${OUTDIR}/apidoc/sphinx/jsondata_m_pointer.rst
cat docsrc/jsondata_m_patch.rst          > ${OUTDIR}/apidoc/sphinx/jsondata_m_patch.rst
cat docsrc/jsondata_m_compute.rst        > ${OUTDIR}/apidoc/sphinx/jsondata_m_compute.rst
cat docsrc/jsondata_m_exceptions.rst     > ${OUTDIR}/apidoc/sphinx/jsondata_m_exceptions.rts
#
cat docsrc/jsondata_m_selftest.rst       > ${OUTDIR}/apidoc/sphinx/jsondata_m_selftest.rst

#
# static - literal data
cat ArtisticLicense20.html > "${STATIC}/ArtisticLicense20.html"
cat licenses-amendments.txt > "${STATIC}/licenses-amendments.txt"
#
cp docsrc/lionwhisperer.png "${STATIC}"

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
rm ${bin_jsonproc}.py
