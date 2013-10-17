#!/usr/bin/env bash
set -e

repo="$1"
if [ -z "$repo" ] ; then
    echo "Usage: $0 <repo-name>"
    exit 1
fi

sudo git init --bare "$repo"
sudo chgrp -R lesh "$repo"
find -type d "$repo" | xargs sudo chmod g+ws
echo "Repo '$repo' initialized successfully"
