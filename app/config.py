# -*- coding: utf-8 -*-

import os
from datetime import timedelta


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_DEBUG", False)
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://flask_user:flask_password@localhost:3306/flask_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
    }

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Pagination
    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://flask_user:flask_password@localhost:3306/flask_db",
    )


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.environ.get("FLASK_ENV", "development").lower()
    return config_by_name.get(env, config_by_name["default"])
