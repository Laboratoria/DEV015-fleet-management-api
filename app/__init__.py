from flask import Flask
from app.databases import db,arr_url
from app.routes import taxis_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = arr_url  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Inicializa SQLAlchemy con la app
    
    # Registro de Blueprints
    app.register_blueprint(taxis_bp)

    # Crear la base de datos
    with app.app_context():
        db.create_all()

    return app
