#!/usr/bin/env bash
# Quick Start Script for Flask DevOps App
# Usage: bash quickstart.sh [local|docker|docker-compose|ec2]

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${COLOR_BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${COLOR_GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${COLOR_RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${COLOR_YELLOW}⚠ $1${NC}"
}

# Default mode
MODE=${1:-docker-compose}

case $MODE in
    local)
        print_header "Local Development Setup"
        
        # Check Python
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3 not found. Please install Python 3.8+"
            exit 1
        fi
        print_success "Python 3 found: $(python3 --version)"
        
        # Create virtual environment
        if [ ! -d "venv" ]; then
            print_header "Creating virtual environment"
            python3 -m venv venv
            print_success "Virtual environment created"
        else
            print_warning "Virtual environment already exists"
        fi
        
        # Activate venv
        print_header "Activating virtual environment"
        source venv/bin/activate || . venv/Scripts/activate
        print_success "Virtual environment activated"
        
        # Install dependencies
        print_header "Installing dependencies"
        pip install --upgrade pip
        pip install -r requirements.txt
        print_success "Dependencies installed"
        
        # Run tests
        print_header "Running tests"
        pip install pytest pytest-cov
        pytest tests/test_app.py -v --tb=short
        print_success "Tests passed"
        
        # Run Flask app
        print_header "Starting Flask app (Gunicorn)"
        print_warning "App will run on http://127.0.0.1:8000"
        print_warning "Press Ctrl+C to stop"
        gunicorn -w 3 -b 127.0.0.1:8000 --reload app:app
        ;;
        
    docker)
        print_header "Docker Single Container Setup"
        
        # Check Docker
        if ! command -v docker &> /dev/null; then
            print_error "Docker not found. Please install Docker"
            exit 1
        fi
        print_success "Docker found: $(docker --version)"
        
        # Build image
        print_header "Building Docker image"
        docker build -t flask-devops-app:local .
        print_success "Image built: flask-devops-app:local"
        
        # Run container
        print_header "Starting Flask app container"
        print_warning "App will run on http://localhost:8000"
        print_warning "Press Ctrl+C to stop"
        docker run --rm -p 8000:8000 flask-devops-app:local
        ;;
        
    docker-compose)
        print_header "Docker Compose Full Stack Setup"
        
        # Check Docker & Docker Compose
        if ! command -v docker &> /dev/null; then
            print_error "Docker not found. Please install Docker"
            exit 1
        fi
        print_success "Docker found: $(docker --version)"
        
        if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
            print_error "Docker Compose not found. Please install Docker Compose"
            exit 1
        fi
        print_success "Docker Compose is available"
        
        # Build and start
        print_header "Building and starting services"
        export APP_IMAGE=flask-devops-app:local
        docker compose up -d --build
        print_success "Services started"
        
        # Wait for services
        print_header "Waiting for services to be ready"
        sleep 5
        
        # Health check
        if curl -f http://localhost/ > /dev/null 2>&1; then
            print_success "App is accessible at http://localhost/"
        else
            print_warning "App might still be starting, check: docker compose logs -f"
        fi
        
        print_warning "To view logs: docker compose logs -f"
        print_warning "To stop services: docker compose down"
        print_warning "To view individual service logs: docker compose logs -f flask-app"
        ;;
        
    ec2)
        print_header "EC2 Manual Deployment Setup"
        
        print_warning "This assumes you have:"
        print_warning "  - An EC2 instance running Ubuntu"
        print_warning "  - SSH access to the instance"
        print_warning "  - Git installed on EC2"
        
        read -p "Enter EC2 instance IP or domain: " EC2_HOST
        read -p "Enter SSH user (default: ubuntu): " EC2_USER
        EC2_USER=${EC2_USER:-ubuntu}
        read -p "Enter path to .pem file: " PEM_FILE
        
        if [ ! -f "$PEM_FILE" ]; then
            print_error "PEM file not found: $PEM_FILE"
            exit 1
        fi
        
        print_header "Connecting to EC2 instance"
        ssh -i "$PEM_FILE" "$EC2_USER@$EC2_HOST" << 'EOSSH'
            set -e
            
            echo "=== Clone Repository ==="
            [ -d ~/flask_app ] || git clone https://github.com/lokeshsa2004/flask-devops-app.git ~/flask_app
            cd ~/flask_app
            git pull origin master
            
            echo "=== Setup Python Environment ==="
            [ -d venv ] || python3 -m venv venv
            source venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            
            echo "=== Setup Systemd Service ==="
            sudo cp config/systemd/flask_app.service /etc/systemd/system/
            sudo systemctl daemon-reload
            
            echo "=== Setup Nginx ==="
            sudo cp config/nginx/flask_app /etc/nginx/sites-available/
            sudo ln -sf /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
            sudo nginx -t
            
            echo "=== Start Services ==="
            sudo systemctl start flask_app
            sudo systemctl start nginx
            sudo systemctl enable flask_app
            sudo systemctl enable nginx
            
            echo "=== Verification ==="
            echo "Gunicorn status:"
            sudo systemctl status flask_app
            echo ""
            echo "Nginx status:"
            sudo systemctl status nginx
            echo ""
            echo "Testing local connection:"
            curl -s http://127.0.0.1:8000/ | head -n 10
EOSSH
        
        print_success "EC2 deployment completed"
        print_header "Next steps:"
        print_warning "1. SSH into instance: ssh -i $PEM_FILE $EC2_USER@$EC2_HOST"
        print_warning "2. Check logs: sudo journalctl -u flask_app -f"
        print_warning "3. Access app at: http://$EC2_HOST"
        ;;
        
    *)
        print_header "Flask DevOps App - Quick Start"
        echo "Usage: bash quickstart.sh [mode]"
        echo ""
        echo "Available modes:"
        echo "  local              - Local development with Python venv"
        echo "  docker             - Single Docker container"
        echo "  docker-compose     - Docker Compose (Nginx + Flask)"
        echo "  ec2                - Deploy to EC2 instance"
        echo ""
        echo "Examples:"
        echo "  bash quickstart.sh local"
        echo "  bash quickstart.sh docker-compose"
        echo "  bash quickstart.sh ec2"
        exit 0
        ;;
esac
