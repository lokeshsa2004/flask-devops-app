# Flask DevOps App - Full Stack Production-Ready Application

A complete full-stack Flask application with modern architecture, database integration, responsive frontend, and production-grade deployment capabilities.

## 📋 What's in this repo

- **Backend**: Scalable Flask app with blueprint architecture, SQLAlchemy ORM, REST API
- **Database**: MySQL integration with user management system
- **Frontend**: Modern responsive UI with dynamic JavaScript, user management dashboard
- **Assets**: CSS, JavaScript, and icon assets
- **Tests**: Comprehensive test suite with pytest
- **Docker**: Dockerfile and Docker Compose for containerized deployment
- **CI/CD**: GitHub Actions workflow for automated testing, building, and EC2 deployment
- **VM Deployment**: Systemd and Nginx configs for bare-metal deployments

## 🚀 Quick Start

### Local Development (with venv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python3 -m flask run
```

Open `http://127.0.0.1:5000`

### Docker Compose (Recommended for full testing)

```bash
export APP_IMAGE=flask-devops-app:local
docker compose up -d
curl http://localhost/
```

Visit:
- **Home**: `http://localhost/`
- **Dashboard**: `http://localhost/dashboard/`
- **API Health**: `http://localhost/api/health`

## 📁 Project Structure

```
app/
├── __init__.py                 # Flask app factory
├── config.py                   # Configuration management
├── models/
│   └── __init__.py            # SQLAlchemy User model
├── routes/
│   ├── __init__.py            # Blueprint registration
│   ├── home.py                # Home page route
│   ├── dashboard.py           # Dashboard & About routes
│   └── api.py                 # REST API endpoints
├── static/
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── dashboard.css      # Dashboard styles
│   ├── js/
│   │   ├── main.js            # Global utilities
│   │   └── dashboard.js       # Dashboard interactivity
│   └── images/                # Icons and assets
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── home.html              # Home page
│   ├── dashboard.html         # User dashboard
│   └── about.html             # About & Technology info
tests/
├── test_app.py                # Comprehensive test suite
└── conftest.py                # Pytest configuration
app.py                          # Entry point
requirements.txt                # Python dependencies
Dockerfile                       # Container image
docker-compose.yml              # Multi-container setup (Flask + MySQL + Nginx)
nginx.conf                       # Nginx reverse proxy configuration
.env.example                     # Environment variables template
.github/workflows/ci.yml         # GitHub Actions CI/CD
```

## 🎯 Key Features

### ✅ Backend Architecture
- **Modular Flask**: Factory pattern with blueprints
- **SQLAlchemy ORM**: User model with CRUD operations
- **Database**: MySQL with connection pooling
- **REST API**: /api/users, /api/health endpoints
- **Error Handling**: Graceful error responses
- **Logging**: Production-grade logging

### ✅ Frontend
- **Responsive Design**: Mobile-friendly layout
- **User Dashboard**: View, create, edit, delete users
- **Dynamic Forms**: Modal-based user management
- **Search**: Real-time user filtering
- **Pagination**: Browse users across pages
- **Modern UI**: Gradient backgrounds, smooth animations

### ✅ Database
- **User Model**: ID, username, email, name, bio, timestamps
- **Validation**: Unique constraints on username & email
- **CRUD Methods**: get_by_id, get_by_username, get_all, create, update, delete
- **Pagination**: Built-in pagination support

### ✅ DevOps
- **Docker**: Non-root user, health checks
- **Docker Compose**: MySQL + Flask + Nginx orchestration
- **Nginx**: Reverse proxy, static file serving, SSL ready
- **Systemd**: Service configs for VM deployment
- **GitHub Actions**: Test, lint, build, deploy pipeline
- **CI/CD**: Auto-deploy to EC2 on master branch push

### ✅ Testing
- **Pytest**: Comprehensive test suite
- **Coverage**: Code coverage reports
- **Database Tests**: SQLAlchemy model tests
- **API Tests**: Endpoint validation
- **Integration Tests**: Full workflow tests

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and update:

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=mysql+pymysql://user:password@host/dbname
MYSQL_DATABASE=flask_db
MYSQL_USER=flask_user
MYSQL_PASSWORD=flask_password

# Docker
APP_IMAGE=ghcr.io/lokeshsa2004/flask-devops-app:latest
```

## 📦 Deployment Options

### 1. Local Development
```bash
source venv/bin/activate
python3 -m flask run
```

### 2. Docker Single Container
```bash
docker build -t flask-devops-app:local .
docker run -p 8000:8000 flask-devops-app:local
```

### 3. Docker Compose (Full Stack)
```bash
docker compose up -d
```

Includes:
- MySQL 8.0 (port 3306)
- Flask App (port 8000, internal)
- Nginx (port 80)

### 4. Ubuntu VM with Systemd
```bash
git clone <repo> flask_app
cd flask_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo cp config/systemd/flask_app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now flask_app

sudo cp config/nginx/flask_app /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 5. AWS EC2 with GitHub Actions
- Configure secrets: `EC2_HOST`, `EC2_USER`, `EC2_KEY`
- Push to `master` branch
- Automatic testing, Docker build, GHCR push, EC2 deployment

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html

# Specific test class
pytest tests/test_app.py::TestAPIRoutes -v

# Watch mode (requires pytest-watch)
ptw tests/
```

## 📊 API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /dashboard/` - User dashboard
- `GET /dashboard/about` - About page

### API Routes
- `GET /api/health` - Health check
- `GET /api/users` - List users (paginated)
- `POST /api/users` - Create user
- `GET /api/users/<id>` - Get user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

## 🔐 Security

- Non-root container user
- Secure session cookies (HTTPONLY, SECURE, SAMESITE)
- SQL injection protection (SQLAlchemy ORM)
- CSRF protection ready
- Nginx reverse proxy isolation
- Environment-based secrets

## 📚 Stack Components

| Component | Purpose | Version |
|-----------|---------|---------|
| Python | Backend runtime | 3.11 |
| Flask | Web framework | 2.3+ |
| SQLAlchemy | ORM | 3.0+ |
| MySQL | Database | 8.0 |
| Gunicorn | WSGI server | 21+ |
| Nginx | Reverse proxy | latest |
| Docker | Containerization | latest |
| pytest | Testing | latest |

## 🛠️ Development

### Add a new route
```python
# Create app/routes/new_feature.py
from flask import Blueprint
bp = Blueprint("new_feature", __name__, url_prefix="/new")

@bp.route("/", methods=["GET"])
def index():
    return "New feature"

# Register in app/routes/__init__.py
def register_blueprints(app):
    # ... existing blueprints
    app.register_blueprint(new_feature.bp)
```

### Add a database model
```python
# Update app/models/__init__.py
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ... columns
```

### Run database migrations
```bash
flask db init  # First time only
flask db migrate -m "Add new column"
flask db upgrade
```

## 🐛 Troubleshooting

**"Access denied for user" error**
- Docker Compose: MySQL takes time to start, wait 10-15 seconds
- Ensure `docker-compose up` waits for MySQL healthcheck

**Static files not loading**
- Nginx paths must match Flask static_folder configuration
- Check Nginx config `/static/` location

**Port already in use**
- Change port in `docker-compose.yml` or `nginx.conf`
- Or kill existing container: `docker compose down`

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by Lokesh S for production-grade Flask deployment demonstrations.

## 📖 Documentation

See `docs/INSTRUCTIONS.md` for detailed deployment instructions for each platform.
