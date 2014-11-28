#!/usr/bin/env bash

cat site/VERSION
git push
git push --tags
git push ssh://dev.fizlesh.ru//srv/git/lesh
git push --tags ssh://dev.fizlesh.ru//srv/git/lesh
