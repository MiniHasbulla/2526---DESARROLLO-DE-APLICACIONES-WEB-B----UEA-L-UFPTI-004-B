"""
Programa principal
"""

from inventory import Inventario
import sys

def mostrar_menu_principal():
    """menú principal del sistema"""
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE INVENTARIO - LIBRERÍA".center(60))
    print("="*60)
    print("1. Agregar nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar productos por nombre")
    print("5. Mostrar todo el inventario")
    print("6. Ver estadísticas")
    print("7. Salir")
    print("="*60)

def obtener_entero_positivo(mensaje):
    """Solicita y valida un número entero positivo"""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Por favor, ingresa un número válido")

def obtener_float_positivo(mensaje):
    """Solicita un número decimal positivo"""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Por favor, digita un número válido")

def main():
    """Función principal del programa"""
    print("Iniciando Sistema de Gestión de Inventario...")
    
    # instancia del inventario
    inventario = Inventario()
    
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            # Agregar producto
            print("\n--- AGREGAR NUEVO PRODUCTO ---")
            nombre = input("Nombre del libro: ").strip()
            if not nombre:
                print("El nombre no puede estar vacío")
                continue
            
            cantidad = obtener_entero_positivo("Cantidad en stock: ")
            precio = obtener_float_positivo("Precio: $")
            autor = input("Autor (opcional): ").strip()
            genero = input("Género (opcional): ").strip()
            
            inventario.agregar_producto(nombre, cantidad, precio, autor, genero)
        
        elif opcion == "2":
            # Eliminar producto
            print("\n--- ELIMINAR PRODUCTO ---")
            try:
                id_producto = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)
            except ValueError:
                print("ID inválido")
        
        elif opcion == "3":
            # Actualizar producto
            print("\n--- ACTUALIZAR PRODUCTO ---")
            try:
                id_producto = int(input("ID del producto a actualizar: "))
                
                # producto actual
                if id_producto in inventario.productos:
                    print(f"\nProducto actual: {inventario.productos[id_producto]}")
                    print("\nDeje en blanco los campos que no desea actualizar")
                    
                    cantidad_str = input("Nueva cantidad: ").strip()
                    precio_str = input("Nuevo precio: $").strip()
                    autor = input("Nuevo autor: ").strip()
                    genero = input("Nuevo género: ").strip()
                    
                    cantidad = int(cantidad_str) if cantidad_str else None
                    precio = float(precio_str) if precio_str else None
                    
                    inventario.actualizar_producto(
                        id_producto, 
                        cantidad=cantidad, 
                        precio=precio,
                        autor=autor if autor else None,
                        genero=genero if genero else None
                    )
                else:
                    print(f"Producto con ID {id_producto} no encontrado")
            except ValueError:
                print("ID inválido")
        
        elif opcion == "4":
            # Buscar productos
            print("\n--- BUSCAR PRODUCTOS ---")
            nombre = input("Digita el nombre o parte del nombre a buscar: ").strip()
            
            if nombre:
                resultados = inventario.buscar_productos(nombre)
                
                if resultados:
                    print(f"\nSe encontraron {len(resultados)} producto(s):")
                    for producto in resultados:
                        print(f"   {producto}")
                else:
                    print("No se encontraron productos con ese nombre")
            else:
                print("Debes ingresar un término de búsqueda")
        
        elif opcion == "5":
            # Mostrar todo el inventario
            inventario.mostrar_todos()
        
        elif opcion == "6":
            # Mostrar solo estadísticas
            print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
            inventario.mostrar_estadisticas()
        
        elif opcion == "7":
            # Salir
            print("\n¡Gracias totales!")
            print("Datos guardados en la base de datos")
            sys.exit(0)
        
        else:
            print("Opción no válida. Por favor, selecciona 1-7")
        
        input("\n⏎ Presiona Enter para continuar...")

if __name__ == "__main__":
    main()