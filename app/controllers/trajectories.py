""" modulo para gestionar la consulta de trayectorias
"""
from datetime import datetime

from flask import jsonify, abort
from sqlalchemy import func

from app.database.db import db
from app.models.taxis import Taxi
from app.models.trajectories import Trajectory



def validate_date(date_str):
    """funcion que valida y ananliza la fecha"""
    try:
        year=date_str[6:]
        month=date_str[3:5]
        day=date_str[:2]
        date_str2= year+"-"+month+"-"+day

        return datetime.strptime(date_str2, "%Y-%m-%d")
    except ValueError:
        abort(400, description="Invalid date format. Expected YYYY-MM-DD.")


def select_trajectories(taxi_id, date=None):
    """
    Retorna todas las trayectorias del taxi y opconalmente filtra por fecha
    """
    #print ("fecha--", date)
    #query = Trajectory.query.filter_by(taxi_id=taxi_id)
    #print (taxi_id)
# Verificar si el taxi_id es válido
    if not taxi_id:
        abort(400, description="Taxi ID is required.")

    # Verificar si se requiere fecha y no se proporciona
    if not date:
        abort(400, description="Date is required.")

    if date:
        parsed_date = validate_date(date)

        query = Trajectory.query.filter(
            Trajectory.taxi_id == taxi_id,
            func.date(Trajectory.date) == parsed_date
        )

    else:
        query = Trajectory.query.filter(Trajectory.taxi_id == taxi_id)

    trajectories = query.all()
    #print ("taxi despues del queryyyyyyyyyy", taxi_id)
    if not trajectories:
        # Arrojar un error 404 si no se encuentra el taxi_id
        abort(404, description="Taxi ID not found.")
    response = [
        {
            "id": trajectory.id,
            "taxiId": trajectory.taxi_id,
            "date": trajectory.date,
            "latitude": trajectory.latitude,
            "longitude": trajectory.longitude
        } for trajectory in trajectories
    ]

    print("respuesta de trayectorias", response)

    return jsonify(response)


def select_last_location(page, limit):
    """Retorna el historial de la trayectoria para cada taxi."""
    try:
        subquery = (
            db.session.query(func.max(Trajectory.id).label("max_id"), Trajectory.taxi_id)
            .group_by(Trajectory.taxi_id)
            .subquery()
        )

        last_location_query = (
            db.session.query(Trajectory)
            .join(subquery, Trajectory.id == subquery.c.max_id)
            .join(Taxi, Taxi.id == Trajectory.taxi_id)
            .paginate(page=page, per_page=limit)
        )

        response = [
            {
                "taxiId": taxi.taxi_id,
                "plate": taxi.taxi.plate.strip(),
                "date": taxi.date.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": taxi.date.isoformat(),
                "latitude": taxi.latitude,
                "longitude": taxi.longitude
            } for taxi in last_location_query.items
        ], 200

        return (response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Manejo de errores



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
    ],200
    return response
