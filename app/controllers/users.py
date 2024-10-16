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
    """Returna lista de usuarios"""
    users_query = Users.query.paginate(page=page, per_page=limit)
    response = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users_query.items
    ]

    return jsonify(response), 200

def modify_user(uid, current_user, data):
    """Modifica la información del usuario y retorna la nueva data actualizada."""
    # Buscamos al usuario por ID (asumiendo que `uid` es el ID del usuario)
    user = Users.query.filter_by(id=uid).first()

    if not user:
        return jsonify({"error": "User does not exist"}), 404

    # Solo el usuario puede modificar su propia información
    if current_user != user.id:
        return jsonify({"error": "You can only modify your own data."}), 403

    # Validación y actualización de los campos proporcionados en `data`
    if "name" in data:
        if not data["name"]:  # Validar que el nombre no esté vacío
            return jsonify({"error": "Name cannot be empty"}), 400
        user.name = data["name"]

    if "email" in data:
        if not data["email"]:  # Validar que el email no esté vacío
            return jsonify({"error": "Email cannot be empty"}), 400
        # Validar formato de email (opcional, puedes usar un regex si es necesario)
        user.email = data["email"]

    if "password" in data:
        if not data["password"]:  # Validar que la contraseña no esté vacía
            return jsonify({"error": "New password cannot be empty"}), 400
        # Encriptar la nueva contraseña antes de guardarla
        user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    # Actualizar los datos del usuario en la base de datos
    try:
        user.update()  # Método que guarda los cambios
        response = {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        return jsonify(response), 200
    except Exception as e:
        print(f"Error al actualizar el usuario: {e}")
        return jsonify({"error": "An error occurred while updating the user."}), 500



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