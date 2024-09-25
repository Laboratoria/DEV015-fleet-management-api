from flask import Blueprint, jsonify, request
from sqlalchemy.orm import session
from app.models import Taxi
from app.database import get_db


# Create a blueprint for the taxi routes
taxis_bp = Blueprint('taxis', __name__)

@taxis_bp.route('/taxis', methods=['GET'])
def get_taxis():
    """
    Endpoint to get taxis filtered by plate and paginated.
    """
    # Get the request parameters
    plate = request.args.get('plateQuery', '').strip()
    page = int(request.args.get('pageParam', 1))  
    limit = int(request.args.get('limitParam', 10))  
    offset = (page - 1) * limit  

    # Validate the parameters
    if page < 1 or limit < 1:
        return jsonify({"error": "page or limit is not valid"}), 400

    try:
        # Use a session with context manager
        with get_db() as db:  # Replaced session with db from get_db()
            # Query with filter by 'plate' and pagination
            query = db.query(Taxi).filter(Taxi.plate.ilike(f'%{plate}%')).limit(limit).offset(offset)
            taxis = query.all()

            # Return an empty array if no taxis are found
            if not taxis:
                return jsonify([]), 200
            
            # Format the response
            taxi_list = [{'id': taxi.id, 'plate': taxi.plate} for taxi in taxis]
            return jsonify(taxi_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
