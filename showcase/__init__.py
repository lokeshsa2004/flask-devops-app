# -*- coding: utf-8 -*-

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from showcase.extensions import db
from showcase.routes import bp as showcase_bp


def create_app(config_overrides=None):
    """Application factory for StackForge Showcase."""
    load_dotenv()

    root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(root / "templates"),
        static_folder=str(root / "static"),
        static_url_path="/static",
    )

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    default_sqlite = "sqlite:///" + str(root / "instance" / "stackforge.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", default_sqlite
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    app.register_blueprint(showcase_bp)

    @app.cli.command("init-db")
    def init_db_command():
        """Create tables and seed demo content."""
        from showcase.seed import seed_if_empty

        with app.app_context():
            os.makedirs(root / "instance", exist_ok=True)
            db.create_all()
            inserted = seed_if_empty()
            print(f"init-db: tables ready, seeded {inserted} rows")

    return app
