#se inicializa el paquete de la aplicacion

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import taxis_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxis.db'  # Cambia esto según tu base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Inicializa SQLAlchemy con la app
    
    # Registro de Blueprints
    app.register_blueprint(taxis_bp)

    # Crear la base de datos
    with app.app_context():
        db.create_all()

    return app
