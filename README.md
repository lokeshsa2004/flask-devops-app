# Flask DevOps App

Simple Flask app deployed using:
- Gunicorn
- Nginx
- Systemd
- Docker (containerized deployment)

## Setup

1. Create virtualenv
2. Install requirements
3. Run with Gunicorn
4. Configure Nginx

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

## Push image to a registry and pull it elsewhere

Example with Docker Hub:

```bash
docker login
docker tag flask-devops-app:local <dockerhub-username>/flask-devops-app:latest
docker push <dockerhub-username>/flask-devops-app:latest
```

On another machine/VM:

```bash
docker pull <dockerhub-username>/flask-devops-app:latest
docker run --rm -p 8000:8000 <dockerhub-username>/flask-devops-app:latest
```

## Deploy container on EC2 (Ubuntu)

1) Install Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

2) Pull and run (map container 8000 to host 80):

```bash
docker pull <dockerhub-username>/flask-devops-app:latest
docker run -d --name flask-devops-app --restart unless-stopped -p 80:8000 <dockerhub-username>/flask-devops-app:latest
```

3) Ensure the EC2 Security Group allows inbound TCP **80**.

Then access:

`http://<ec2-public-ip>/`

## What to monitor (short note)

- **Availability/health**: HTTP 200 on `/` (and optionally add a dedicated `/healthz` later).
- **Latency and error rate**: 4xx/5xx counts, p95 response time.
- **Container stability**: restarts, uptime, image version running.
- **Resource usage**: container + host CPU, memory, disk.
- **Logs**: app/Gunicorn stdout/stderr and container logs (spikes in tracebacks).
- **Network**: request rate, bandwidth, failed connections/timeouts.
