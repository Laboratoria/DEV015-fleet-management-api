"""
Módulo para la gestión de la tabla de taxis.
Contiene funciones para obtener información sobre taxis.

"""
from app.models.taxis import Taxi

def get_taxis(page, limit, plate=None):
    """
    Retorna la paginación de los taxis con información de la placa.

    :param page: Número de página para la paginación.
    :param limit: Número de taxis por página.
    :param plate: Placa del taxi para filtrar.
    :return: JSON con la lista de taxis.
    """
    query = Taxi.query

    if plate:  # Si se proporciona una placa, filtrar por ella
        query = query.filter(Taxi.plate.ilike(f"%{plate}%"))

    taxis_paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return [
        {"id": taxi.id, "plate": taxi.plate}
        for taxi in taxis_paginated.items
    ] , 200
