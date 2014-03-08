#!/usr/bin/env bash

# cleans old page versions

if [ -z "$1" ]; then
    echo "Usage: $0 <directory-to-clean-versions> [-n|--nothing] [-v|--verbose] [versions-to-keep]"
    exit 1
fi

SEARCH_DIR="`cd $1; pwd`"

shift

COMMAND="rm -f"

if [ "$1" == "-n" ] || [ "$1" == "--nothing" ]; then
    COMMAND="ls -1"
    shift
fi

if [ "$1" == "-v" ] || [ "$1" == "--verbose" ]; then
    VERBOSE="1"
    shift
fi

ARC_VERSIONS=5

if [ -n "$1" ]; then
    ARC_VERSIONS="$1"
fi

if [ "$VERBOSE" == "1" ]; then
    echo "Cleaning versions in $SEARCH_DIR"
fi    

cleanup_dir()
{
    local DIR="$1"

    if ! [ -r "$DIR/content" ]; then
        if [ "$VERBOSE" == "1" ]; then
            echo "Directory $DIR has no content file, skipping. " 1>&2
        fi
        return 0
    fi
    if ! ls $DIR/content-version*gz &>/dev/null; then
        return 0
    fi
    if [ "$VERBOSE" == "1" ]; then
        echo "Cleaning version in directory $DIR"
    fi
    #ls -1t $DIR/content-version*gz
    TO_REMOVE="`ls -1rt $DIR/content-version*gz | head -n "-$ARC_VERSIONS"`"
    if [ -n "$TO_REMOVE" ]; then
        $COMMAND $TO_REMOVE
    fi
}

DIRS=`find "$SEARCH_DIR" -type d`
for DIR in $DIRS; do
    cleanup_dir $DIR
done

