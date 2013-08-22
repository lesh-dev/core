#!/bin/bash

# VPS Backup Invoker
# ------------------
# Please do not edit this file directly, get a copy from git
# tools/backup/backup-script.sh

backup_status_file=/tmp/backup-status
quota_status_file=/tmp/quota-status
letter_file=/tmp/backup-letter.txt
out_log=/tmp/backup-letter.log
# mailx on Debian cannot send letters with attachments, so we use mutt
mail_cmd=mutt

mailto="vdm-photo@ya.ru,dichlofos-mv@yandex.ru,trousev@yandex.ru,trousev.archive@gmail.com"

# clear garbage
rm -f $backup_status_file $quota_status_file
rm -f $out_log $out_log.gz

echo -en "Backup report for fizlesh.ru\\n---------------------------------------\\n" > $letter_file
/srv/tools/backup.sh 2>&1 1> $out_log
echo -en "Last 20 lines of log:\\n\\n" >> $letter_file
tail -n 20 $out_log >> $letter_file
gzip $out_log

do_send="NO"
quota_text="OK"
backup_text="OK"

if ! [ -r "$backup_status_file" ]; then
    echo "FATAL: backup status is not set. " >> $letter_file
    do_send="YES"
fi

if ! [ -r "$quota_status_file" ]; then
    echo "FATAL: quota status is not set. " >> $letter_file
    do_send="YES"
fi

backup_status=$(cat "$backup_status_file")
if [ "$backup_status." != "OK." ]; then
    do_send="YES"
    backup_text="FAILED"
fi

quota_status=$(cat "$quota_status_file")
if [ "$quota_status." != "OK." ]; then
    do_send="YES"
    quota_text="FAILED"
fi

if [ "$do_send." == "YES." ]; then
    $mail_cmd -a $out_log.gz -s "[lesh-dev] Backup: $backup_text, Quota: $quota_text" -- "$mailto" < $letter_file
else
    echo "No need to send mail"
fi

exit 0

