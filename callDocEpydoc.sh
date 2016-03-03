PROJECT='jsondata'
VERSION="00.00.006"
RELEASE="00.00.006"
AUTHOR='Arno-Can Uestuensoez'
COPYRIGHT='Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
LICENSE='Artistic-License-2.0 + Forced-Fairplay-Constraints'

MYPATH=${BASH_SOURCE%/*}/
if [ "X${MYPATH#./}" != "X$MYPATH" ];then
	MYPATH=${PWD}${MYPATH#.}
fi
INDIR=${MYPATH}
#OUTDIR=~/tmp/bld/data-objects/data-objects-core/doc/epydoc/
OUTDIR=build/epydoc/
if [ ! -e "${OUTDIR}" ];then
	mkdir -p "${OUTDIR}"
fi
export PYTHONPATH=$PYTHONPATH:$PWD:${MYPATH}

FILEDIRS=""
#FILEDIRS="$FILEDIRS ${INDIR}"
FILEDIRS="$FILEDIRS `find ${INDIR}jsondata -type f -name '*.py'`"
FILEDIRS="$FILEDIRS `find ${INDIR}bin -type f -name '*.py'`"

CALL=epydoc
CALL="$CALL --graph=all"
CALL="$CALL --html"
#CALL="$CALL --pdf"
CALL="$CALL --pstat pstatfile"
CALL="$CALL -o $OUTDIR"
CALL="$CALL "
CALL="$CALL $@"
CALL="$CALL ${FILEDIRS} "
cat <<EOF
#
# Create apidoc builder...
#
EOF
echo "CALL=<$CALL>"
eval $CALL

echo
echo "call: firefox ${OUTDIR}index.html"
echo
