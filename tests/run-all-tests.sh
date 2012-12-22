#!/bin/bash

set -e 

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
	shift;
	echo "Syntax: $0 [target-site] [-c|--continue]"
	echo "Flag '-c': run whole test suite, even if some tests failed. "
	exit 1
fi

CONTINUE="NO"
if [ "$1" == "-c" ] || [ "$1" == "--continue" ]; then
	shift;
	echo "Continue-on-fail mode ON"
	CONTINUE="YES"
fi

TARGET_SITE="$1"
if [ -z "$TARGET_SITE" ]; then
	TARGET_SITE="test.fizlesh.ru"
	echo "No test site parameter passed, using default: $TARGET_SITE"
else
	shift;
fi

source "./tests-helper-functions.sh"

echo "$0 started on `date +%Y-%m-%d-%H:%M:%S`"

python test-suite.py
