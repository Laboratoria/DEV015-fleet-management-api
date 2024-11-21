"""Module for token creation"""

from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.models.users import Users
from app.extensions import bcrypt


def create_token(email, password):
    """Creates authentication token"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = Users.query.filter(Users.email == email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        response = {
            "accessToken": access_token,
            "user": {"id": user.id, "email": user.email}
        }
        return jsonify(response), 200
    return jsonify({"error": "Email or password incorrect"}), 404
