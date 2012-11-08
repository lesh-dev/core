#!/bin/bash

# this script prepares test host: makes initial state

set -e 

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
	echo "This script creates new test environment on test.fizlesh.ru using preproduction recipe."
	exit 1
fi

ssh tech@fizlesh.ru "sudo publish preproduction"
ssh tech@fizlesh.ru "sudo publish testing"




