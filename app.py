# Para poder trabajar con las variables de entorno
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Importa load_dotenv de la librería de python-dotenv, para cargar las variables de entorno
from dotenv import load_dotenv

#Cargar variable de entorno
load_dotenv(dotenv_path='.env.development.local')

app = Flask(__name__)

# Se carga la variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#Crea una instancia de SQLAlchemy y la vincula con Flask
db = SQLAlchemy(app)

# Aquí se define el endpoint y responde a la petición 'GET'
@app.route('/taxis', methods=['GET'])
def get_taxis():
    return "Hola mundo", 200

if __name__ == '__main__':
    app.run(debug=True)
