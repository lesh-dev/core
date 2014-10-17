#!/usr/bin/env bash

mail_list="list"

echo "Sending contest from $mail_list"
for addr in $(cat $mail_list); do
    mutt \
        -F muttrc
        -a pravila-olimpiada-fizlesh-contest-2014-2015.pdf
        -a usloviya-olimpiada-fizlesh-contest-2014-2015.pdf \
        -s 'О Межрегиональной Физической Олимпиаде 2014-2015' \
        -- $addr < letter2014.txt
    sleep 1
    echo "Sent to $addr"
done
