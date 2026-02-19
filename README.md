# Socnet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/socnet/actions/workflows/ci.yml)

Social network built with Django Framework.

## Features

- Multi-language (currently English and Russian). Selected based on browser settings.
- Light and dark theme support with a switch. The browser theme is selected by default.
- Infinite scrolling.
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
- Receive error notifications in [Sentry](https://sentry.io/) or by email

## Installation

[Install `Docker Compose`](https://docs.docker.com/compose/install/).

### Configuration

Copy the `.env.example` file to `.env`. Set the settings you need in the `.env` file.

### Development

```bash
# Build services

# Linux
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)

# Windows
docker compose build

# Run DB migrations
docker compose run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose run --rm django python3 manage.py createsuperuser
# Compile translations
docker compose run --rm django python3 manage.py compilemessages --locale en --locale ru

# Run without debugpy
docker compose up --remove-orphans
# Or run with debugpy
docker compose -f compose.yaml -f compose.override.yaml -f compose.debug.yaml up --remove-orphans
```

### Production

To run this in production, you need to specify the production settings in `.env`.

```bash
# Build services
docker compose -f compose.yaml -f compose.prod.yaml build
# Run DB migrations
docker compose -f compose.yaml -f compose.prod.yaml run --rm django python3 manage.py migrate
# Create a superuser if you want
docker compose -f compose.yaml -f compose.prod.yaml run --rm django python3 manage.py createsuperuser
# Run
docker compose -f compose.yaml -f compose.prod.yaml up -d --remove-orphans
```

## Tech Stack

### Containerization

- Docker
- Docker Compose

### Backend

- Python 3.14
- Django 5.2
- django-allauth
- django-bootstrap5
- django-cleanup
- django-environ
- django-filter
- django-logentry-admin
- django-ninja
- channels
- channels-redis
- sentry-sdk

Markdown parsing and HTML sanitization, and a few other things are implemented in Rust in the `socnet_rs` package using the following libraries:

- ammonia
- pulldown-cmark
- pyo3

### Databases

- PostgreSQL 18 for persistent data
- Valkey 9 (FOSS Redis fork) for cache and as a layer for Channels

### Frontend

- HTML with Django Template language
- HTMX 2
- Bootstrap CSS 5.x
- Font Awesome 6
- TypeScript (compiled and minified with esbuild)
- viewerjs
- luxon

### Web servers

- Caddy
- granian

### Testing

- pytest
- factory-boy

### Linting

- mypy
- ruff
- eslint
- stylelint

## DB schema

![](https://github.com/monosans/socnet/assets/76561516/f8d077b5-bb2c-4834-941e-3375ef56ba48)

## License

[MIT](LICENSE)
