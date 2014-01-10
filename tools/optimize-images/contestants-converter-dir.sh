#!/usr/bin/env bash

set -xe

convert_files_in_dir()
{
    pwd
    rar_name="$1"
    unrar x "$rar_name"

    mkdir -p lq

    if ls *.jpg; then
        for i in *.jpg ; do
            echo $i
            convert -quality 86 -contrast -level 20 "$i" "lq/$i"
        done
        rm *.jpg
        mv lq/*.jpg .
    fi

    if ls *.JPG; then
        for i in *.JPG ; do
            echo $i
            convert -quality 86 -contrast -level 20 "$i" "lq/$i"
        done
        rm *.JPG
        mv lq/*.JPG .
    fi
    rm -rf lq
    rm -f "$rar_name"
    rar a "$rar_name" *.jpg *.JPG
    rm -f *.jpg *.JPG
}

for f in *.rar ; do
    convert_files_in_dir "$f"
done
