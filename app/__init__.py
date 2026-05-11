# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate

from app.config import get_config
from app.models import db
from app.routes import register_blueprints


def create_app(config=None):
    """Application factory pattern"""

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    )

    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    register_blueprints(app)

    # Create tables (only if database is available)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Could not create database tables: {e}")

    # Setup logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app


def setup_logging(app):
    """Setup application logging"""

    if app.debug:
        return

    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "flask_app.log"), maxBytes=10240000, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask app startup")


def register_error_handlers(app):
    """Register error handlers"""

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f"Server error: {error}")
        return {"error": "Internal server error"}, 500

    @app.shell_context_processor
    def make_shell_context():
        """Add objects to shell context"""
        return {"db": db}
