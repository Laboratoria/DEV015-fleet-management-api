"""
Módulo para la gestión de la tabla de taxis.
Contiene funciones para obtener información sobre taxis.

"""
from flask import jsonify
from app.models.taxis import Taxi

def get_taxis(page, limit):
    """
    Retorna la paginación de los taxis con información de la placa.

    :param page: Número de página para la paginación.
    :param limit: Número de taxis por página.
    :return: JSON con la lista de taxis.
    """
    taxis_paginated = Taxi.query.paginate(page=page, per_page=limit, error_out=False)
    response = {
        "total": taxis_paginated.total,
        "page": page,
        "per_page": limit,
        "taxis": [
            {"id": taxi.id, "plate": taxi.plate}
            for taxi in taxis_paginated.items
        ]
    }

    return jsonify(response), 200
