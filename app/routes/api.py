# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import User, db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    try:
        # Try to execute a simple query
        db.session.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e), "database": "disconnected"}), 503


@bp.route("/users", methods=["GET"])
def get_users():
    """Get all active users as JSON"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        pagination = User.get_all(page=page, per_page=per_page)
        users = [user.to_dict() for user in pagination.items]

        return jsonify(
            {
                "users": users,
                "total": pagination.total,
                "pages": pagination.pages,
                "current_page": page,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": str(e), "users": [], "total": 0, "pages": 0, "current_page": 1}), 503


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = User.get_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@bp.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        bio = data.get("bio")

        if not username or not email:
            return jsonify({"error": "username and email are required"}), 400

        user = User.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 503


@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user"""
    try:
        user = User.get_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user.update(**data)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 503


@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.get_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.delete()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 503
