#!/usr/bin/env bash
set -xe

# oim = google image optimizer

im_path="$1"
ext="$2"

scp fizlesh.ru:$im_path/*.$ext .
rm -rf output
mkdir -p output
for i in *.$ext ; do
    ./oim $i output/$i
done
du -bc *.$ext | grep total
du -bc output/*.$ext | grep total
