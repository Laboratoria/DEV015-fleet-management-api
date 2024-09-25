from flask import Blueprint, jsonify, request
from app.services import fetch_taxis

taxis_bp = Blueprint('taxis', __name__)

@taxis_bp.route('/taxis', methods=['GET'])
def get_taxis():
    plate = request.args.get("plate", type=str, default=None)
    page = request.args.get("page", type=int, default=1)
    limit = request.args.get("limit", type=int, default=10)

    if page < 1 or limit < 1:
        return jsonify({"error": "Page number and limit must be greater than 0."}), 400

    try:
        taxis_data = fetch_taxis(plate, page, limit)

        if not taxis_data['taxis']:
            return jsonify({"message": "No taxis found"}), 404

        return jsonify(taxis_data), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
