from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base declarative for models
Base = declarative_base()

# Taxi model
class Taxi(Base):
    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, index=True)  # Use String instead of VARCHAR
