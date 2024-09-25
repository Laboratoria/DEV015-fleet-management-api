import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
arr_url = os.getenv('DATABASE')

db = SQLAlchemy()
