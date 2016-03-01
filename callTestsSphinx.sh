PROJECT='jsondata-tests'
VERSION="00.00.003"
RELEASE="00.00.003"
AUTHOR='Arno-Can Uestuensoez'

MYPATH=${BASH_SOURCE%/*}/
if [ "X${MYPATH#./}" != "X$MYPATH" ];then
	MYPATH=${PWD}${MYPATH#.}
fi
INDIR=${MYPATH}tests/
OUTDIR=~/tmp/bld/data-objects/data-objects-core/doc/sphinx/
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}" 
fi
export PYTHONPATH=$PYTHONPATH:$PWD:${MYPATH}:${MYPATH}tests


FILEDIRS=""
FILEDIRS="$FILEDIRS ${INDIR}"
#FILEDIRS="$FILEDIRS ${INDIR}a_selftest"
#FILEDIRS="$FILEDIRS ${INDIR}b_system"
#FILEDIRS="$FILEDIRS ${INDIR}c_libs"
#FILEDIRS="$FILEDIRS ${INDIR}testlib"
#FILEDIRS="$FILEDIRS ${INDIR}utils"

CALL=""
CALL="$CALL export PYTHONPATH=$PYTHONPATH;"
CALL="$CALL sphinx-apidoc "
CALL="$CALL -A '$AUTHOR'"
CALL="$CALL -H '$PROJECT'"
CALL="$CALL -V '$VERSION'"
CALL="$CALL -R '$RELEASE'"
CALL="$CALL -o ${OUTDIR}/testdoc"
CALL="$CALL $@"
CALL="$CALL ${FILEDIRS} "

DOCHTML=${OUTDIR}testdoc/_build/html/index.html
cat <<EOF
#
# Create apidoc builder...
#
EOF
echo "CALL=<$CALL>"
eval $CALL
echo "sys.path.insert(0, os.path.abspath('$PWD/../src'))" >> ${OUTDIR}/testdoc/conf.py


#CALL="SPHINXOPTS= "
CALL=" "
CALL="$CALL cd ${OUTDIR}/testdoc;"
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
