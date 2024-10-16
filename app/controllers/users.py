"""Module controller for table users"""

from flask import jsonify
from app.models.users import Users
from app.extensions import bcrypt

def new_user(data):
    """Añade un nuevo usuario y retorna la información del usuario."""
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    print(f"Datos recibidos: {data}")


    if not email or not password:
        return jsonify({"error": "Email or password not provided"}), 400

    if Users.query.filter(Users.email == email).first():
        return jsonify({"error": "Email already exists"}), 409

    try:
        # Crear un nuevo usuario
        user = Users(name, email, password)
        print(f"-----------------------------------------Usuario a crear: {user}")

        user.create()

        # Respuesta con la información del usuario creado
        response = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify(response), 201  # 201 indica que se ha creado exitosamente
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return jsonify({"error": "An error occurred while creating the user."}), 500



def select_users(page, limit):
    """Retorna una lista de usuarios con paginación"""

    # Verifica que los parámetros de paginación sean válidos
    try:
        page = int(page)
        limit = int(limit)
        if limit <= 0:
            return jsonify({"error": "Invalid limit value"}), 400
    except ValueError:
        return jsonify({"error": "Page and limit must be integers"}), 400

    # Ejecutar la consulta con paginación
    users_query = Users.query.paginate(page=page, per_page=limit)

    # Preparar la respuesta en formato JSON
    response = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users_query.items
    ]

    return jsonify(response), 200



def modify_user(uid, current_user, data):
    """Modifica un usuario existente en la base de datos"""
    # Consulta para encontrar al usuario por UID
    user = Users.query.filter_by(id=uid).first()

    if not user:
        return None  # Usuario no encontrado

    # Si el usuario actual tiene permisos para modificar (opcional)
    if current_user != user.id:  # Este es un ejemplo básico, podrías mejorar los permisos
        raise Exception("No tienes permiso para modificar este usuario")

    # Actualizar los campos que han sido enviados
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = hash_password(data["password"])  # Asegúrate de hashear la contraseña

    # Guardar los cambios en la base de datos
    db.session.commit()
    return user



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
