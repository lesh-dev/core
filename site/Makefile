all:
	echo "Nothing to do."

install:
	sudo cp -a * /var/www/html/site/
	sudo rm -rf /var/www/html/site/.prec/*
	sudo mkdir -p /var/www/html/site/.prec/
	sudo chmod 777 /var/www/html/site/.prec
	sudo touch /var/www/html/site/.htaccess
	sudo touch /var/www/html/site/install.php
	sudo touch /var/www/html/site/settings.php
	sudo chown -R apache:apache /var/www/html/site/fizlesh.ru-content
	sudo chown -R apache:apache /var/www/html/site/.htaccess
	sudo chown -R apache:apache /var/www/html/site/install.php
	sudo chown -R apache:apache /var/www/html/site/settings.php
