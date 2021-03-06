# SocNet

Social network written in Django Framework.

## What can users do?

- Maintain their own profile by providing information about themselves and posting.
- Subscribe to other users to later see their posts in their news feed.
- Write comments on posts.
- Like posts and comments.
- Write each other messages in real time.
- Search users and posts.

## Main technologies used

- Docker
- Docker Compose

Backend:

- Python 3.8+
- Django 4.0
- Django REST framework (DRF)
- Django Channels (WebSockets)
- Django Allauth
- Django environ
- PostgreSQL
- Redis
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
docker compose run --rm django python manage.py migrate
docker compose run --rm django python manage.py compilemessages
docker compose up
```

### Production

To run this in production, you need to specify a domain name and email settings in `.env`.

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
