#!/bin/bash
find . -type f | xargs enca -L russian |  grep 1251
