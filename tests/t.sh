#!/usr/bin/env bash
rm -f *.pyc
PYTHONDONTWRITEBYTECODE=1 python ./test-suite.py "$@"
