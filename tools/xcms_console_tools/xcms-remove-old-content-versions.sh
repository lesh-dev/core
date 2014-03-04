#!/usr/bin/env bash
set -e 
# This helper script removes all old content versions from specified directory.

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
	echo "This script lists all 'very old' content versions from specified XCMS content directory. "
	echo "It leaves some recent versions (20 by default). "
	echo "Syntax: $0 <xcms-content-dir> [number-of-versions-to-leave]"
	exit 1
fi

CONTENT_DIR="$1"

if ! [ -d "$CONTENT_DIR" ];  then
	echo "Error: specified path '$CONTENT_DIR' does not exists or is not a directory. "
	exit 1
fi

CONTENT_DIR="`cd $CONTENT_DIR; pwd`"

shift;

COUNT=20

if ! [ -z "$1" ]; then
	COUNT="$1"
#	echo "Set remaining version count to $COUNT"
fi


PAGES="$CONTENT_DIR/cms/pages"

if ! [ -d "$PAGES" ]; then
	echo "Seems that we are not in XCMS Content directory: cannot find 'pages' subdirectory. "
	exit 1
fi

DIR_LIST=`find "$PAGES" -type d`

for DIR in $DIR_LIST; do
	#echo "Old version files in $DIR:"
	VERSIONS=`find "$DIR" -maxdepth 1 -name "content-version-*.gz" -type f`
	#echo "VER=$VERSIONS"
	if [ -z "$VERSIONS" ]; then
		continue
	fi
	
	TO_DELETE=`ls -1 -r -t $VERSIONS | head -n "-$COUNT"`
	if [ -z "$TO_DELETE" ]; then
		continue
	fi
	
	ls -1 $TO_DELETE
done




