"""
Claves y variabels de entorno
"""

import os
#from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuracion """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
