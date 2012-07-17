install sync:
	(cd ../ && find . -name '*~' | xargs rm -f && sudo rsync -avz --delete forum/ /var/www/html/forum/)
backup:
	(cd ../ && tar -cvzf forum-`date +%Y.%m.%d-%H.%M`.tar.gz forum)
