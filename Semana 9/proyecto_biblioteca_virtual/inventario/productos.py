from .bd import db

class Producto(db.Model):
    __tablename__ = 'libros'  # nombre a "libros"
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)  # Antes se llamaba "nombre"
    autor = db.Column(db.String(100))
    precio = db.Column(db.Float, default=0.0)
    cantidad = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Libro {self.titulo}>'