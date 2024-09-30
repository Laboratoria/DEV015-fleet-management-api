from app.database.db import db

class taxi(db.Model):
      __tablename__ = "taxis"

      id = db.Column(db.Integer, primary_key=True)
      plate = db.Column(db.String(), nullable=False) 


      def __init__(self, plate):
        self.plate = plate
 #para debbug
      def __repr__(self):
        return f"<Taxi id={self.id}, plate={self.plate}>"