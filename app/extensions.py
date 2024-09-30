from flask import Flask
from app.controllers import get_taxis_controller


def init_routes(app: Flask):
    app.add_url_rule('/taxis', 'get_taxis', get_taxis_controller, methods=['GET'])
