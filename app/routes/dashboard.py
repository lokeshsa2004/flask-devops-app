# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify

from app.models import User

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET"])
def dashboard():
    """Dashboard page - displays user data"""
    page = request.args.get("page", 1, type=int)
    
    try:
        pagination = User.get_all(page=page, per_page=10)
        users = pagination.items
    except Exception as e:
        # If database is not available, show empty dashboard
        users = []
        pagination = type('obj', (object,), {
            'items': [],
            'total': 0,
            'pages': 1,
            'has_prev': False,
            'has_next': False
        })()

    return render_template(
        "dashboard.html",
        users=users,
        pagination=pagination,
        page=page,
    )


@bp.route("/about", methods=["GET"])
def about():
    """About page"""
    return render_template("about.html")
