import bcrypt #fix
from app.database.db import db

class Users(db.Model):
    """Class for table users"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)  # Hash the password

    def hash_password(self, password):
        """Hashes the password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')  # Store as a string in the database

    def check_password(self, password):
        """ comprueba si la contraseña ingresada hacae match con la cifrada"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def create(self):
        """Añadir nuevo usuario a la tabla"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Añadir tablas """
        db.session.commit()

    def delete(self):
        """Borrar el usuario de la tabla """
        db.session.delete(self)
        db.session.commit()
