# Yatube
### Социальная сеть для блоггеров на базе Django Framework
Социальная сеть, которая позволяет пользователям просматривать и создавать записи, вступать в группы, оставлять комментарии и подписываться на интересующих авторов. Также, реализована возможность регистрации и авторизации. Проект имеет верстку с адаптацией под размер экрана устройства пользователя.

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:NikitaChalykh/YaTube.git

cd YaTube
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env

source env/bin/activate
```
3. Установить зависимости из файла ```requirements.txt```:
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
cd hw05_final

python3 manage.py migrate
```
5. Запустить проект (в режиме сервера Django):
```bash
python3 manage.py runserver
```
Стек технологий
----------
* Python 3.8
* Django 2.2 
* Unittest
* Pytest
* SQLite3
* CSS
* JS
* HTML


![](https://img.shields.io/pypi/pyversions/p5?logo=python&logoColor=yellow&style=for-the-badge)
![](https://img.shields.io/badge/Django-2.2.16-blue)
