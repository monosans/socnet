# SocNet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/socnet/actions/workflows/ci.yml)

Social network built with Django Framework.

## Features

English and Russian languages ​​are supported. The language is selected based on the browser settings.

A light and dark theme with a switch is supported. The default is the browser theme.

### Regular users

- Register and confirm their account by email
- Sign in
- Add backup email addresses in case they lose access to the primary address
- Reset and change their password
- Use two-factor authentication with one-time passwords via mobile authenticator
- Provide information about themselves in their profile
- Write real-time messages with Markdown and HTML support to other users using WebSockets
- Create, edit, like and delete posts and comments with Markdown and HTML support
- Subscribe to other users to see their posts in their news feed
- Search for posts by text
- Search for users by selectable fields
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

### Containerization

- Docker
- Docker Compose

### Backend

- Python 3.8+
- Django 4.2
- django-allauth-2fa
- django-allauth
- django-cleanup
- django-environ
- django-filter
- django-logentry-admin
- django-otp
- django-crispy-forms
- crispy-bootstrap5
- djangorestframework
- drf-spectacular
- channels
- channels-redis
- sentry-sdk
- websockets

Markdown parsing, HTML sanitization and some other things are implemented in Rust in the `socnet_rs` package using the following libraries:

- ammonia
- pulldown-cmark
- pyo3

### Databases

- PostgreSQL 15 for persistent data
- Redis 7 for cache and as a layer for Channels

### Frontend

- HTML with Django Template language
- Bootstrap CSS 5.3
- Font Awesome 6
- JavaScript

### Web servers

- Caddy
- gunicorn
- uvicorn

### Testing

- pytest
- factory-boy

### Linting

- mypy
- ruff
- eslint
- stylelint

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
