# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from showcase import create_app  # noqa: E402
from showcase.extensions import db  # noqa: E402
from showcase.models import ShowcaseItem  # noqa: E402
from showcase.seed import seed_if_empty  # noqa: E402


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with application.app_context():
        db.create_all()
        seed_if_empty()
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert b"StackForge Showcase" in response.data


def test_home_includes_stylesheet(client):
    response = client.get("/")
    assert b'rel="stylesheet"' in response.data


def test_api_items_json(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) >= 3
    assert all("title" in item and "image_url" in item for item in payload["items"])


def test_api_health_ok(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload.get("ok") is True


def test_unknown_route_404(client):
    assert client.get("/nope").status_code == 404


def test_seed_is_idempotent(app):
    with app.app_context():
        before = ShowcaseItem.query.count()
        assert before >= 1
        inserted = seed_if_empty()
        assert inserted == 0
        assert ShowcaseItem.query.count() == before
