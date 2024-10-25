"""
módulo para pruebas unitarias endopoint delete
"""
import pytest
from app.api import create_app
from app.database import db
from app.models.users import Users

@pytest.fixture
"""
"""
def client():
