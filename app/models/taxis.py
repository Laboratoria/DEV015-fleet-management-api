"""
este modulo define el modelo para taxis
"""
from app.database.db import db

class Taxi(db.Model):
    """
    Modelo para la tabla de taxis en la base de datos.
    Cada taxi tiene un identificador único y una placa.
    """
    __tablename__ = "taxis"

    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    plate = db.Column(db.String(), nullable=False)  # Placa del taxi, obligatorio,

    def __init__(self, plate):
        """
        Inicializa un nuevo objeto Taxi con la placa proporcionada.
        """
        self.plate = plate

    def __repr__(self):
        """
        Devuelve una representación legible del objeto Taxi.
        """
        return f"<Taxi id={self.id}, plate={self.plate}>"