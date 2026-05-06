# Docker Commands Reference

## 🚀 Quick Reference Commands

### Build Commands

```bash
# Build local image
docker build -t flask-devops-app:local .

# Build with specific tag
docker build -t flask-devops-app:v1.0 .

# Build for GHCR
docker build -t ghcr.io/lokeshsa2004/flask-devops-app:latest .

# Build without cache
docker build --no-cache -t flask-devops-app:local .

# Build with build args
docker build --build-arg PYTHON_VERSION=3.11 -t flask-devops-app:local .
```

---

## 🏃 Run Commands (Single Container)

### Basic Run

```bash
# Run and expose port
docker run -p 8000:8000 flask-devops-app:local

# Run in background
docker run -d -p 8000:8000 --name flask-app flask-devops-app:local

# Run with restart policy
docker run -d --restart unless-stopped -p 8000:8000 --name flask-app flask-devops-app:local

# Run with auto-cleanup
docker run --rm -p 8000:8000 flask-devops-app:local
```

### Run with Options

```bash
# Run with environment variables
docker run -d -e FLASK_ENV=production -p 8000:8000 flask-devops-app:local

# Run with volume mount
docker run -d -v $(pwd):/app -p 8000:8000 flask-devops-app:local

# Run with resource limits
docker run -d -m 512m --cpus="0.5" -p 8000:8000 flask-devops-app:local

# Run with health check
docker run -d --health-cmd="curl -f http://localhost:8000/ || exit 1" -p 8000:8000 flask-devops-app:local

# Run with log driver
docker run -d --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 -p 8000:8000 flask-devops-app:local
```

---

## 🐳 Docker Compose Commands

```bash
# Start services (build if needed)
docker compose up

# Start in background
docker compose up -d

# Start with rebuild
docker compose up -d --build

# Start with specific image
export APP_IMAGE=flask-devops-app:local
docker compose up -d

# View logs (all services)
docker compose logs

# View logs (follow)
docker compose logs -f

# View logs (specific service)
docker compose logs -f flask-app
docker compose logs -f nginx

# View logs (last 100 lines)
docker compose logs --tail=100

# Stop services
docker compose stop

# Stop specific service
docker compose stop flask-app

# Stop and remove containers
docker compose down

# Stop and remove everything (volumes too)
docker compose down -v

# Restart services
docker compose restart

# Restart specific service
docker compose restart flask-app

# Scale service (if no port mapping)
docker compose up -d --scale flask-app=3

# Pause services
docker compose pause

# Unpause services
docker compose unpause

# View service status
docker compose ps

# View full details
docker compose ps -a

# Execute command in service
docker compose exec flask-app bash
docker compose exec nginx bash

# View service logs with errors
docker compose logs 2>&1 | grep ERROR

# Validate docker-compose.yml
docker compose config

# Show running processes
docker compose top flask-app
```

---

## 📊 Container Management

### List Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# List with custom format
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

# List only IDs
docker ps -q

# List with specific filters
docker ps -f status=running
docker ps -f name=flask
```

### Inspect Containers

```bash
# Get full container details
docker inspect flask-app

# Get specific field
docker inspect flask-app | grep -i ipaddress

# Get IP address only
docker inspect -f '{{.NetworkSettings.IPAddress}}' flask-app

# Get port mappings
docker inspect -f '{{.NetworkSettings.Ports}}' flask-app

# Get environment variables
docker inspect -f '{{.Config.Env}}' flask-app
```

### View Logs

```bash
# View container logs
docker logs flask-app

# Follow logs (streaming)
docker logs -f flask-app

# Last 50 lines
docker logs --tail=50 flask-app

# Last 30 minutes
docker logs --since 30m flask-app

# Logs with timestamps
docker logs -t flask-app

# View logs with errors highlighted
docker logs flask-app 2>&1 | grep ERROR
```

### Control Containers

```bash
# Stop container
docker stop flask-app

# Force stop
docker kill flask-app

# Start container
docker start flask-app

# Restart container
docker restart flask-app

# Pause container
docker pause flask-app

# Unpause container
docker unpause flask-app

# Rename container
docker rename old-name new-name

# Remove container
docker rm flask-app

# Remove stopped containers
docker container prune

# Remove all unused containers
docker container prune -f
```

### Execute Commands

```bash
# Run command in running container
docker exec flask-app ls -la

# Interactive bash shell
docker exec -it flask-app bash

# Interactive sh shell (lighter image)
docker exec -it flask-app sh

# Run as specific user
docker exec -u appuser flask-app whoami

# Get Python version
docker exec flask-app python --version

# Run Flask command
docker exec flask-app flask --version

# Run tests
docker exec flask-app pytest tests/test_app.py
```

---

## 📦 Image Management

### List Images

```bash
# List local images
docker images

# List with specific repository
docker images flask-devops-app

# List dangling images
docker images -f dangling=true

# List images with format
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Inspect Images

```bash
# Get image details
docker inspect flask-devops-app:local

# Get image size
docker inspect -f '{{.Size}}' flask-devops-app:local

# Get image history
docker history flask-devops-app:local

# Get entrypoint
docker inspect -f '{{.Config.Entrypoint}}' flask-devops-app:local
```

### Tag & Push

```bash
# Tag image
docker tag flask-devops-app:local ghcr.io/lokeshsa2004/flask-devops-app:latest

# Tag for multiple repos
docker tag flask-devops-app:local myrepo/flask-app:v1.0

# Login to registry
docker login ghcr.io
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push image
docker push ghcr.io/lokeshsa2004/flask-devops-app:latest

# Push multiple tags
docker push ghcr.io/lokeshsa2004/flask-devops-app:v1.0
docker push ghcr.io/lokeshsa2004/flask-devops-app:latest

# Logout
docker logout ghcr.io
```

### Remove & Cleanup

```bash
# Remove image
docker rmi flask-devops-app:local

# Remove image (force)
docker rmi -f flask-devops-app:local

# Remove dangling images
docker image prune

# Remove unused images
docker image prune -a

# Remove everything unused
docker system prune -a

# Cleanup with disk space reclaim
docker system prune -a --volumes
```

---

## 🔍 Monitoring & Health

### Resource Usage

```bash
# View real-time resource stats
docker stats

# View stats for specific container
docker stats flask-app

# View stats without streaming
docker stats --no-stream

# View memory usage
docker stats --format "table {{.Container}}\t{{.MemUsage}}"
```

### Health Checks

```bash
# View container health status
docker inspect -f '{{.State.Health}}' flask-app

# Get detailed health info
docker inspect -f '{{.State.Health.Status}}' flask-app

# Manual health test
curl http://localhost:8000/

# Test through Nginx
curl http://localhost/
```

### Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect app-network

# Inspect container network
docker inspect -f '{{.NetworkSettings}}' flask-app

# Connect container to network
docker network connect app-network flask-app

# Disconnect container from network
docker network disconnect app-network flask-app

# Test network connectivity
docker exec flask-app ping nginx
```

---

## 💾 Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create app-data

# Inspect volume
docker volume inspect app-data

# Remove volume
docker volume rm app-data

# Remove unused volumes
docker volume prune

# Mount volume in container
docker run -v app-data:/data -p 8000:8000 flask-devops-app:local

# Mount local directory
docker run -v $(pwd):/app -p 8000:8000 flask-devops-app:local
```

---

## 🐛 Debugging

```bash
# Check Docker daemon status
docker version

# Check system info
docker info

# View Docker events (real-time)
docker events

# Specific container events
docker events --filter="container=flask-app"

# Build with verbose output
docker build --progress=plain -t flask-devops-app:local .

# Run container with debug shell
docker run -it flask-devops-app:local /bin/bash

# Copy files from container
docker cp flask-app:/app/app.py ./app.py

# Copy files to container
docker cp app.py flask-app:/app/app.py

# Check logs for errors
docker logs flask-app 2>&1 | grep -E "ERROR|Exception|Traceback"
```

---

## 🔐 Security

```bash
# Run container as non-root
docker run -u 1000 flask-devops-app:local

# Run container read-only
docker run --read-only flask-devops-app:local

# Drop capabilities
docker run --cap-drop=ALL flask-devops-app:local

# Scan image for vulnerabilities
docker scout cves flask-devops-app:local

# View running processes (security check)
docker top flask-app

# Check environment variables (sensitive data check)
docker inspect -f '{{.Config.Env}}' flask-app
```

---

## 📝 Useful One-Liners

```bash
# Remove all stopped containers
docker container prune -f

# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Get IP of running container
docker inspect -f '{{.NetworkSettings.IPAddress}}' flask-app

# Kill all containers
docker kill $(docker ps -q)

# View all running services with ports
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Save image to tar
docker save flask-devops-app:local | gzip > flask-app.tar.gz

# Load image from tar
docker load < flask-app.tar.gz

# Get image size
du -h $(docker inspect -f '{{.GraphDriver.Data.MergedDir}}' flask-app)
```

---

## 📚 Docker Compose Examples

### Development (with hot reload)

```yaml
services:
  flask-app:
    build: .
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
    ports:
      - "8000:8000"
```

Run: `docker compose up`

### Production (with logging)

```yaml
services:
  flask-app:
    image: ghcr.io/lokeshsa2004/flask-devops-app:latest
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

Run: `docker compose up -d`

### Multi-stage build

```dockerfile
# Build stage
FROM python:3.11 as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY app.py .
EXPOSE 8000
CMD ["gunicorn", "app:app"]
```

---

## ✅ Checklist for Production

- [ ] Image scanned for vulnerabilities
- [ ] Non-root user configured
- [ ] Resource limits set
- [ ] Health checks configured
- [ ] Logging driver configured
- [ ] Restart policy set to `unless-stopped`
- [ ] Secrets not hardcoded
- [ ] Environment variables externalized
- [ ] Volume mounts used for persistence
- [ ] Network isolation configured
- [ ] Image optimized (slim base, multi-stage)
- [ ] Tests run in CI/CD
- [ ] Image tagged with version
- [ ] Image pushed to registry

