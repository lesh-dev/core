#!/bin/bash

# Checks that no tabs uses in code
set -xe

check_files()
{
    if find ../../site -type f -name $1 | xargs grep $'\t' ; then
        echo "Code style check failed for xcms files, see files above. "
        exit 1
    fi
    return 0
}

check_files '*.xcms'
check_files '*.php'
check_files '*.code'
