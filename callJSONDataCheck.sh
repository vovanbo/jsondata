PROJECT='jsondata-tests'
VERSION="00.00.003"
RELEASE="00.00.003"
AUTHOR='Arno-Can Uestuensoez'

export PYTHONPATH=$PYTHONPATH:$PWD
MYPATH=${BASH_SOURCE%/*}/

X=$*
if [ "X${X}" != "X${X#*-- }" ];then
	CALL="python ${X%%-- *} ${MYPATH}bin/jsondatacheck  ${X##*-- }"
else
	CALL="python ${MYPATH}bin/jsondatacheck ${@}"
	if [ "X${X}" != "X${X#*-h}"  -o "X${X}" != "X${X#*--help}" ];then
		_HELP=1
	fi
fi

helpOnWrapper () {
	cat <<EOF
SYNOPSIS:
  ${0##*/} [OPTIONS]

DESCRIPTION: CALL-WRAPPER
  The "${0##*/}" is a slim call wrapper for R&D with a few settings.
  The main task is to provide the current context for the 
    "jsondatacheck.py"
  by temporary setting of PYTHONPATH.

OPTIONS:
  [python-options]
    See REMARKS.

  [jsondatacheck.py-options]
    See REMARKS.
 
REMARKS:
  Python options could be passed through the wrapper by the call:

    ${0##*/} <python-pass-trough-options> -- <jsondatacheck-options>

  resulting in:

    python <python-pass-trough-options> jsondatacheck <jsondatacheck-options>

AUTHOR:
  Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

COPYRIGHT:
  Copyright (C) 2015,2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

LICENSE:
  For the wrapper itself: Apache-2.0

EOF
	read -p "For help on 'jsondatacheck' press [yY]:"
	case $REPLY in
		[yY])$CALL;;
	esac
}

if [ "X${_HELP}" == "X1" ];then
	helpOnWrapper
	exit 0
fi
echo "CALL=<$CALL>"
$CALL
ret=$?
if [ $ret -eq 0 -a "X${_HELP}" == "X1" ];then
	helpOnWrapper
fi
