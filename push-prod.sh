#!/usr/bin/env bash

echo -n "Source version: "
cat site/VERSION
echo "Last tags:"
git tag | sort -Vr | head -n 5
echo "Pushing to github..."
git push
echo "    and tags..."
git push --tags
echo "Pushing to fizlesh.ru..."
git push ssh://fizlesh.ru//srv/git/lesh
echo "    and tags..."
git push --tags ssh://fizlesh.ru//srv/git/lesh
echo "Everything completed"
