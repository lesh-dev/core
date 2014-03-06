#!/usr/bin/env bash

# cleans old page versions

if [ -z "$1" ]; then
    echo "Usage: $0 <directory-to-clean-versions> [versions-to-keep]"
    exit 1
fi

SEARCH_DIR="`cd $1; pwd`"

shift

ARC_VERSIONS=5

if [ -n "$1" ]; then
    ARC_VERSIONS="$1"
fi

echo "Cleaning versions in $SEARCH_DIR"

cleanup_dir()
{
    if ! [ -r "$DIR/content" ]; then
        echo "Directory $DIR has no content, skipping. "
        return 0
    fi
    if ! ls $DIR/content-version*gz &>/dev/null; then
        return 0
    fi
    echo "Cleaning version in directory $DIR"
    #ls -1t $DIR/content-version*gz
    ls -1t $DIR/content-version*gz | head -n "-$ARC_VERSIONS" | xargs rm -f
}

DIRS=`find "$SEARCH_DIR" -type d`
for DIR in $DIRS; do
    cleanup_dir $DIR
done
