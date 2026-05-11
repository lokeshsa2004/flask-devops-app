# StackForge Showcase (Flask full-stack demo)

This repository is a **small full-stack sample** named **StackForge Showcase**:

- **Backend**: Flask + SQLAlchemy + **MySQL** (via **PyMySQL**)
- **Frontend**: Jinja templates + static **CSS** + a little **JavaScript** (theme toggle + JSON grid)
- **Assets**: PNG placeholders under `static/img/` (generated in Docker builds via `scripts/generate_placeholders.py`)
- **Ops**: Docker / Docker Compose (**MySQL + Flask + Nginx**), GitHub Actions CI/CD, optional EC2 deploy

## Quick links

- **Runbook / deploy details**: `docs/INSTRUCTIONS.md`
- **App factory + routes**: `showcase/`
- **WSGI entrypoint**: `app.py` (`gunicorn app:app`)

## Local quickstart (SQLite by default)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_placeholders.py
flask --app app init-db
pytest -q
flask --app app run --debug
```

## Docker Compose (recommended: MySQL + app + Nginx)

```bash
docker compose up -d --build
```

Open `http://localhost/` (Nginx → Flask).

## CI/CD

See `.github/workflows/ci.yml` (tests + lint + Docker publish + Compose-based EC2 deploy).
