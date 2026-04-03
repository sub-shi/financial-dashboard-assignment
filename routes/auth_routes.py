from flask import Blueprint, request, jsonify
from models.user import User
from utils.jwt_utils import generate_token
from utils.helpers import get_json_or_error

auth_bp = Blueprint("auth", __name__)

#LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data, err, status = get_json_or_error()
    if err:
        return err, status

    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = generate_token(user)      #GENERATE JWT TOKEN

    return jsonify({
        "token": token,
        "user": user.to_dict()
    })