#!/usr/bin/env bash
my_dir=$(dirname "$(readlink -f $0)")
git_branch="$( cd $my_dir; git symbolic-ref HEAD | sed -e s:refs/heads/:: )"
git_version="$(cd $my_dir; git rev-list --all | wc -l)"

# to flush CSS cache each time it deploys
local_status="$( git status | sha256sum - | cut -c1-4 )"
local_diff="$( git diff | sha256sum - | cut -c5-8 )"

version=$(cat "$my_dir/../../version")
echo $git_branch-$version-r$git_version-$local_status-$local_diff
