#!/bin/bash
rm -rf /tmp/backup-status
echo -en " **** lesh-dev.dtdns.net : backup report\\n\\n" > /tmp/backup-letter.txt
/srv/tools/backup.sh 1> /tmp/backup-letter.log 2> /tmp/backup-letter.err
cat /tmp/backup-letter.log >> /tmp/backup-letter.txt
echo -en "\\n=====================================\\nErrors was:\\n" >> /tmp/backup-letter.txt
cat /tmp/backup-letter.err >> /tmp/backup-letter.txt

STATUS=$(cat /tmp/backup-status)
if [ $STATUS. == "OK." ]; then
  #mail -s "[lesh-dev] backup OK" vdm-photo@ya.ru,dichlofos-mv@yandex.ru,trousev@yandex.ru,trousev.archive@gmail.com < /tmp/backup-letter.txt
  echo "No need to send mail"
else
  mail -s "[lesh-dev] BACKUP FAILURE" vdm-photo@ya.ru,dichlofos-mv@yandex.ru,trousev@yandex.ru,trousev.archive@gmail.com < /tmp/backup-letter.txt
fi