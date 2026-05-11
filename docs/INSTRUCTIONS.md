# Instructions (Consolidated)

This repo is **StackForge Showcase**: a Flask app backed by **MySQL**, with **static JS/CSS** and **images** under `static/img/`.

## What runs where

- **Browser** → Nginx (port 80 in Compose) → Gunicorn/Flask (port 8000 internally)
- **MySQL 8** runs as the `db` service; Flask connects using `DATABASE_URL`

## Local development (SQLite)

By default (no `DATABASE_URL`), the app uses SQLite under `./instance/stackforge.db`.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/generate_placeholders.py
flask --app app init-db
pytest -q
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

Open `http://127.0.0.1:8000`.

Useful endpoints:

- `/` HTML UI
- `/api/items` JSON for the client-side grid
- `/api/health` DB connectivity check

## Docker Compose (MySQL + Flask + Nginx)

```bash
docker compose up -d --build
curl -fsS http://localhost/api/health
docker compose logs -f
```

Stop:

```bash
docker compose down
```

Notes:

- The Flask container entrypoint waits for MySQL, runs `flask init-db`, then starts Gunicorn (`docker/entrypoint.sh`).
- Default DB credentials are **demo-only**; change them before any real deployment.

## Single-container Docker (no bundled MySQL)

This is mainly for quick image smoke tests; the app will use **SQLite** unless you pass `DATABASE_URL`:

```bash
docker build -t flask-devops-app:local .
docker run --rm -p 8000:8000 flask-devops-app:local
```

## VM / bare-metal (Ubuntu) with systemd + nginx

If you deploy without Docker, point `DATABASE_URL` at a real MySQL instance and keep Gunicorn behind Nginx.

Files:

- `config/systemd/flask_app.service`
- `config/nginx/flask_app`

## GitHub Actions / EC2 deploy

Workflow: `.github/workflows/ci.yml`

- **Tests** run against a **MySQL service container** (SQLAlchemy still works; unit tests also use an in-memory SQLite app fixture for speed).
- **EC2 deploy** runs `docker compose pull` + `docker compose up -d`, which starts **db + flask-app + nginx**.

### Secrets

Required for deploy:

- `EC2_HOST`
- `EC2_USER`
- `EC2_KEY`

Optional:

- `GHCR_TOKEN` (only if your GHCR image is private)
