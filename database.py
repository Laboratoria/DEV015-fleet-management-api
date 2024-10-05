from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgres://default:jZ1GA5JOmipk@ep-tiny-sky-a4nu73yw-pooler.us-east-1.aws.neon.tech:5432/verceldb"

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir modelo
class Taxi(Base):
    """Modelo para la tabla 'taxis'."""
    __tablename__ = "taxis"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, index=True)

# Crear tablas
Base.metadata.create_all(bind=engine)
