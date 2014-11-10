#!/usr/bin/env bash

cat site/VERSION
git push ssh://dev.fizlesh.ru//srv/git/lesh
git push --tags ssh://dev.fizlesh.ru//srv/git/lesh
