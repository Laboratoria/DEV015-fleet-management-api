"""
módulo para rutas de endpoints
"""

from flask import Blueprint, request, jsonify

from app.controllers.taxi import get_taxis
from app.controllers.trajectories import select_trajectories
from app.controllers.trajectories import select_last_location

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

