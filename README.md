# <img src="socnet/static/public/img/logo.svg" alt="" width="40" align="top"> Socnet

A social network built with Django: posts, comments, real-time messages, subscriptions and search, in English and Russian.

## Features

- Sign up with email confirmation, backup email addresses, password reset and two-factor authentication (TOTP).
- Profiles, subscriptions, a news feed of the people you follow, and account deletion.
- Posts and comments with Markdown and HTML, likes and editing.
- Real-time messages over WebSockets, also with Markdown and HTML.
- Images in posts, comments and messages open in a gallery ([viewerjs](https://fengyuanchen.github.io/viewerjs/)).
- Inexact search for posts and messages by text, and for users by the fields you pick.
- English and Russian, picked from the browser settings.
- Light and dark themes that follow the browser until you switch.
- Infinite scrolling, and the site installs as a Progressive Web App.
- Administrators get the Django admin panel and error reports in [Sentry](https://sentry.io/) or by email.

## Run locally

You need [Docker Compose](https://docs.docker.com/compose/install/).

```bash
cp .env.example .env
docker compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g)  # on Windows: docker compose build
docker compose run --rm django python3 manage.py migrate
docker compose run --rm django python3 manage.py compilemessages --locale en --locale ru
docker compose up --remove-orphans
```

Open <http://localhost:8000>. Emails, such as the sign-up confirmation, go to the log of the `django` container. [PgHero](https://github.com/ankane/pghero) runs at <http://localhost:8080>.

Other commands:

```bash
# Create an administrator for the admin panel at /admin/ (ADMIN_URL in .env)
docker compose run --rm django python3 manage.py createsuperuser
# Run the tests
docker compose run --rm django pytest
# Start with debugpy listening on port 5678
docker compose -f compose.yaml -f compose.override.yaml -f compose.debug.yaml up --remove-orphans
```

## Deploy

Fill in the production part of `.env`: `DJANGO_SECRET_KEY`, `DOMAIN_NAME`, `TLS_EMAIL` and the email settings. Caddy gets the TLS certificate for `DOMAIN_NAME` on its own.

```bash
docker compose -f compose.yaml -f compose.prod.yaml build
docker compose -f compose.yaml -f compose.prod.yaml run --rm django python3 manage.py migrate
docker compose -f compose.yaml -f compose.prod.yaml up -d --remove-orphans
```

Static files and translations are collected and compiled when the container starts. To create an administrator, run `createsuperuser` with the same `-f` flags.

## Tech stack

- Backend: Python 3.14, Django 6.1, Channels, django-allauth, django-ninja, granian. Markdown rendering and HTML sanitization are written in Rust in `socnet_rs`, with pulldown-cmark, ammonia and PyO3.
- Data: PostgreSQL 18, and in production Valkey 9 for the cache and Channels.
- Frontend: Django templates, HTMX 2, Bootstrap 5, Font Awesome 6, TypeScript bundled with esbuild, viewerjs, luxon.
- Infrastructure: Docker Compose, Caddy, Sentry.
- Tests and linters: pytest, factory-boy, mypy, ruff, Oxlint, Stylelint.

## Database schema

![Database schema](https://github.com/monosans/socnet/assets/76561516/f8d077b5-bb2c-4834-941e-3375ef56ba48)

## License

[MIT](LICENSE)
