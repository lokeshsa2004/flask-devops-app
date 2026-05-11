# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET"])
def index():
    """Home page - serves as landing page"""
    return render_template("home.html")
