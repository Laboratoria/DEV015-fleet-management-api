"""ejecución de la API"""
from flask_migrate import Migrate

from app.api import create_app
from app.database.db import db

app = create_app()
migrate = Migrate (app, db)

if __name__ == "__main__":
    app.run(debug=True)
