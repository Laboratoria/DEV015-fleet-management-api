from app.databases import db
from sqlalchemy import Column, Integer, VARCHAR

class taxi(db.Model):
    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True)
    plate = Column(VARCHAR)

    def __repr__(self):
        return f"<Taxi {self.plate}>"

