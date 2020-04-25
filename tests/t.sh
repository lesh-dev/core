#!/usr/bin/env bash
#rm -f logs/*.log
rm -f *.pyc
PYTHONDONTWRITEBYTECODE=1 python2 ./test-suite.py "$@"
