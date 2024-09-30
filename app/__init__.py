from flask import Flask
from config import Config

from databases import db
from routes import init_routes

def create_app():
    app = Flask(__name__)

    # Configurar la URL de la base de datos directamente desde Config
    app.config.from_object(Config)

    # Inicializar la base de datos con la app
    db.init_app(app)

    # Crear las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()

    # Inicializar las rutas
    init_routes(app)

    return app
