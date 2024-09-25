from flask import Flask
from app.routes import taxis_bp
from app.models import Base
from app.database import engine


# Initialize Flask app
app = Flask(__name__)

# Create the database tables (if needed)
Base.metadata.create_all(bind=engine)

# Register the blueprint
app.register_blueprint(taxis_bp)

# Start the server
if __name__ == '__main__':
    app.run(debug=True)
