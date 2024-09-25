from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

# Create the engine using the database URL from the config
engine = create_engine(Config.DATABASE_URL)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a session for use in the application
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
