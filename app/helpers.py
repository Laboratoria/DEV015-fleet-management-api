"""
Funciones pequeñas reciclables
"""

from flask import jsonify
from app.models.users import Users

def get_user_by_uid(uid):
    """Helper to get user by email or ID"""
    return Users.query.filter((Users.email if "@" in uid else Users.id) == uid).first()

def error_response(message, status_code):
    """Helper to generate error responses"""
    return jsonify({"error": message}), status_code

def success_response(user):
    """Helper to generate success responses"""
    return jsonify({"id": user.id, "name": user.name, "email": user.email})
