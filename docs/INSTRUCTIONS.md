# Instructions (Consolidated)

This repo intentionally keeps documentation **small and single-source**:
- Start with `README.md`
- Use this file for all setup/deploy instructions

## Local development (virtualenv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

Open `http://127.0.0.1:8000`.

## Docker (single container)

```bash
docker build -t flask-devops-app:local .
docker run --rm -p 8000:8000 flask-devops-app:local
```

Open `http://localhost:8000`.

## Docker Compose (nginx → app)

```bash
export APP_IMAGE=flask-devops-app:local
docker compose up -d --build
curl -fsS http://localhost/ >/dev/null && echo "OK"
docker compose logs -f
```

Stop:

```bash
docker compose down
```

## VM / bare-metal (Ubuntu) with systemd + nginx

This uses:
- `config/systemd/flask_app.service`
- `config/nginx/flask_app`

High-level steps on the VM:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx

git clone <your-repo-url> flask_app
cd flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo cp config/systemd/flask_app.service /etc/systemd/system/flask_app.service
sudo systemctl daemon-reload
sudo systemctl enable --now flask_app

sudo cp config/nginx/flask_app /etc/nginx/sites-available/flask_app
sudo ln -sf /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/flask_app
sudo nginx -t
sudo systemctl restart nginx
```

## CI/CD notes (GitHub Actions)

Workflow: `.github/workflows/ci.yml`

- Runs **tests + lint** on PRs and pushes to `master`.
- Builds & pushes a Docker image to GHCR on non-PR events.
- Deploy job expects the repo to contain `docker-compose.yml` and uses it on the EC2 host.

### Secrets used by the workflow

Required:
- `EC2_HOST`
- `EC2_USER`
- `EC2_KEY`

Optional (only if your GHCR image is private):
- `GHCR_TOKEN`

