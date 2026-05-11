# -*- coding: utf-8 -*-

"""WSGI entrypoint for Gunicorn: ``gunicorn app:app``."""

from showcase import create_app

app = create_app()
