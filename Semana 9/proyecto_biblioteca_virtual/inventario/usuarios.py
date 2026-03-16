from flask_sqlalchemy import SQLAlchemy
from .bd import db  # Importa base de datos

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en MySQL
    
    # Columnas de la tabla
    id_usuario = db.Column(db.Integer, primary_key=True)  # Número
    nombre = db.Column(db.String(100), nullable=False)    # Nombre 
    mail = db.Column(db.String(100), unique=True, nullable=False)  # Email
    password = db.Column(db.String(255), nullable=False)  # Contraseña
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'