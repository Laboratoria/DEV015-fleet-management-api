"""
este modulo define el modelo de la trayectoria alamacenando la data
de la trayectoria, incluyendo los campos de taxi id date latitude
y longuitud
"""
from app.database.db import db

class Trajectory(db.Model):
    """Model for storing trajectory data."""

    __tablename__ = "trajectories"
    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'),nullable=False)
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    taxi = db.relationship('Taxi', backref='trajectories')


    def __init__(self, taxi_id, date, latitude, longitude):
        """Initialize trajectory with taxi_id, date, latitude, and longitude."""
        self.taxi_id = taxi_id
        self.date = date
        self.latitude = latitude
        self.longitude = longitude