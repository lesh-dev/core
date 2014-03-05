#!/usr/bin/env bash

# this script prepares test host: makes initial state

set -e

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    cat <<EOF
This script creates new test environment on test.fizlesh.ru using 'rc' recipe.
Usage: $0 [options]
Options are:
    -c|--clear-db        Perform database cleanup on testing instance
EOF
    exit 1
fi

tech_ssh="ssh tech@fizlesh.ru"

$tech_ssh "sudo publish rc"
$tech_ssh "sudo publish testing"

if [ "$1" = "-c" ] || [ "$1" = "--clear-db" ] ; then
    $tech_ssh "sudo publish init-test-db"
fi

echo "Testing prepared successfully"
