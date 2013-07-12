#!/usr/bin/env bash
set -xe

# oim = google image optimizer
ln -sf ~/local/page-speed-1.9/out/Release/optimize_image_bin oim

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
mkdir -p backup
mv *.$ext backup/
ssh fizlesh.ru <<EOF
rm -rf opt-images
mkdir -p opt-images
EOF
scp output/*.$ext fizlesh.ru:opt-images/
ssh -t fizlesh.ru sudo cp opt-images/*.$ext $im_path/
