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
* ```cd instance/ui```
* ```npm install```
* ```npm run build```

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
