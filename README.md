# Flask DevOps App

Minimal Flask app with production-style deployment options:
- Gunicorn
- Nginx
- Systemd (VM/bare-metal)
- Docker / Docker Compose

## What’s in this repo

- **App**: `app.py` (single route `/`)
- **Tests**: `tests/test_app.py`
- **Docker**: `Dockerfile`
- **Docker Compose**: `docker-compose.yml` + `nginx.conf`
- **VM deployment configs**: `config/systemd/flask_app.service`, `config/nginx/flask_app`

## Quickstart (recommended)

See `docs/INSTRUCTIONS.md` for the full instructions (local, Docker, Compose, EC2, CI/CD).

## Local (virtualenv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

Open `http://127.0.0.1:8000`.

## Docker: build + run locally

Build the image:

```bash
docker build -t flask-devops-app:local .
```

Run the container (app listens on port 8000 in the container):

```bash
docker run --rm -p 8000:8000 flask-devops-app:local
```

Open in browser:

`http://localhost:8000`

## Docker Compose (Nginx container + app container)

This repo also supports a 2-container layout:

Browser → **Nginx (container, port 80)** → **Flask+Gunicorn (container, port 8000)**.

Run locally:

```bash
export APP_IMAGE=flask-devops-app:local
docker compose up -d
```

Open:

`http://localhost/`
