#!/usr/bin/env bash
my_dir=$(dirname "$(readlink -f $0)")
git_branch=$(cd $my_dir; git symbolic-ref HEAD | sed -e s#refs/heads/##)
git_version=$(cd $my_dir; git rev-list --all | wc -l)
version=$(cat "$my_dir/../../version")
echo $git_branch-$version rev. $git_version
