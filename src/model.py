from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #Crea instancia SQLAlchemy

class Taxi(db.Model):
    __tablename__ = 'taxis'

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), nullable=False)

    def dictionary(self):
        return{
            'id': self.id,
            'plate': self.plate
        }
    