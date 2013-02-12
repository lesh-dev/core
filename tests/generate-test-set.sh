#!/bin/bash

# this script is used to create Python test suite from all existing tests.
# usage: ./$0

TESTS=`ls -1 xcms_*.py`

if [ "$?" -ne "0" ]; then
	echo "Tests not found";
	exit 1
fi

set -e

TEST_SET="./auto_test_set.py"
if [ -r "$TEST_SET" ]; then
	chmod +w "$TEST_SET"
	mv "$TEST_SET" "$TEST_SET.bak"
fi

echo "This file is AUTO-GENERATED. Do not edit it directly, edit generator instead. " > "$TEST_SET"

echo " " >> "$TEST_SET"

ls -1 $TESTS | sed s@'.py$'@@  | sed s@xcms_@'import xcms_'@ >> "$TEST_SET"

echo "def getTests(baseUrl, args): return [" >> "$TEST_SET"
grep -m 1 'class Xcms' $TESTS | sed s@'.py:class '@'.'@ | sed s@'\s*(\s*SeleniumTest\s*)\s*:'@'(baseUrl, args),'@ >> "$TEST_SET"

echo "]" >> "$TEST_SET"
echo >> "$TEST_SET"

chmod +x-w "$TEST_SET"
echo "Successfully updated test suite $TEST_SET. Now you may run main test suite test-suite.py (or use generated test set somewhere else)"
