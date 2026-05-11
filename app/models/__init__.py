# -*- coding: utf-8 -*-

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def create_user(cls, username, email, first_name=None, last_name=None, bio=None):
        """Create a new user"""
        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        """Get user by username"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls, page=1, per_page=10):
        """Get all active users with pagination"""
        return cls.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def update(self, **kwargs):
        """Update user attributes"""
        allowed_fields = {
            "first_name",
            "last_name",
            "email",
            "bio",
            "is_active",
        }
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """Delete user"""
        db.session.delete(self)
        db.session.commit()
