"""Módulo controlador para la tabla de usuarios"""

from flask import jsonify
from app.models.users import Users
from app.extensions import bcrypt

def new_user(data):
    """Añade un nuevo usuario y retorna la información del usuario."""
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    print(f"Datos recibidos: {data}")

    # Validar campos requeridos
    if not email or not password:
        return jsonify({"error": "Email or password not provided"}), 400

    # Comprobar si el email ya existe
    if Users.query.filter(Users.email == email).first():
        return jsonify({"error": "Email already exists"}), 409

    try:
        # Crear un nuevo usuario
        user = Users(name=name, email=email, password=password)
        print(f"-----------------------------------------Usuario a crear: {user}")

        user.create()  # Método para guardar en la base de datos

        # Respuesta con la información del usuario creado
        response = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify(response), 201  # 201 indica que se ha creado exitosamente
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return jsonify({"error": "An error occurred while creating the user."}), 500

def select_users(page, limit):
    """Retorna lista de usuarios paginada."""
    users_query = Users.query.paginate(page=page, per_page=limit)
    response = [
        {"id": user.id, "name": user.name, "email": user.email} for user in users_query.items
    ]

    return jsonify(response), 200

def modify_user(uid, data):
    """Modifica la información del usuario y retorna la nueva data actualizada."""
    user = Users.query.filter_by(id=uid).first()
    print("AQUI ESTA IUD ------------------------------",uid)
    # Verificar si el usuario existe
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    # Comprobar si el cuerpo de la solicitud está vacío (es decir, contiene solo un objeto vacío)
    if not data or (len(data) == 1 and 'name' not in data):
        return jsonify({"error": "No body provided"}), 400

    # Comprobar si se está intentando actualizar el email o la contraseña
    if 'email' in data or 'password' in data:
        return jsonify({"error": "Cannot update email or password"}), 400

    # Actualizar los campos según lo que venga en la solicitud
    if "name" in data:
        user.name = data["name"]

    try:
        user.update()  # Guardar los cambios en la base de datos
        response = {
            "id": user.id,  # Retornar el ID del usuario actualizado
            "name": user.name,
            "email": user.email
        }
        return response, 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



def check_user_exists(uid):
    """
    Verifica si un usuario existe en la base de datos.

    :param uid: ID del usuario a verificar
    :return: True si el usuario existe, False en caso contrario
    """
    user = Users.query.filter_by(id=uid).first()  # Obtener usuario por ID

    # Devuelve True si el usuario existe, False si no
    return user is not None

def delete_user(uid, current_user):
    """Borra un usuario y retorna la información del usuario."""
    user = Users.query.filter((Users.email == uid) | (Users.id == uid)).first()

    # Verificar si el usuario existe
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    # Verificar permisos
    if current_user != user.id:
        return jsonify({"error": "Permission denied."}), 403

    response = {"id": user.id, "name": user.name, "email": user.email}
    try:
        user.delete()  # Método para eliminar de la base de datos
        return jsonify(response), 200  # Cambiar a 200 OK después de eliminar
    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")
        return jsonify({"error": "An error occurred while deleting the user."}), 500
