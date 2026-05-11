# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, url_for
from sqlalchemy import text

from showcase.extensions import db
from showcase.models import ShowcaseItem

bp = Blueprint("showcase", __name__)


@bp.route("/")
def home():
    items = ShowcaseItem.query.order_by(
        ShowcaseItem.sort_order.asc(), ShowcaseItem.id.asc()
    ).all()
    return render_template(
        "index.html",
        items=items,
        hero_image=url_for("static", filename="img/hero-stackforge.png"),
    )


@bp.route("/api/items")
def api_items():
    rows = ShowcaseItem.query.order_by(
        ShowcaseItem.sort_order.asc(), ShowcaseItem.id.asc()
    ).all()
    return jsonify(
        {
            "items": [
                {
                    "id": r.id,
                    "title": r.title,
                    "summary": r.summary,
                    "badge": r.badge,
                    "image_url": url_for("static", filename=f"img/{r.image_key}"),
                }
                for r in rows
            ]
        }
    )


@bp.route("/api/health")
def api_health():
    """Lightweight readiness: verifies DB connectivity."""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"ok": True, "database": "reachable"})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "database": "error", "detail": str(exc)}), 503
