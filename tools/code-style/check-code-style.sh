#!/bin/bash

# Checks that no tabs uses in code
#set -xe

path="."
my_base="`dirname $0`"
fail=

check_style()
{
    for i in `find $path -type f -name $1`; do
        if ! $my_base/check.py $i > /tmp/check-result ; then
            echo "*** Checking '$i' failed:"
            cat /tmp/check-result
            echo
            echo
            fail="yes"
        fi
    done
    return 0
}

check_style '*.xcms'
check_style '*.php'
check_style '*.code'
check_style '*.sh'

if [ "$fail" == "yes" ] ; then
    echo "Code style checking failed, see the output for details"
    exit 1
fi