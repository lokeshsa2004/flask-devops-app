# Flask DevOps App - Complete Deployment Guide

## 📋 Repository Analysis

### Project Structure
```
flask-devops-app/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Multi-container orchestration
├── nginx.conf                      # Nginx reverse proxy config
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI/CD pipeline
├── config/
│   ├── nginx/
│   │   └── flask_app               # Nginx server block config
│   └── systemd/
│       └── flask_app.service       # Systemd service unit
├── tests/
│   └── test_app.py                 # Unit tests (500+ lines)
└── sites-enabled/                  # Nginx enabled sites directory
```

### Key Technologies
- **Framework**: Flask 2.3+
- **App Server**: Gunicorn 21+
- **Reverse Proxy**: Nginx
- **Container Runtime**: Docker
- **Container Orchestration**: Docker Compose
- **Init System**: Systemd (for bare metal deployment)
- **CI/CD**: GitHub Actions
- **Python Version**: 3.11 (or 3.8-3.11 tested)

---

## 🐳 Docker Commands

### 1. Build Docker Image Locally

```bash
# Build with default tag
docker build -t flask-devops-app:local .

# Build with custom tag
docker build -t flask-devops-app:v1.0 .

# Build with GitHub container registry tag (for GHCR)
docker build -t ghcr.io/lokeshsa2004/flask-devops-app:latest .
```

### 2. Run Single Container (Flask + Gunicorn only)

```bash
# Run and expose port 8000
docker run --rm -p 8000:8000 flask-devops-app:local

# Run in detached mode
docker run -d --name flask-app -p 8000:8000 flask-devops-app:local

# Run with restart policy
docker run -d --name flask-app --restart unless-stopped -p 8000:8000 flask-devops-app:local

# Access the app
curl http://localhost:8000
```

### 3. Docker Compose (Full Stack: Nginx + Flask)

```bash
# Start services with local image
export APP_IMAGE=flask-devops-app:local
docker compose up -d

# Or with GHCR image
export APP_IMAGE=ghcr.io/lokeshsa2004/flask-devops-app:latest
docker compose up -d

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f flask-app
docker compose logs -f nginx

# Stop all services
docker compose down

# Remove volumes and containers
docker compose down -v

# Rebuild and restart
docker compose up -d --build
```

### 4. Container Inspection & Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs flask-app
docker logs nginx
docker logs -f flask-app  # Follow logs

# Execute command in container
docker exec -it flask-app bash
docker exec -it nginx bash

# Check container resource usage
docker stats

# Stop container
docker stop flask-app

# Start container
docker start flask-app

# Remove container
docker rm flask-app

# View container details
docker inspect flask-app
```

### 5. Push Images to GitHub Container Registry (GHCR)

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u <USERNAME> --password-stdin

# Tag image
docker tag flask-devops-app:local ghcr.io/lokeshsa2004/flask-devops-app:latest
docker tag flask-devops-app:local ghcr.io/lokeshsa2004/flask-devops-app:v1.0

# Push to GHCR
docker push ghcr.io/lokeshsa2004/flask-devops-app:latest
docker push ghcr.io/lokeshsa2004/flask-devops-app:v1.0
```

---

## ⚙️ GitHub Actions - Complete Setup

### Current CI/CD Pipeline Overview

The `ci.yml` workflow includes:
1. **Test Job**: Runs pytest on Python 3.8-3.11
2. **Lint Job**: Code quality checks (Black, isort, Flake8)
3. **Deploy Job**: Deploys to EC2 (requires secrets)
4. **Notify Job**: Status notifications

### Required GitHub Secrets

Add these secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `EC2_HOST` | EC2 instance public IP or domain | `203.0.113.45` |
| `EC2_USER` | SSH user (usually `ubuntu`) | `ubuntu` |
| `EC2_KEY` | Private SSH key (EC2 .pem file content) | (paste full key) |
| `GHCR_TOKEN` | GitHub Container Registry PAT token | (see below) |

### How to Generate Required Secrets

#### 1. EC2_KEY (SSH Private Key)
```bash
# On your local machine (Windows with OpenSSH)
# If you already have the .pem file:
# Copy its contents to the clipboard, then paste in GitHub Secret

# Or generate a new key pair:
ssh-keygen -t rsa -f flask-app-key -N ""
# Upload flask-app-key.pub to EC2 authorized_keys
```

#### 2. GHCR_TOKEN (GitHub Container Registry Token)
```bash
# Go to: https://github.com/settings/tokens
# Click "Generate new token" > "Generate new token (classic)"
# Select scopes:
#   - write:packages
#   - read:packages
#   - delete:packages
# Copy the token and add as GHCR_TOKEN secret
```

### 🔧 Improvements & Changes to Add

#### 1. Add Docker Build & Push to CI/CD

Create a new workflow file: `.github/workflows/docker-build-push.yml`

```yaml
name: Build & Push Docker Image

on:
  push:
    branches:
      - master
    tags:
      - 'v*'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

#### 2. Update docker-compose.yml with environment variables

```yaml
version: '3.8'

services:
  flask-app:
    image: ${APP_IMAGE:-ghcr.io/lokeshsa2004/flask-devops-app:latest}
    container_name: flask-app
    restart: unless-stopped
    expose:
      - "8000"
    environment:
      - FLASK_ENV=${FLASK_ENV:-production}
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  nginx:
    image: nginx:latest
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - flask-app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### 3. Add .dockerignore file

```
.git
.github
.gitignore
.venv
venv
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache
.coverage
htmlcov
*.env
*.pem
.DS_Store
README.md
tests/
.dockerignore
Dockerfile
docker-compose.yml
```

#### 4. Create GitHub Actions environment file

Create `.github/workflows/.env.example`:

```bash
# Example environment variables for deployment
APP_IMAGE=ghcr.io/lokeshsa2004/flask-devops-app:latest
FLASK_ENV=production
DEBUG=False
```

#### 5. Add Security Best Practices

Update `Dockerfile` for better security:

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').status" || exit 1

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
```

---

## 🚀 Quick Start Guide

### Local Development
```bash
# 1. Clone and setup
git clone https://github.com/lokeshsa2004/flask-devops-app.git
cd flask-devops-app

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest tests/test_app.py -v

# 5. Run Flask app (development)
python app.py

# OR run with Gunicorn (production)
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

### Docker Compose (Recommended for local testing)
```bash
# Build and start
export APP_IMAGE=flask-devops-app:local
docker compose up -d --build

# Access app
curl http://localhost/

# Monitor
docker compose logs -f

# Cleanup
docker compose down
```

### EC2 Deployment (Manual - without GitHub Actions)
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@<EC2_HOST>

# Clone repository
git clone https://github.com/lokeshsa2004/flask-devops-app.git
cd flask-devops-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy systemd service
sudo cp config/systemd/flask_app.service /etc/systemd/system/

# Copy nginx config
sudo cp config/nginx/flask_app /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/

# Start services
sudo systemctl daemon-reload
sudo systemctl start flask_app
sudo systemctl enable flask_app
sudo systemctl restart nginx

# Verify
sudo systemctl status flask_app
curl http://127.0.0.1:8000/
curl http://localhost/
```

---

## 📊 Testing

```bash
# Run all tests
pytest tests/test_app.py -v

# Run specific test class
pytest tests/test_app.py::TestAppRoutes -v

# Run with coverage
pytest tests/test_app.py --cov=. --cov-report=html

# Run with markers (if defined)
pytest tests/test_app.py -v -m "not slow"
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| `docker compose up` fails | Ensure Docker daemon is running, check `docker ps` |
| Port 80 already in use | Change port in docker-compose: `"8080:80"` |
| Flask app not responding | Check `docker logs flask-app` for errors |
| Nginx connection refused | Ensure flask-app is running: `docker ps` |
| GitHub Actions deploy fails | Verify secrets are set and EC2 instance is running |
| SSH key permission denied | Check key permissions: `chmod 400 key.pem` |

---

## 📝 CI/CD Pipeline Secrets Checklist

- [ ] `EC2_HOST` - Public IP of EC2 instance
- [ ] `EC2_USER` - SSH username (ubuntu)
- [ ] `EC2_KEY` - Private SSH key content
- [ ] `GHCR_TOKEN` - GitHub Container Registry token (optional, for image pushing)

---

## 🎯 Next Steps

1. **Add Docker Build Workflow** - Automate image building and pushing to GHCR
2. **Add SSL/TLS** - Configure HTTPS with Let's Encrypt
3. **Add Environment Variables** - Use `.env` for configuration
4. **Add Monitoring** - Integrate Prometheus/Grafana or DataDog
5. **Add Logging** - Centralize logs with ELK stack or Loki
6. **Add Health Checks** - Already partially added, expand monitoring
7. **Database Integration** - Add database service to docker-compose if needed

