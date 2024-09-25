from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # Get the DATABASE_URL from the environment variables
    DATABASE_URL = os.getenv('DATABASE_URL')
