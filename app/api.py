"""
definicion de rutas y maneja las solicitudes HTTP
"""
from flask import Flask, request
#from flask_jwt_extended import JWTManager, get_jwt_identity

from app.database.db import db
from app.controllers.taxi import get_taxis
from app.controllers.trajectories import select_trajectories
from app.controllers.trajectories import select_last_location
#falata la funcion de trayectoria con placa
#importar funciones de users
#importar login

from app.config import Config
#importar encriptacion
#importar herramientas de usuarios email

def create_app():
    """Creates routes"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    #bcrypt.init_app(app)  # Initializes bcrypt
    #mail.init_app(app)  # Initializes flask-mail
    #jwt = JWTManager(app)

#primer endpoint
    @app.route("/taxis", methods=["GET"])
    #@token_required
    def endp_taxis():
        """Gets listas de taxis """
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return get_taxis(page, limit)

#segundo endpoint
    @app.route("/trajectories", methods=["GET"])
    #@token_required

    def endp_trajectories():
        """ get la localizacion de un taxi por fechas"""
        taxi_id = request.args.get("taxiId")
        date = request.args.get("date")
        return select_trajectories(taxi_id, date)

#tercer endpoint
    @app.route("/trajectories/latest", methods=["GET"])
    #@token_required
    def get_last_location():
        """Gets la ultima localizacion de cada taxi"""
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)
        return select_last_location(page, limit)



#cuarto endopoint users

    return app
