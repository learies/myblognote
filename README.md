# MyBlogNote

Платформа для блога. Можно публиковать посты, подписаться на авторов, комментировать посты.

## Технологии
- Python 3.9
- Django 3.2
- Django REST framework 3.13
- Unittest

## Установка
Клонировать репозиторий:
```
$ git clone https://github.com/learies/myblognote.git
```
Перейти в проект:
```
$ cd myblognote
```
Cоздать виртуальное окружение:
```
$ python3 -m venv venv
```
Активировать виртуальное окружение:
```
$ source venv/bin/activate
```
Установить зависимости:
```
(venv)$ pip install -r requirements.txt
```
Сделать миграции:
```
(venv)$ python manage.py migrate
```
Запустить проект:
```
(venv)$ python3 manage.py runserver
```
