#!/usr/bin/env bash

my_self=$(readlink -f "$0")
my_dir="$(dirname "$my_self")"

set -e

project_name="fizlesh"
destination="$1"
if [ -z "$destination" ] ; then
    destination="$project_name"
fi

main_repo_path="git@github.com:lesh-dev/core.git"
if echo $(hostname) | grep -q fizlesh ; then
    # production host
    main_repo_path="/srv/git/lesh"
    hg_common_repo_path="/srv/git"
fi

# bootstrap project into current directory
git clone $main_repo_path $destination
# tmp hack for old and new engine
hg clone $hg_common_repo_path/xengine $destination/site/xengine
hg clone $hg_common_repo_path/deploy-tools $destination/deploy-tools

echo "Bootstrapping '$project_name' with dependencies done to '$destination'"
