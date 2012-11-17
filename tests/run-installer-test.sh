#!/bin/bash

set -e

TARGET_SITE="$1"
if [ -z "$TARGET_SITE" ]; then
	TARGET_SITE="test.fizlesh.ru"
	echo "No test site parameter passed, using default $TARGET_SITE"
fi
	
. "./tests-helper-functions.sh"

echo "Reverting test installation to initial state. "
ssh tech@fizlesh.ru "sudo publish testing reset"

echo "Running installer test"
run_test "test-installer.py"

