# Yatube API

API для социальной сети блогов.

## Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать: `venv\Scripts\activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Применить миграции: `python manage.py migrate`
6. Запустить: `python manage.py runserver`

## Примеры

Получить токен: `POST /api/v1/jwt/create/`

Создать пост: `POST /api/v1/posts/`

Подписаться: `POST /api/v1/follow/`
