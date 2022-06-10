# SocNet

Social network written in Django Framework as a portfolio project.

## What can users do?

- Maintain their own profile by providing information about themselves and posting.
- Subscribe to other users to later see their posts in their news feed.
- Write comments on posts.
- Like posts and comments.
- Write each other messages in real time.
- Search users and posts.

## Main technologies used

Backend:

- Python
- Django
- Django REST framework (DRF)
- Django Channels (WebSockets)
- PostgreSQL
- Redis
- Gunicorn + Uvicorn

Frontend:

- HTML + Django template language
- Bootstrap CSS
- JavaScript

Misc:

- Docker
- Poetry

## Supported languages

English and Russian languages ​​are supported. The language is selected based on the browser settings.

## Installation

[Install `docker` and `docker-compose`](https://docs.docker.com/engine/install/).

### Configuration

Copy the `config/.env.template` file to `config/.env`. Set the settings you need in the `config/.env` file.

### Development

```bash
docker compose build
docker compose run --rm web python manage.py migrate
docker compose up
```

### Production

To run this in production, you need to specify a domain name in `config/.env`. An SSL certificate will be obtained automatically.

```bash
docker compose -f docker-compose.yml -f docker/docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker/docker-compose.prod.yml up -d
```
