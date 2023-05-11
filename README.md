# SocNet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/socnet/actions/workflows/ci.yml)

Social network built with Django Framework.

## Features

English and Russian languages ​​are supported. The language is selected based on the browser settings.

### Regular users

- Register and confirm their account by email
- Sign in
- Reset and change their password
- Use two-factor authentication with one-time passwords
- Provide information about themselves in their profile
- Write real-time messages with Markdown and HTML support to other users using WebSockets
- Create, edit, like and delete posts and comments with Markdown and HTML support
- Subscribe to other users to see their posts in their news feed
- Search for posts by text or for other users
- Delete their account

### Administrators

- All of the above
- Use Django admin panel
- Use a REST API that has a Swagger UI and supports all CRUD operations and filtering
- Receive error notifications in [Sentry](https://sentry.io/) or by email

## DB schema

Generated with [django-extensions](https://github.com/django-extensions/django-extensions).

![](https://user-images.githubusercontent.com/76561516/224795816-22bf775e-ced0-44ca-a8ef-b3501179a182.png)

## Tech Stack

- Docker
- Docker Compose
- Caddy

### Backend

- Python 3.8+
- Django 4.2
- Django REST framework (DRF)
- DRF Spectacular
- Django Channels
- Django Filter
- Django Allauth
- Django Allauth 2FA
- Django OTP
- Django Crispy Forms
- Django Environ
- Sentry
- WebSockets
- lxml
- pytest + factory-boy
- mypy
- Gunicorn + Uvicorn
- PostgreSQL 15
- Redis 7
- etc.

### Frontend

- HTML + Django template language
- Bootstrap CSS 5
- JavaScript
- Font Awesome 6

## Installation

[Install `Docker Compose`](https://docs.docker.com/compose/install/).

### Configuration

Copy the `.env.example` file to `.env`. Set the settings you need in the `.env` file.

### Development

```bash
# Build services
docker compose build --pull
# Pull service images
docker compose pull --ignore-pull-failures
# Run DB migrations
docker compose run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose run --rm django python3 manage.py createsuperuser
# Compile translations
docker compose run --rm django python3 manage.py compilemessages

# Run without debugpy
docker compose up
# Or run with debugpy
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.debugpy.yml up
```

### Production

To run this in production, you need to specify the production settings in `.env`.

```bash
# Build services
docker compose -f docker-compose.yml -f docker-compose.prod.yml build --pull
# Pull service images
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull --ignore-pull-failures
# Run DB migrations
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py createsuperuser
# Compile translations
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py compilemessages
# Run
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
