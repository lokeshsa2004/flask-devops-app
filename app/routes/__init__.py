# -*- coding: utf-8 -*-

from . import api, dashboard, home


def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(home.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(api.bp)
