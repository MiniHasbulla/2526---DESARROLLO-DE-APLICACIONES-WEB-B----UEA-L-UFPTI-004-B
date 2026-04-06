# inventario/usuarios.py
from .bd import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Flask-Login necesita un método get_id que devuelva el identificador
    def get_id(self):
        return str(self.id_usuario)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'