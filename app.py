from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Motor de la base de datos con SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaración base para los modelos
Base = declarative_base()

# Modelo de la tabla taxis
class Taxi(Base):
    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True)
    plate = Column(String)

# Configuración del logging (opcional)
# logging.basicConfig(level=logging.DEBUG)

@app.route('/taxis', methods=['GET'])
def get_taxis():
    """
    Endpoint para obtener taxis filtrados por placa y paginados.
    """
    # Obtener los parámetros de la solicitud
    plate = request.args.get('plateQuery', '')
    page = int(request.args.get('pageParam', 1))  
    limit = int(request.args.get('limitParam', 10))  
    offset = (page - 1) * limit  

    # Validación de los parámetros
    if page < 1 or limit < 1:
        return jsonify({"error": "page or limit is not valid"}), 400

    try:
        # Usando context manager para asegurar el cierre adecuado de la sesión
        with SessionLocal() as session:
            # Consulta con filtro por 'plate' y paginación
            query = session.query(Taxi).filter(Taxi.plate.ilike(f'%{plate}%')).limit(limit).offset(offset)
            taxis = query.all()

            # Retornar un array vacío si no se encuentran taxis
            if not taxis:
                return jsonify([]), 200
            
            # Formatear la respuesta
            taxi_list = [{'id': taxi.id, 'plate': taxi.plate} for taxi in taxis]
            return jsonify(taxi_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
