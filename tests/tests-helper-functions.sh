#!/bin/bash

run_test()
{
	if [ -z "$1" ]; then
		echo "Parameters not specified for run_test()"
		exit 1
	fi
	if [ -z "$TARGET_SITE" ]; then
		echo "Error: TARGET_SITE variable is not set. Your test wrapper is incorrect. "
		exit 1
	fi
	
	echo "========== Running test $1 =========="
	if ! python $1 "$TARGET_SITE"; then
		echo "Test $1 FAILED";
		return 1
	else
		echo "Test $1 PASSED"
		return 0
	fi
}
