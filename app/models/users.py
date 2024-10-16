""" métodos para lo ususarios
"""
from app.database.db import db

class Users(db.Model):
    """Class for table users"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)  # Cifrar la contraseña

    def hash_password(self, password):
        """Cifra la contraseña usando operaciones básicas (sin importar nada externo)"""
        hashed = ""
        for char in password:
            hashed += str(ord(char) + 3)
        return hashed

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con la cifrada"""
        return self.password == self.hash_password(password)

    def create(self):
        """Añadir nuevo usuario a la tabla"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Actualizar el usuario en la tabla"""
        db.session.commit()

    def delete(self):
        """Eliminar el usuario de la tabla"""
        db.session.delete(self)
        db.session.commit()
