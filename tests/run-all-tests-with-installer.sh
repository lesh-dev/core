#!/bin/bash

set -e 

TARGET_SITE="http://test.fizlesh.ru"
TEST_LOG="$0.log"

echo "$0 started on `date +%Y-%m-%d-%H:%M:%S`"

. "./tests-helper-functions.sh"

echo "Reverting test installation to initial state. "

ssh tech@fizlesh.ru "sudo publish testing reset"

echo "Running installer test"

run_test "test-installer.py"

bash "./run-all-tests.sh"
