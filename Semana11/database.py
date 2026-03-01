"""
Módulo para manejar conexión y operaciones con SQLite
"""

import sqlite3
from models import Producto

class DatabaseManager:
    def __init__(self, db_name="libreria.db"):
        """Inicializa la conexión"""
        self.db_name = db_name
        self.crear_tablas()
    
    def get_connection(self):
        """conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def crear_tablas(self):
        """Crea las tablas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos (libros)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                autor TEXT,
                genero TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de clientes (para futuras funcionalidades)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de ventas (para futuras funcionalidades)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                total REAL,
                fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Tablas creadas/verificadas")
    
    def guardar_producto(self, producto):
        """Guarda un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO productos (nombre, cantidad, precio, autor, genero)
            VALUES (?, ?, ?, ?, ?)
        ''', (producto.nombre, producto.cantidad, producto.precio, producto.autor, producto.genero))
        
        conn.commit()
        producto_id = cursor.lastrowid
        conn.close()
        return producto_id
    
    def cargar_productos(self):
        """Carga los productos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, nombre, cantidad, precio, autor, genero FROM productos')
        productos_db = cursor.fetchall()
        conn.close()
        
        # Convertir a objetos Producto usando una lista de comprensión
        productos = []
        for prod in productos_db:
            producto = Producto(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5])
            productos.append(producto)
        
        return productos
    
    def actualizar_producto(self, producto):
        """Actualiza un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE productos 
            SET cantidad = ?, precio = ?, autor = ?, genero = ?
            WHERE id = ?
        ''', (producto.cantidad, producto.precio, producto.autor, producto.genero, producto.id))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def eliminar_producto(self, producto_id):
        """Elimina un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (búsqueda parcial)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, cantidad, precio, autor, genero 
            FROM productos 
            WHERE nombre LIKE ?
        ''', (f'%{nombre}%',))
        
        productos_db = cursor.fetchall()
        conn.close()
        
        productos = []
        for prod in productos_db:
            producto = Producto(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5])
            productos.append(producto)
        
        return productos