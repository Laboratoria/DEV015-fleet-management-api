"""Module controller for table users"""

from flask import jsonify
from app.models.users import Users
from app.extensions import bcrypt

def new_user(data):
    """Añade un nuevo usuario y retorna la información del usuario."""
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password not provided"}), 400

    if Users.query.filter(Users.email == email).first():
        return jsonify({"error": "Email already exists"}), 409

    # Crear un nuevo usuario
    user = Users(name, email, password)
    user.create()

    # Respuesta con la información del usuario creado
    response = {"id": user.id, "name": user.name, "email": user.email}
    return jsonify(response), 201  # 201 indica que se ha creado exitosamente



def select_users(page, limit):
    """Returna lista de usuarios"""
    users_query = Users.query.paginate(page=page, per_page=limit)
    response = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users_query.items
    ]

    return jsonify(response), 200


def modify_user(uid, current_user, data):
    """modifica la informacion del usuario y retorna la nueva data"""
    user = Users.query.filter((Users.email == uid) | (Users.id == uid)).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    if current_user != user.id:
        return jsonify({"error": " Only the user can modify their own data."}), 403

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        if not data["password"]:
            return jsonify({"error": "New password cannot be empty"}), 400
        user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

        user.update()
        response = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify(response), 200


def delete_user(uid, current_user):
    """borrs usuers y retorna la infromacion de usuario"""
    user = Users.query.filter((Users.email == uid) | (Users.id == uid)).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    if current_user != user.id:
        return jsonify({"error": "Permission denied."}), 403

    response = {"id": user.id, "name": user.name, "email": user.email}
    user.delete()
    return jsonify(response), 204

