"""
módulo par agestionar a los usuarios
"""
from flask import jsonify

from app.helpers import get_user_by_uid, error_response, success_response
from app.models.users import Users
from app.extensions import bcrypt

def new_user(name, email, password):
    """Agrega un nuevo usuario a la tabla y retorna mas informacion"""
    if not email or not password:
        return error_response("Email or password not provided", 400)
    if Users.query.filter(Users.email == email).first():
        return error_response("Email already exists", 409)
    user = Users(name, email, password)
    user.create()
    return success_response(user)


def select_users(page, limit):
    """Retorna la lista de usuarios"""
    users_query = Users.query.paginate(page=page, per_page=limit)
    response = [success_response(user).json for user in users_query.items]
    return jsonify(response)

def modify_user(uid, current_user, data):
    """Modifies user's information and returns the new data"""
    user = get_user_by_uid(uid)
    if not user:
        return error_response("User does not exist", 404)
    if current_user == user.id:
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        user.update()
        return success_response(user)
    return error_response("Only the user can modify their own data", 400)

def delete_user(uid, current_user):
    """Deletes user and returns deleted user's information"""
    user = get_user_by_uid(uid)  # Helper to get user by ID or email
    if not user:
        return error_response("User does not exist", 404)
    if current_user == user.id:
        response = success_response(user).json  # Success response before deletion
        user.delete()
        return jsonify(response)
    return error_response("Only the user can delete their own profile", 400)