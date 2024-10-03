"""gestión de la tabal ade taxis
"""
from flask import jsonify
from app.models.taxis import Taxi

def get_taxis(page, limit):
    """
    retrona la paginacion de los taxis con informacion de la placa
    """
    taxis_paginated = Taxi.query.paginate(page=page, per_page=limit, error_out=False)
    response= [
        {"id": taxi.id, "plate": taxi.plate}
        for taxi in taxis_paginated.items
    ]

    return jsonify(response)
