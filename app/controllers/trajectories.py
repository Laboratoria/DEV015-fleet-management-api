""" modulo para gestionar la consulta de trayectorias
"""
from datetime import datetime

from flask import jsonify, abort
from sqlalchemy import func

from app.models.taxis import Taxi
from app.models.trajectories import Trajectory



def validate_date(date_str):
    """funcion que valida y ananliza la fecha"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        abort(400, description="Invalid date format. Expected YYYY-MM-DD.")


def select_trajectories(taxi_id, date=None):
    """
    Retorna todas las trayectorias del taxi y opconalmente filtra por fecha
    """
    query = Trajectory.query.filter_by(taxi_id=taxi_id)

    if date:
        parsed_date = validate_date(date)
        query = query.filter(func.date(Trajectory.date) == parsed_date.date())

    trajectories = query.all()

    response = [
        {
            "id": trajectory.id,
            "taxi_id": trajectory.taxi_id,
            "date": trajectory.date,
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude
        } for trajectory in trajectories
    ]

    return jsonify(response)


def select_last_location(page, limit):
    """Retorna el rhistroial de la trauectoria para cada taxi"""
    subquery = (func.max(Trajectory.id).label("max_id"))
    last_location_query = (
        Trajectory.query
        .join(Taxi, Taxi.id == Trajectory.taxi_id)
        .filter(Trajectory.id.in_(subquery))
        .paginate(page=page, per_page=limit)
    )

    response = [
        {
            "taxi_id": taxi.taxi_id,
            "plate": taxi.taxi.plate,
            "date": taxi.date,
            "latitude": taxi.latitude,
            "longitude": taxi.longitude
        } for taxi in last_location_query.items
    ]

    return jsonify(response)


def trajectories_with_plate(taxi_id, date=None):
    """retorna todas la trayectorias por cada taxi incluyendo la placa y si se filtra por fecha
    """
    query = Trajectory.query.join(Taxi, Taxi.id == Trajectory.taxi_id).filter_by(taxi_id=taxi_id)

    if date:
        parsed_date = validate_date(date)
        query = query.filter(func.date(Trajectory.date) == parsed_date.date())

    trajectories = query.all()

    response = [
        {
            "taxi_id": trajectory.taxi_id,
            "plate": trajectory.taxi.plate,
            "date": trajectory.date,
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude
        } for trajectory in trajectories
    ]

    return jsonify(response)