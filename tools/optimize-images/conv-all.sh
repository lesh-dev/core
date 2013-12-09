#!/usr/bin/env bash

set -xe

convert_files_in_dir()
{
    if ! ls *.rar ; then
        return
    fi
    pwd
    rar_name="$(ls *.rar)"
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
    zip "$rar_name.zip" *.jpg *.JPG
}

for d in 1* ; do
    (cd "$d" && convert_files_in_dir )
done
