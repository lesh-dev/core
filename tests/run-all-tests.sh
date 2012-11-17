#!/bin/bash

set -e 

TARGET_SITE="$1"
if [ -z "$TARGET_SITE" ]; then
	TARGET_SITE="test.fizlesh.ru"
	echo "No test site parameter passed, using default $TARGET_SITE"
fi

. "./tests-helper-functions.sh"

echo "$0 started on `date +%Y-%m-%d-%H:%M:%S`"

echo "tests to run: "
ls -1 ./xcms-*.py

for TEST in ./xcms-*.py; do
	run_test $TEST
done