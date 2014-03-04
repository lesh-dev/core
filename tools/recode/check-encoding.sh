#!/usr/bin/env bash
find . -type f -size +0 | egrep -v '(\.pdf|\.jpg|\.png|\.jpeg|\.gz|\.gif|\.ico|\.avi|\.bz2)' | xargs \
    enca -L russian | egrep '(1251|Unrecognized)'
