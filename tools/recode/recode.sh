#!/usr/bin/env bash

set -e

for i in $(find -type f | grep -v recode); do
    #echo $i
    enca $i | grep 1251  1> /dev/null
    if [ "$?" == "0" ]; then
        cp $i recode
        cat recode | enconv > $i
    fi
done
