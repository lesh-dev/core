#!/bin/bash

# Checks that no tabs uses in code
set -xe

check_tabs()
{
    if find ../../site -type f -name $1 | xargs grep $'\t' ; then
        echo "Tabs check failed for xcms files, see files above. "
        exit 1
    fi
    return 0
}

check_shorttag()
{
    if grep -RI '<?[^px]' ../../site ; then
        echo "shorttag check failed, please fix"
        exit 1
    fi
    return 0
}

check_shorttag
check_tabs '*.xcms'
check_tabs '*.php'
check_tabs '*.code'
