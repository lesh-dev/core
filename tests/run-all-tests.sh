#!/bin/bash

set -e 

run_test()
{
	echo "Running test $1"
	python $1
}

for i in ./*.py; do
	run_test xcms-open-non-existing.py
done