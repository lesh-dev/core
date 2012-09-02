#!/bin/bash

# Checks that no tabs uses in code
#set -xe

path="."
my_base="`dirname $0`"

check_style()
{
    for i in `find $path -type f -name $1`; do
        echo "*** Checking '$i'"
        $my_base/check.py $i
    done
    return 0
}

# TODO: check cr/lf symbols in code

check_style '*.xcms'
check_style '*.php'
check_style '*.code'
