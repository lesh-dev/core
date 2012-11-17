#!/bin/bash

set -e 

TARGET_SITE="http://test.fizlesh.ru"

echo "$0 started on `date +%Y-%m-%d-%H:%M:%S`"

bash "./run-installer-test.sh" "$TARGET_SITE"

bash "./run-all-tests.sh" "$TARGET_SITE"
