"""
Módulo clase Producto para Libreria
tupla atributos inmutables
"""

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio, autor="", genero=""):
        """
        Constructor de la clase Producto.
        tupla
        """
        self._datos = (id_producto, nombre, cantidad, precio, autor, genero)
    
    # Getters usando propiedades
    @property
    def id(self):
        return self._datos[0]
    
    @property
    def nombre(self):
        return self._datos[1]
    
    @property
    def cantidad(self):
        return self._datos[2]
    
    @property
    def precio(self):
        return self._datos[3]
    
    @property
    def autor(self):
        return self._datos[4]
    
    @property
    def genero(self):
        return self._datos[5]
    
    # Setters (crean una nueva tupla - inmutabilidad)
    def set_cantidad(self, nueva_cantidad):
        """Actualiza la cantidad"""
        self._datos = (self.id, self.nombre, nueva_cantidad, self.precio, self.autor, self.genero)
    
    def set_precio(self, nuevo_precio):
        """Actualiza el precio"""
        self._datos = (self.id, self.nombre, self.cantidad, nuevo_precio, self.autor, self.genero)
    
    def to_dict(self):
        """producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'autor': self.autor,
            'genero': self.genero
        }
    
    def __str__(self):
        """string del producto"""
        return f"ID: {self.id} | {self.nombre} | Cant: {self.cantidad} | Precio: ${self.precio:.2f} | Autor: {self.autor} | Género: {self.genero}"