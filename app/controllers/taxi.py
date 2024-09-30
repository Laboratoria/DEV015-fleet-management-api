from flask import jsonify
from app.models.taxis import taxis

def get_taxis(page, limit):
    taxis_query = taxis.query.paginate(page=page, limit=limit)
    response = []
    for taxis in taxis_query.items:
        taxi_info = {"id": taxi.id, "plate": taxi.plate}
        response.append(taxi_info)
    return jsonify(response)
