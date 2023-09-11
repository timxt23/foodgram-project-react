# Foodgram - продуктовый помощник

![example workflow](https://github.com/timxt23/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


### Описание проекта

Foodgram - это платформа для публикации рецептов. В проекте реализованы следующие функции:
- подписка авторизованных пользователей на избранных авторов;
- добавление рецептов в избранное;
- добавление ингредиентов, необходимых для приготовления, в список покупок;
- скачинвание списка покупок.

## Как запустить проект:
- Клонировать репозиторий `git@github.com:tantsiura/foodgram-project-react.git`
- Скопировать файлы `docker-compose.yaml` и `nginx/default.conf` из проекта директроии _**infra**_ на сервер по следующему пути `home/<your_username>/docker-compose.yaml` и `home/<your_username>/nginx/default.conf`.
- Установка docker:
    ```bash
    sudo apt install docker.io 
    ```
- Установка docker-compose, документация в помощь [official documentation](https://docs.docker.com/compose/install/).
- Создайте секреты в GitHub Actions согласно шаблону ниже:
    ```
    Name:                Content:
    DB_ENGINE            django.db.backends.postgresql # indicate that we are working with postgresql
    DB_NAME              postgres # database name
    POSTGRES_USER        postgres # login to connect to the database
    POSTGRES_PASSWORD    postgres # password to connect to the database (set your own)
    DB_HOST              db # name of the service (container)
    DB_PORT              5432 # port for connecting to the database
    HOST                 158.160.11.231 # server ip
    USER                 tantsiura # UserName to connect to the server
    SSH_KEY              # Private access key to connect to the server `cat ~/.ssh/id_rsa`
    PASSPHRASE           # Secret key\passphrase if your ssh key is protected with a passphrase
    TELEGRAM_TO          # id of the user's chat or the chat where the bot will send the success result
    TELEGRAM_TOKEN       # Bot token TG for sending notification
    DOCKER_USERNAME      # Docker username for publishing images
    DOCKER_PASSWORD      # Docker user password
    ```
- Сделайте коммит на Master/Main ветку и готовый к запуску проект задеплоится на ваш сервер.

- Перед запуском проекта выполните миграции:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

- И создайте супер-юзера:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

- Наполните базу данных:
    ```bash
    docker-compose exec web python manage.py loaddata /data/data.json
    ```

# Автор

Author: [timxt](https://github.com/timxt)
