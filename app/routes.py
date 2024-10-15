"""
módulo para rutas de endpoints
"""

from flask import Blueprint, request, jsonify

from app.controllers.taxi import get_taxis
from app.controllers.trajectories import select_trajectories
from app.controllers.trajectories import select_last_location
from app.controllers.users import new_user
from app.controllers.users import select_users
from app.controllers.users import modify_user
from app.controllers.users import delete_user
#from app.extensions import bcrypt


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
#@token_required
def get_trajectories():
    """Obtiene todas las ubicaciones de un taxi para una fecha específica"""
    taxi_id = request.args.get("taxiId", type=str)
    date = request.args.get("date", type=str)

    return select_trajectories(taxi_id, date)

@api_bp.route("/trajectories/latest", methods=["GET"])
#@token_required
def get_last_location():
    """Obtiene la última ubicación de cada taxi"""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    return select_last_location(page, limit)


@api_bp.route("/users", methods=["POST"])
def create_user():
    """Creates a new user"""
    data = request.get_json()
    print (data)
    return new_user (data)



@api_bp.route("/users", methods=["GET"])
# @token_required
def get_users():
    """Obtiene la lista de todos los usuarios paginada"""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    return select_users(page, limit)

@api_bp.route("/users/<uid>", methods=["PUT"])
# @token_required
def update_user(uid):
    """Actualiza la información de un usuario existente"""
    current_user = request.args.get("currentUser", type=int)
    data = request.get_json()

    return modify_user(uid, current_user, data)

@api_bp.route("/users/<uid>", methods=["DELETE"])
# @token_required
def de_user(uid):
    """Elimina un usuario existente"""
    current_user = request.args.get("currentUser", type=int)
    return delete_user(uid, current_user)