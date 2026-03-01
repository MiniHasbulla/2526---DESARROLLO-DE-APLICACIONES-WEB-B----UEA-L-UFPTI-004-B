"""
Módulo Inventario utilizando Python

"""

from models import Producto
from database import DatabaseManager
from collections import defaultdict

class Inventario:
    def __init__(self):
        """Inicializa el inventario"""
        self.db = DatabaseManager()
        self.productos = {}  # Diccionario: ID -> Producto
        self.cargar_desde_db()
    
    def cargar_desde_db(self):
        """Carga los productos"""
        productos_db = self.db.cargar_productos()
        self.productos = {p.id: p for p in productos_db}  # Diccionario por comprensión
        print(f"Cargados {len(self.productos)} productos desde la base de datos")
    
    def agregar_producto(self, nombre, cantidad, precio, autor="", genero=""):
        """Añade un producto"""
        # Crear objeto Producto (sin ID, se generará en la BD)
        producto = Producto(None, nombre, cantidad, precio, autor, genero)
        
        # Guardar en BD y obtener ID
        producto_id = self.db.guardar_producto(producto)
        
        # Actualizar el objeto con el ID generado
        producto._datos = (producto_id, nombre, cantidad, precio, autor, genero)
        
        # Añadir al diccionario
        self.productos[producto_id] = producto
        print(f"Producto '{nombre}' agregado con ID {producto_id}")
        return producto_id
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto por ID"""
        if producto_id in self.productos:
            nombre = self.productos[producto_id].nombre
            if self.db.eliminar_producto(producto_id):
                del self.productos[producto_id]
                print(f"Producto '{nombre}' eliminado")
                return True
        else:
            print(f"Producto con ID {producto_id} no encontrado")
        return False
    
    def actualizar_producto(self, producto_id, cantidad=None, precio=None, autor=None, genero=None):
        """Actualiza cantidad o precio"""
        if producto_id in self.productos:
            producto = self.productos[producto_id]
            
            # Actualizar atributos si se proporcionan nuevos valores
            if cantidad is not None:
                producto.set_cantidad(cantidad)
            if precio is not None:
                producto.set_precio(precio)
            if autor is not None:
                # Para actualizar autor, necesitamos crear nueva tupla
                producto._datos = (producto.id, producto.nombre, producto.cantidad, 
                                 producto.precio, autor, producto.genero)
            if genero is not None:
                producto._datos = (producto.id, producto.nombre, producto.cantidad, 
                                 producto.precio, producto.autor, genero)
            
            # Guardar en base de datos
            if self.db.actualizar_producto(producto):
                print(f"Producto ID {producto_id} actualizado")
                return True
        else:
            print(f"Producto con ID {producto_id} no encontrado")
        return False
    
    def buscar_productos(self, nombre):
        """Busca productos por nombre"""
        resultados = self.db.buscar_por_nombre(nombre)
        
        # Actualizar el diccionario
        for prod in resultados:
            self.productos[prod.id] = prod
        
        return resultados
    
    def mostrar_todos(self):
        """Muestra todos los productos"""
        if not self.productos:
            print("Inventario vacío")
            return
        
        print("\n" + "="*80)
        print("INVENTARIO COMPLETO".center(80))
        print("="*80)
        
        # Ordenar productos
        productos_ordenados = sorted(self.productos.values(), key=lambda p: p.nombre)
        
        for producto in productos_ordenados:
            print(producto)
        
        # Mostrar estadísticas
        self.mostrar_estadisticas()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas"""
        print("-"*80)
        
        # Usar conjunto
        generos = {p.genero for p in self.productos.values() if p.genero}
        
        # Usar defaultdict
        conteo_generos = defaultdict(int)
        valor_inventario = 0
        
        for producto in self.productos.values():
            if producto.genero:
                conteo_generos[producto.genero] += 1
            valor_inventario += producto.cantidad * producto.precio
        
        print(f"Total de productos: {len(self.productos)}")
        print(f"Géneros disponibles: {len(generos)}")
        print(f"Valor total del inventario: ${valor_inventario:.2f}")
        
        if conteo_generos:
            print("Productos por género:")
            for genero, cantidad in conteo_generos.items():
                print(f"   - {genero}: {cantidad} título(s)")