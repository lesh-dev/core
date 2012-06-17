#!/bin/bash

# Checks that no tabs uses in code
set -xe

path="."

check_tabs()
{
    if find $path -type f -name $1 | xargs grep $'\t' ; then
        echo "Tabs check failed for xcms files, see files above. "
        exit 1
    fi
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

check_shorttag
check_tabs '*.xcms'
check_tabs '*.php'
check_tabs '*.code'
