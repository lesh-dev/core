#!/bin/bash

set -e 

TARGET_SITE="http://test.fizlesh.ru"

LOG="test.log"

run_test()
{
	echo "========== Running test $1 ==========" >> "$LOG"
	if ! python $1 "$TARGET_SITE" >> "$LOG"; then
		echo "Test $1 FAILED";
	else
		echo "Test $1 PASSED"
	fi
	
}

echo "Test suite started on `date +%Y-%m-%d-%H:%M:%S`" > "$LOG"

for TEST in ./xcms-*.py; do
	run_test $TEST
done