#!/usr/bin/env bash

. deploy-tools/installer/installer.sh

version="$(echo -n "Source version: " && cat version)"
print_message $version
print_message "Last tags:"
git tag | sort -Vr | head -n 5

gh_lesh="git@github.com:lesh-dev/core.git"
vm_root="ssh://fizlesh.ru//srv/git"
bb_root="ssh://hg@bitbucket.org/dichlofos"

print_message "Pushing to github..."
print_message "    [repo] lesh..."
git push $gh_lesh
print_message "    [tags] lesh..."
git push --tags $gh_lesh
print_message "    [repo] deploy-tools"
(cd deploy-tools && hg push $bb_root/deploy-tools )
print_message "    [repo] xengine"
(cd site/xengine && hg push $bb_root/xengine )

print_message "Pushing to fizlesh.ru..."
print_message "    [repo] lesh..."
git push $vm_root/lesh
print_message "    [tags] lesh..."
git push --tags $vm_root/lesh

print_message "    [repo] deploy-tools"
( cd site/xengine && hg push $vm_root/xengine )
print_message "    [repo] xengine"
( cd deploy-tools && hg push $vm_root/deploy-tools )

print_message "Everything completed"
