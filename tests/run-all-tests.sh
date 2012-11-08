#!/bin/bash

set -e 

. "./tests-helper-functions.sh"

TARGET_SITE="http://test.fizlesh.ru"

echo "$0 started on `date +%Y-%m-%d-%H:%M:%S`"

for TEST in ./xcms-*.py; do
	run_test $TEST
done