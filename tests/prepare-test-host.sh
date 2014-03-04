#!/usr/bin/env bash

# this script prepares test host: makes initial state

set -e

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "This script creates new test environment on test.fizlesh.ru using 'rc' recipe."
    exit 1
fi

tech_ssh="ssh tech@fizlesh.ru"

$tech_ssh "sudo publish rc"
$tech_ssh "sudo publish testing"

echo "Testing prepared successfully"
