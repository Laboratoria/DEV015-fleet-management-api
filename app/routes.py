"""
módulo para rutas de endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.controllers.taxi import get_taxis
from app.controllers.trajectories import (
    select_trajectories,
    select_last_location,
    trajectories_with_plate
)
from app.controllers.users import new_user, select_users, modify_user, delete_user
from app.controllers.login import create_token
from app.extensions import bcrypt
from app.utils import token_required, list_to_excel, send_excel_email

# Definir un Blueprint para las rutas de la API
api_bp = Blueprint('api', __name__)

@api_bp.route("/taxis", methods=["GET"])
# @token_required  # Descomentar si necesitas autenticación
def endp_taxis():
    """Obtiene una lista de taxis"""

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    plate = request.args.get("plate")
    if page < 1 or limit < 1:
        return jsonify({"error": "page and limit must be greater than 0"}), 400

    response = get_taxis(page, limit, plate)
    return response

@api_bp.route("/trajectories", methods=["GET"])
@token_required
def get_trajectories():
    """Obtiene todas las ubicaciones de un taxi para una fecha específica"""
    taxi_id = request.args.get("taxiId")
    date = request.args.get("date")
    return select_trajectories(taxi_id, date)

@api_bp.route("/trajectories/latest", methods=["GET"])
@token_required
def get_last_location():
    """Obtiene la última ubicación de cada taxi"""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    return select_last_location(page, limit)

@api_bp.route("/users", methods=["POST"])
@token_required
def create_user():
    """Crea un nuevo usuario"""
    data = request.get_json()
    try:
        name = data["name"]
        email = data["email"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Falta información"}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return new_user(name, email, hashed_password)

@api_bp.route("/users", methods=["GET"])
@token_required
def get_users():
    """Obtiene una lista de usuarios"""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    return select_users(page, limit)

@api_bp.route("/users/<uid>", methods=["PATCH"])
@token_required
def update_user(uid):
    """Actualiza la información de un usuario"""
    current_user = get_jwt_identity()
    data = request.get_json()
    return modify_user(uid, current_user, data)

@api_bp.route("/users/<uid>", methods=["DELETE"])
@token_required
def delete_by_id(uid):
    """Elimina un usuario"""
    current_user = get_jwt_identity()
    return delete_user(uid, current_user)

@api_bp.route("/auth/login", methods=["POST"])
def get_token():
    """Obtiene un token de autenticación"""
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Falta información"}), 400
    return create_token(email, password)

@api_bp.route("/trajectories/export", methods=["GET"])
@token_required
def export_trajectories():
    """
    Obtiene un archivo de Excel con las ubicaciones de un taxi y
    lo envía por correo electrónico
    """
    taxi_id = request.args.get("taxiId")
    date = request.args.get("date")
    email = request.args.get("email")
    if not taxi_id or not date or not email:
        return jsonify({"error": "Faltan parámetros"}), 400
    query_list = trajectories_with_plate(taxi_id, date)
    excel_file = list_to_excel(query_list)
    return send_excel_email(email, excel_file, f"locations-{taxi_id}-{date}")