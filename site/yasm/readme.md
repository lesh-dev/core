#Запуск YaSM:

Необходимо
* npm >=6.1.0
* python3, pip3

Сборка
* Конфиг с 'SQLALCHEMY_DATABASE_URI' положить в instance
* ```sudo aptitude install python3-pip```
* ```python3 -m virtualenv -p `which python3` venv```
* ```. venv/bin/activate```
* ```pip install -r requirements.txt``` 
* ```python run.py docs```
* ```python run.py generate```
* ```cd instance/ui```
* ```npm install```
* ```npm run build```

Сборка документации
* из корня проекта выполнить
* ```cd docs```
* ```make coverage```
* ```make html```

Запуск
* ```python run.py runserver```

#Авторизация с использованием oauth2

Для корректной работы авторизации по ```oauth2``` необходимо создать приложения в каждой из поддерживаемых платформ:
* Яндекс паспорт    https://oauth.yandex.ru
* Facebook          https://developers.facebook.com/apps
* Вконтакте         https://vk.com/apps?act=manage
* Google+           https://console.developers.google.com

Настройка для запуска локально:
* В качестве ссылки на сайт приложения указывать ```localhost```
* В качестве callback uri ```localhost/login/callback/<provider_name>```,
<br>для Яндекса: ```localhost:5000/login/callback/yandex```
* Добавить данные про приложения в ```instance/config.py```
<br> Переменная ```OAUTH_CREDENTIALS``` - словарь с ключами - названиями провайдеров авторизации, значениями - конфигурацией провайдера
<br>
```
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '<App ID>',
        'secret': '<App Secret>'
    },
    'vk': {
        'id': '<ID приложения>',
        'secret': '<Защищённый ключ>'
    },
    'yandex': {
        'id': '<ID>',
        'secret': '<Пароль>'
    },
    'google': {
        "web": {
            "client_id": "<то, что предложит скачать гугл>",
            "project_id": "<то, что предложит скачать гугл>",
            "auth_uri": "<то, что предложит скачать гугл>",
            "token_uri": "<то, что предложит скачать гугл>",
            "auth_provider_x509_cert_url": "<то, что предложит скачать гугл>",
            "client_secret": "<то, что предложит скачать гугл>",
            "redirect_uris": ["http://localhost/login/callback/google"],
            "javascript_origins": ["http://localhost"]
        }
    }
}
```

* Для работы с oauth2 от google необходимо либо выставить глобальную переменную ```OAUTHLIB_INSECURE_TRANSPORT``` либо использовать ```https```




#Локальная бд. 

* Установить postgresql https://www.postgresql.org/download/linux/ubuntu/ (10 версия)
* Положить в yasm/instance/config.py

```
SQLALCHEMY_DATABASE_URI = "postgresql://lesh:123456@127.1:5432/lesh"
SECRET_KEY = "aj;afsd lkfj jorie ajlk;ds"
```
* Добавить пользователя lesh
```
sudo -u postgres psql
    create role lesh;
    create database lesh owner lesh;
    ALTER ROLE lesh WITH LOGIN;
    alter role lesh password '123456';
```

(проверка
    psql -d lesh -U user -h 127.0.0.1
)

* В данный момент с миграцией  sqlite_to_postgresql/migrate.sh проблемы. Можно просто скопировать migration.sql (есть в чате) в /tmp

```
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f /tmp/migration.sql
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f ./pending/attributes.sql -U lesh -h 127.0.0.1
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f ./pending/rights.sql -U lesh -h 127.0.0.1
psql -d lesh --single-transaction -v ON_ERROR_STOP=on -f ./pending/search-view.sql -U lesh -h 127.0.0.1

``` 

```
psql -d lesh
    insert into person_attributes values(582, 'example', 'example');
    insert into direct_login values (963, 'i', 'pbkdf2:sha256:50000$jK658PL9$5b3a40b6db6f338f639c32f4810f3cfb0358ee55d87a89c3f973750467fb7896');
    update person set rights = 'admin' where person_id = 963;
```

* Установить postgrest

* Скачать https://github.com/PostgREST/postgrest/releases/download/v5.1.0/postgrest-v5.1.0-ubuntu.tar.xz
* Распаковать, к примеру, в /opt/

```
sudo cp ansible/postgrest.conf /etc/postgrest/lesh.conf
sudo cp ansible/postgrest.service /etc/systemd/system/postgrest.service
sudo systemctl daemon-reload
sudo systemctl start postgrest.
```

(тест с помощью curl 'localhost:3000/search?description=ilike.%конф%&limit=2')

* python run.py runserver

