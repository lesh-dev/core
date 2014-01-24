#!/usr/bin/env bash
my_dir=$(dirname "$(readlink -f $0)")
git_branch=$(git symbolic-ref HEAD | sed -e s#refs/heads/##)
git_version=$(git rev-list --all | wc -l)
version=$(cat "$my_dir/../../site/VERSION")
echo $git_branch-$version rev. $git_version
