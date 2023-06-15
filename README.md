# SocNet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/socnet/actions/workflows/ci.yml)

Social network built with Django Framework.

## Features

- Multi-language (currently English and Russian). Selected based on browser settings.
- Light and dark theme support with a switch. The browser theme is selected by default.
- Progressive Web App (PWA) support.

### Regular users

- Register and confirm their account by email
- Sign in
- Add backup email addresses in case they lose access to the primary address
- Reset and change their password
- Use two-factor authentication with time-based one-time passwords (TOTP)
- Provide information about themselves in their profile
- Write real-time messages with Markdown and HTML support to other users using WebSockets
- Create, edit, like and delete posts and comments with Markdown and HTML support
- View images in posts, comments and messages as a gallery using [viewerjs](https://fengyuanchen.github.io/viewerjs/)
- Subscribe to other users to see their posts in their news feed
- Inexact search for posts by text
- Inexact search for messages by text
- Inexact search for users by selectable fields
- Delete their account
- And a lot of other little things

### Administrators

- All of the above
- Use Django admin panel
- Use a REST API that has a Swagger UI and supports all CRUD operations and filtering
- Receive error notifications in [Sentry](https://sentry.io/) or by email

## DB schema

Generated with [django-extensions](https://github.com/django-extensions/django-extensions).

![](https://github.com/monosans/socnet/assets/76561516/08b8f834-40f7-4b45-9fca-089209207256)

## Tech Stack

### Containerization

- Docker
- Docker Compose

### Backend

- Python 3.8+
- Django 4.2
- django-allauth-2fa
- django-allauth
- django-bootstrap5
- django-cleanup
- django-environ
- django-filter
- django-logentry-admin
- django-otp
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
- TypeScript
- viewerjs
- luxon

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
# Pull service images
docker compose pull --ignore-buildable
# Build services
docker compose build --pull
# Run DB migrations
docker compose run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose run --rm django python3 manage.py createsuperuser
# Compile translations
docker compose run --rm django python3 manage.py compilemessages -i site-packages

# Run without debugpy
docker compose up
# Or run with debugpy
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.debugpy.yml up
```

### Production

To run this in production, you need to specify the production settings in `.env`.

```bash
# Pull service images
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull --ignore-buildable
# Build services
docker compose -f docker-compose.yml -f docker-compose.prod.yml build --pull
# Run DB migrations
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm django python3 manage.py createsuperuser
# Run
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
