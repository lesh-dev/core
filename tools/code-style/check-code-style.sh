#!/bin/bash

# Checks that no tabs uses in code
set -xe

path="."
my_base="`dirname $0`"

check_tabs()
{
    for i in `find $path -type f -name $1`; do
        echo "*** Checking '$i'"
        $my_base/check.py $i
    done
    return 0
}

check_shorttag()
{
    if grep -RI '<[?][^px]' $path || grep -RI '<[?]$' ../../site ; then
        echo "shorttag check failed, please fix"
        exit 1
    fi
    return 0
}

# TODO: check cr/lf symbols in code

check_shorttag
check_tabs '*.xcms'
check_tabs '*.php'
check_tabs '*.code'
