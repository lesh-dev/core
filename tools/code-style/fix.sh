#!/usr/bin/env bash
set -e

regex="$1"

fix_file()
{
    file="$1"
    tmp_file=${file}.tmp
    if ! [ -e "$file" ]; then
        return 0
    fi
    perl -p -e "$regex" $file > $tmp_file
    if ! diff -q $tmp_file $file ; then
        mv $tmp_file $file
        echo "FIXED $file"
    else
        rm $tmp_file
    fi
}

fix_ext()
{
    echo "Fixing $1..."
    list="$( find . -name "$1" )"
    for i in $list; do
        fix_file "$i"
    done
}

if [ -z "$regex" ] ; then
    echo "Usage: $0 <sed-replace-regex>"
    echo "  e.g: $0 s/UberPrefix/uber_prefix/g"
    exit 1
fi

fix_ext "*.xcms"
fix_ext "*.code"
fix_ext "*.php"
fix_ext "*.py"
fix_ext "*.js"
fix_ext "*.sh"
fix_ext "*.html"
fix_ext "*.css"
#fix_ext "*"
