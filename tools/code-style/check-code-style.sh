#!/bin/bash
# We should not ignore any errors, it's better to fail
# Please do not remove the following line
set -e

# Runs python-based code style checker

path="."
my_base="`dirname $0`"
fail=

# ignore list (contrib files whose code style
# we don't want to verify
ignore_list="class.phpmailer.php"

check_style()
{
    for i in `find $path -type f -name "$1"`; do
        # skip ignored files
        ib="`basename $i`"
        for b in $ignore_list ; do
            if [ "$ib" == "$b" ] ; then
                ignore="yes"
                break
            fi
        done
        if [ "$ignore" == "yes" ] ; then
            continue
        fi
        # check files
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