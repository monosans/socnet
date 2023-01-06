# SocNet

[![CI](https://github.com/monosans/socnet/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/monosans/socnet/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/monosans/socnet/main.svg)](https://results.pre-commit.ci/latest/github/monosans/socnet/main)
[![codecov](https://codecov.io/gh/monosans/socnet/branch/main/graph/badge.svg)](https://codecov.io/gh/monosans/socnet)

Social network built with Django Framework.

## What can users do?

- Maintain their own profile by providing information about themselves and posting.
- Subscribe to other users to see their posts in their news feed.
- Write comments on posts.
- Like posts and comments.
- Write messages to each other in real time.
- Search for users and posts.

## Main technologies used

- Docker
- Docker Compose

Backend:

- Python 3.8+
- Django 4.1
- Django REST framework (DRF)
- Django Channels (WebSockets)
- Django Allauth
- Django Environ
- Django Filter
- PostgreSQL 15
- Redis 7
- Gunicorn + Uvicorn

Frontend:

- HTML + Django template language
- Bootstrap CSS 5
- JavaScript
- Font Awesome 6

## Supported languages

English and Russian languages ​​are supported. The language is selected based on the browser settings.

## Installation

[Install `Docker Compose`](https://docs.docker.com/compose/install/).

### Configuration

Copy the `.env.template` file to `.env`. Set the settings you need in the `.env` file.

### Development

```bash
docker compose build
docker compose run --rm django python3 manage.py migrate
docker compose run --rm django python3 manage.py compilemessages
```

#### Run without debugpy

```bash
docker compose up
```

#### Run with debugpy

```bash
docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.debugpy.yml up
```

### Production

To run this in production, you need to specify a domain name and email settings in `.env`.

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
