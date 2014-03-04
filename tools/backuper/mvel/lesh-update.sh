#!/usr/bin/env bash
set -xe
cd /var/www/html/lesh
if [ -d lesh.git ] ; then
    mv lesh.git .git
fi
if ! [ -d .git ] ; then
    echo "Something is a miss here"
    exit 1
fi
log=../lesh-update.log
echo '* * * Update state for lesh repo' > $log
date >> $log
echo 'Last 5 commits were:' >> $log
( git pull && git checkout -- * && git log -n 5 ) >> $log || true
mv .git lesh.git || true
