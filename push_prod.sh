#!/usr/bin/env bash

echo -n "Source version: "
cat version
echo "Last tags:"
git tag | sort -Vr | head -n 5

gh_lesh="git@github.com:lesh-dev/core.git"
vm_root="ssh://fizlesh.ru//srv/git"
bb_root="ssh://hg@bitbucket.org/dichlofos"

echo "Pushing to github..."
echo "    [repo] lesh..."
git push $gh_lesh
echo "    [tags] lesh..."
git push --tags $gh_lesh
echo "    [repo] deploy-tools"
(cd deploy-tools && hg push $bb_root/deploy-tools )
echo "    [repo] xengine"
(cd site/xengine && hg push $bb_root/xengine )

echo "Pushing to fizlesh.ru..."
echo "    [repo] lesh..."
git push $vm_root/lesh
echo "    [tags] lesh..."
git push --tags $vm_root/lesh

echo "    [repo] deploy-tools"
( cd site/xengine && hg push $vm_root/xengine )
echo "    [repo] xengine"
( cd deploy-tools && hg push $vm_root/deploy-tools )

echo "Everything completed"
