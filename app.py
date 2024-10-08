import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Crear la conexión a la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = Flask(__name__)

# Configuración de base de datos
DATABASE_URL = "postgres://default:jZ1GA5JOmipk@ep-tiny-sky-a4nu73yw-pooler.us-east-1.aws.neon.tech:5432/verceldb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir el modelo Taxi
class Taxi(Base):
    __tablename__ = "taxis"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, index=True)

# Crear la base de datos
Base.metadata.create_all(bind=engine)

# Endpoint para listar taxis con paginación y filtrado
@app.route('/taxis', methods=['GET'])
def get_taxis():
    session = SessionLocal()
    
    # Obtener parámetros de paginación y filtrado
    plate_filter = request.args.get('plate')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Construir la consulta
    query = session.query(Taxi)
    
    if plate_filter:
        query = query.filter(Taxi.plate.ilike(f'%{plate_filter}%'))

    # Paginación
    taxis = query.offset((page - 1) * per_page).limit(per_page).all()

    # Preparar la respuesta
    result = [{"id": taxi.id, "plate": taxi.plate} for taxi in taxis]
    
    # Retornar como JSON
    return jsonify(result)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
