from models.libro import Producto
from app import db

class LibroService:
    @staticmethod
    def obtener_todos():
        return Producto.query.all()

    @staticmethod
    def obtener_por_id(id):
        return Producto.query.get_or_404(id)

    @staticmethod
    def crear(titulo, autor, precio, cantidad):
        nuevo = Producto(titulo=titulo, autor=autor, precio=precio, cantidad=cantidad)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

    @staticmethod
    def actualizar(id, titulo, autor, precio, cantidad):
        libro = Producto.query.get_or_404(id)
        libro.titulo = titulo
        libro.autor = autor
        libro.precio = precio
        libro.cantidad = cantidad
        db.session.commit()
        return libro

    @staticmethod
    def eliminar(id):
        libro = Producto.query.get_or_404(id)
        db.session.delete(libro)
        db.session.commit()