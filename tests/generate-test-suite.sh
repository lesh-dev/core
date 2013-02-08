#!/bin/bash

# this script is used to create Python test suite from all existing tests.
# usage: ./$0

TESTS=`ls -1 xcms_*.py`

if [ "$?" -ne "0" ]; then
	echo "Tests not found";
	exit 1
fi

set -e


HEADER="./test-aux/test-suite-header.py"
if ! [ -r "$HEADER" ]; then
	echo "$HEADER not found. "
fi

TEST_SUITE="./auto-test-suite.py"
if [ -r "$TEST_SUITE" ]; then
	chmod +w "$TEST_SUITE"
	mv "$TEST_SUITE" "$TEST_SUITE.bak"
fi

cat "$HEADER" > "$TEST_SUITE"

echo " " >> "$TEST_SUITE"

ls -1 $TESTS | sed s@'.py$'@@  | sed s@xcms_@'import xcms_'@ >> "$TEST_SUITE"

echo "tests = [" >> "$TEST_SUITE"
grep -m 1 'class Xcms' $TESTS | sed s@'.py:class '@'.'@ | sed s@'\s*(\s*SeleniumTest\s*)\s*:'@'(baseUrl),'@ >> "$TEST_SUITE"

echo "]" >> "$TEST_SUITE"
echo >> "$TEST_SUITE"

FOOTER="./test-aux/test-suite-footer.py"
if ! [ -r "$FOOTER" ]; then
	echo "$FOOTER not found. "
fi
cat "$FOOTER" | grep -v "^##" >> "$TEST_SUITE"

sed -i s@'##auto_generated_warning_placeholder##'@'WARNING! This file is AUTO-GENERATED. Do not edit it directly, edit header/footer/generator instead.'@ "$TEST_SUITE"
chmod +x-w "$TEST_SUITE"
echo "Created test suite $TEST_SUITE"
