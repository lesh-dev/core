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

echo "tests to run: "
ls -1 ./xcms-*.py

FAILED_COUNT=0
PASSED_COUNT=0

for TEST in ./xcms-*.py; do
	if ! run_test $TEST; then
		if [ "$CONTINUE" == "YES" ]; then
			FAILED_COUNT=`expr $FAILED_COUNT + 1`
			continue
		else
			exit 1
		fi
	else
		PASSED_COUNT=`expr $PASSED_COUNT + 1`
	fi
done

echo "Tests passed: $PASSED_COUNT, failed: $FAILED_COUNT. "

if [ $FAILED_COUNT -ge 0 ]; then
	exit 1
fi
