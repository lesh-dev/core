#!/usr/bin/env bash

fix_file()
{
    perl -p -e "$1" $file > $file.tmp
    if diff $file.tmp $file ; then
        mv $file.tmp $file
        echo "FIXED $file"
    else
        rm $file.tmp
    fi
}

fix_ext()
{
    echo "Fixing "$1"..."
    L="$( find . -name "$1" )"
    for i in $L; do
        fix_file "$i"
    done
}

fix_ext "*.xcms"
fix_ext "*.code"
fix_ext "*.php"
