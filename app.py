# Para poder trabajar con las variables de entorno
import os 
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
# Importa load_dotenv de la librería de python-dotenv, para cargar las variables de entorno
from dotenv import load_dotenv

#Cargar variable de entorno
load_dotenv(dotenv_path='.env.development.local') 

app = Flask(__name__)

# Se carga la variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#Crea una instancia de SQLAlchemy y la vincula con Flask
db = SQLAlchemy(app) 

# Modelo
class Taxi(db.Model):
    __tablename__ = 'taxis'

    id = db.Column(db.Integer, primary_key = True)
    plate = db.Column(db.String(20), nullable=False)

    #Método
    def dictionary(self):
        return{
            'id': self.id,
            'plate': self.plate
        }

# Endpoint: responde a la petición 'GET'
@app.route('/taxis', methods=['GET'])
def get_taxis():

    # Params de consulta de la solicitud HTTP
    plate = request.args.get('plate')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    # Realiza consulta en la tabla Taxis
    database_query = Taxi.query

    if plate:
        filtered_query = database_query.filter(Taxi.plate.like('%'+plate+'%'))
    else:
        filtered_query = database_query.filter(Taxi.plate == '')

    # Paginar los resultados  
    taxis = filtered_query.paginate(page=page, per_page=limit)
    
    return jsonify([taxi.dictionary() for taxi in taxis]), 200
    
if __name__ == '__main__':
    app.run(debug=True)
