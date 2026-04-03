from flask import Blueprint, request, jsonify
from models.user import User
from models.role import Role
from database import db
from utils.decorators import require_auth
from utils.helpers import get_json_or_error

user_bp = Blueprint("users", __name__)

#CREATE USER
@user_bp.route("/", methods=["POST"])
@require_auth(["admin"])
def create_user():
    data, err, status = get_json_or_error()
    if err:
        return err, status

    name = data.get("name")
    email = data.get("email")
    role_name = data.get("role")

    if not name or not email or not role_name:
        return jsonify({"error": "Missing fields"}), 400               

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(
        name=name,
        email=email,
        role_id=role.id
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201



#GET USERS
@user_bp.route("/", methods=["GET"])
@require_auth(["admin"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])



#UPDATE USERS
@user_bp.route("/<int:id>", methods=["PUT"])
@require_auth(["admin"])
def update_user(id):
    user = User.query.get_or_404(id)
    data, err, status = get_json_or_error()
    if err:
        return err, status

    # Update role
    if "role" in data:
        role = Role.query.filter_by(name=data["role"]).first()
        if not role:
            return jsonify({"error": "Invalid role"}), 400
        user.role_id = role.id

    # Update active status
    if "is_active" in data:
        user.is_active = data["is_active"]

    db.session.commit()

    return jsonify(user.to_dict())

