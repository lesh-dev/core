#!/usr/bin/env bash

# this script prepares test host: makes initial state

set -e

print_usage()
{
    cat <<EOF
This script creates new test environment on test.fizlesh.ru using 'rc' recipe.
Usage: $0 [options]
Options are:
    -c|--clear-db        Perform database cleanup on testing instance
    -h|--help            This help
EOF
    exit 1
}


while [ -n "$1" ] ; do
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        print_usage
    elif [ "$1" = "-c" ] || [ "$1" = "--clear-db" ] ; then
        init_test_db=yes
        shift || true
        continue
    else
        echo "Unknown option '$1'"
        print_usage
    fi
done

site="--site fizlesh.ru"
tech_ssh="ssh tech@fizlesh.ru"

$tech_ssh "sudo publish $site rc" || ( echo "RC publishing FAILED" && exit 1 )
$tech_ssh "sudo publish $site testing" || ( echo "Testing publising FAILED" && exit 1 )

if [ -n "$init_test_db" ] ; then
    $tech_ssh "sudo publish $site init-test-db"
fi

echo "Testing prepared successfully"
