#!/bin/bash

grep -o -P -h "$@" 'u"[^\"]+"' xcms_*.py | sort | uniq -d -c
