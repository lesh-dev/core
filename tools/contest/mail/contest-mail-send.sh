#!/usr/bin/env bash

mail_list="list"

if ! (locale | grep -qi utf) ; then
    echo "Please check your locale settings"
    locale
    exit 1
fi

echo "Sending contest from $mail_list"
for addr in $(cat $mail_list); do
    mutt \
        -F muttrc \
        -a pravila-olimpiada-fizlesh-contest-2015-2016.pdf \
        -a usloviya-olimpiada-fizlesh-contest-2015-2016.pdf \
        -s 'О Межрегиональной Физической Олимпиаде 2015-2016' \
        -- $addr < letter2015.txt
    sleep 1
    echo "Sent to $addr"
done
