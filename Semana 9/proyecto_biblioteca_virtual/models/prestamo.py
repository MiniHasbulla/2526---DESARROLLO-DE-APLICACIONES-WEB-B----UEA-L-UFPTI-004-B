from app import db
from datetime import datetime

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'))
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime, nullable=True)

    # Relaciones
    usuario = db.relationship('Usuario', backref='prestamos')
    libro = db.relationship('Producto', backref='prestamos')  # Producto es el modelo de libro