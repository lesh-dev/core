#!/usr/bin/env bash
my_dir=$(dirname "$(readlink -f $0)")
git_version=$(git rev-list --all | wc -l)
version=$(cat "$my_dir/../../site/VERSION")
echo $version-rev.$git_version
