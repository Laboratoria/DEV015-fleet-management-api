"""
Módulo para crear la app
"""
from flask import Flask
from flask_jwt_extended import JWTManager  # Importación correcta
from app.config import Config
from app.extensions import bcrypt, mail
from app.routes import api_bp
from app.database.db import db

def create_app():
    """
    Crea la aplicación Flask y configura las extensiones.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    JWTManager(app)  # Elimina la variable `jwt` si no la necesitas

    # Registra las rutas
    app.register_blueprint(api_bp)

    return app
