from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

app = Flask(__name__)

# enviar esto a un modulo .env y luego .gitignore
DATABASE_URL = 'postgresql+psycopg2://default:LNpT4n5jdOBf@ep-proud-scene-a1ctqxby-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb'

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

# Configuración del logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/taxis', methods=['GET'])
def get_taxis():
    logging.debug('Received request to /taxis')

    """
    Endpoint para obtener taxis filtrados por placa y paginados.
    """
    # Obtener los parámetros de la solicitud
    plate = request.args.get('plateQuery', '')
    page = int(request.args.get('pageParam', 1))  
    limit = int(request.args.get('limitParam', 10))  
    offset = (page - 1) * limit  

    logging.debug(f'Filtering by plate: {plate}, Page: {page}, Limit: {limit}')

    # Validación de los parámetros
    if page < 1 or limit < 1:
        return jsonify({"error": "page or limit is not valid"}), 400

    try:
        # Usando context manager para asegurar el cierre adecuado de la sesión
        with SessionLocal() as session:
            # Consulta con filtro por 'plate' y paginación
            query = session.query(Taxi).filter(Taxi.plate.ilike(f'%{plate}%')).limit(limit).offset(offset)
            print(query)
            taxis = query.all()
            taxi_list = [{'id': taxi.id, 'plate': taxi.plate} for taxi in taxis]


            logging.debug(f'Query result: {taxis}')

            # Retornar un array vacío si no se encuentran taxis
            if not taxis:
                logging.debug('No taxis found for the given filter')
                return jsonify([]), 200
            
            # Formatear la respuesta
            taxi_list = [{'id': taxi.id, 'plate': taxi.plate} for taxi in taxis]
            logging.debug(f'Taxis found: {taxi_list}')
            
            return jsonify(taxi_list), 200

    except Exception as e:
        logging.error(f'Error fetching taxis: {str(e)}')
        return jsonify({"error": str(e)}), 500

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
