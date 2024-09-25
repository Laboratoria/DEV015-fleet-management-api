
from app import create_app

app = create_app()

if __name__ == '__main_':
    """
    Runs the Flask application in debug mode.
    """
    app.run(debug=True)  
