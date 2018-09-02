Запуск YaSM:
Необходимо
* npm >=6.1.0
* python3, pip3

Сборка
* Конфиг с 'SQLALCHEMY_DATABASE_URI' положить в instance
* ```sudo aptitude install python3-pip```
* ```python3 -m virtualenv -p which python3 venv```
* ```. venv/bin/activate```
* ```pip install -r requirements.txt``` 
* ```cd instance/ui```
* ```npm install```
* ```npm run build```

Запуск
* ```python run.py runserver```