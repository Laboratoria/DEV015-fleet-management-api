"""
modulo con configuracion de db
"""
class Config:
    """
    variables de entorno
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://default:LNpT4n5jdOBf@ep-proud-scene-a1ctqxby-pooler.ap-southeast-1.aws.neon.tech:5432/verceldb' # pylint: disable=C0301
    #POSTGRES_USER="default"
    #POSTGRES_PASSWORD="LNpT4n5jdOBf"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
