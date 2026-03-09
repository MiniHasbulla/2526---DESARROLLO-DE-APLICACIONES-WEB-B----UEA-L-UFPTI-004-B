from .bd import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100))
    precio = db.Column(db.Float, default=0.0)
    cantidad = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Producto {self.nombre}>'