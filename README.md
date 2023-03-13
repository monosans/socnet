# SocNet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/monosans/socnet/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/monosans/socnet/main.svg)](https://results.pre-commit.ci/latest/github/monosans/socnet/main)
[![codecov](https://codecov.io/gh/monosans/socnet/branch/main/graph/badge.svg)](https://codecov.io/gh/monosans/socnet)

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

## Tech Stack

- Docker
- Docker Compose
- Caddy

### Backend

- Python 3.8+
- Django 4.1
- Django REST framework (DRF)
- Django Channels (WebSockets)
- Django Filter
- Django Allauth
- Django Allauth 2FA
- Django OTP
- Django Crispy Forms
- Django Environ
- lxml
- pytest
- PostgreSQL 15
- Redis 7
- Gunicorn + Uvicorn

### Frontend

- HTML + Django template language
- Bootstrap CSS 5
- JavaScript
- Font Awesome 6

## Installation

[Install `Docker Compose`](https://docs.docker.com/compose/install/).

### Configuration

Copy the `.env.template` file to `.env`. Set the settings you need in the `.env` file.

### Development

```bash
# Build a container
docker compose build --no-cache --pull
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

To run this in production, you need to specify a domain name and email settings in `.env`.

```bash
# Build a container
docker compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache --pull
# Run DB migrations
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py createsuperuser
# Compile translations
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py compilemessages
# Run
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
