from functools import wraps
from flask import request, jsonify, g
from utils.jwt_utils import decode_token
from models.user import User
from database import db


def require_auth(allowed_roles=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Token missing"}), 401

            try:
                token = auth_header.split(" ")[1]
            except (IndexError, ValueError):
                return jsonify({"error": "Invalid token format"}), 401

            payload = decode_token(token)

            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            # Get user from DB
            user = db.session.get(User, payload["user_id"])

            if not user or not user.is_active:
                return jsonify({"error": "User inactive"}), 403

            # Role check
            if allowed_roles and payload["role"] not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            # Attach user to request context
            g.user = user

            return func(*args, **kwargs)

        return wrapper
    return decorator