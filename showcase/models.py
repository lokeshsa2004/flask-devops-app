# -*- coding: utf-8 -*-

from showcase.extensions import db


class ShowcaseItem(db.Model):
    """A catalog row for the StackForge showcase (stored in MySQL or SQLite)."""

    __tablename__ = "showcase_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    # Relative to static/img/, e.g. "card-flask.png"
    image_key = db.Column(db.String(200), nullable=False)
    badge = db.Column(db.String(64), nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
