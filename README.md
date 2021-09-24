# Продуктовый помощник Foodgram.
Проект развернут по адресу: http://62.84.123.43/

## Описание сервиса
Проект Продуктовый помощник - это сайт, который позволяет пользователям публиковать и делиться рецептами, добавлять чужие рецепты в избранное и подписываться на публикации других авторов, а также автоматически создавать список продуктов, , которые нужно купить для приготовления выбранных блюд, и скачивать его.

## Установка сервиса
+ backend - образ бэкенда
+ frontend - образ фронтенда
+ postgres - образ базы данных PostgreSQL v 12.04
+ nginx

## Команда клонирования репозитория:
- git clone https://github.com/chgala/foodgram-project-react.git

## Заполнение .env:
Чтобы добавить переменную в .env необходимо открыть файл .env в корневой директории проекта и поместить туда переменную в формате имя_переменной=значение. Пример .env файла: 
> - DB_ENGINE=db
> - DB_NAME=postgres
> - POSTGRES_USER=postgres
> - POSTGRES_PASSWORD=postgres
> - DB_HOST=db
> - DB_PORT=5432

## Запуск проекта:
+ Установите Докер
+ Перейдите в папку в проекте infra/
+ Выполните команду:
> - docker-compose up -d --build

## Первоначальная настройка Django:
> - sudo docker-compose exec backend python manage.py makemigrations
> - sudo docker-compose exec backend python manage.py migrate --noinput
> - sudo docker-compose exec backend python manage.py collectstatic --no-input 
## Создание суперюзера
> - sudo docker-compose exec backend python manage.py createsuperuser

