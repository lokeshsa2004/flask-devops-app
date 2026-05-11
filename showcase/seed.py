# -*- coding: utf-8 -*-

from showcase.extensions import db
from showcase.models import ShowcaseItem


def seed_if_empty() -> int:
    """Insert default rows when the table is empty. Returns number of rows inserted."""
    if ShowcaseItem.query.count() > 0:
        return 0

    rows = [
        ShowcaseItem(
            title="Flask + Gunicorn",
            summary="WSGI app server with multiple workers, structured logs, and graceful reloads.",
            image_key="card-flask.png",
            badge="Python",
            sort_order=10,
        ),
        ShowcaseItem(
            title="Nginx reverse proxy",
            summary="TLS termination, buffering, and routing user traffic to the app tier.",
            image_key="card-nginx.png",
            badge="Edge",
            sort_order=20,
        ),
        ShowcaseItem(
            title="MySQL data tier",
            summary="Relational storage for catalog content, health-checked before the app boots.",
            image_key="card-mysql.png",
            badge="Data",
            sort_order=30,
        ),
    ]
    db.session.add_all(rows)
    db.session.commit()
    return len(rows)
