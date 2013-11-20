#!/bin/sh

# Special linux magic!

mkdir -p lq
for i in *.jpg; do
    echo $i
    convert -quality 86 -contrast -level 20 $i lq/$i-lq.jpg
done
