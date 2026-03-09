from flask import Blueprint, render_template, request, redirect, url_for
from .bd import db
from .productos import Producto
from ..form import ProductoForm
import json, csv, os

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/')
def index():
    """Muestra todos los productos (libros) guardados en la BD"""
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@inventario_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Formulario para agregar un nuevo libro a la BD"""
    form = ProductoForm()
    if form.validate_on_submit():  # Si el formulario se envió y es válido
        # Crear un nuevo producto con los datos del formulario
        producto = Producto(
            nombre=form.nombre.data,
            autor=form.autor.data,
            precio=form.precio.data,
            cantidad=form.cantidad.data
        )
        db.session.add(producto)   # Agregar a la BD
        db.session.commit()        # Guardar cambios
        return redirect(url_for('inventario.index'))  # Volver a la lista
    return render_template('producto_form.html', form=form, titulo='Nuevo Libro')


@inventario_bp.route('/guardar_txt', methods=['POST'])
def guardar_txt():
    """Guarda un dato en datos.txt (desde un formulario simple)"""
    dato = request.form.get('dato', '')
    ruta = os.path.join('inventario', 'data', 'datos.txt')
    with open(ruta, 'a') as f:
        f.write(dato + '\n')
    return 'Dato guardado en TXT'

@inventario_bp.route('/leer_txt')
def leer_txt():
    """Lee y muestra todo el contenido de datos.txt"""
    ruta = os.path.join('inventario', 'data', 'datos.txt')
    try:
        with open(ruta, 'r') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        lineas = []
    return render_template('datos.html', datos=lineas, formato='TXT')


@inventario_bp.route('/guardar_json', methods=['POST'])
def guardar_json():
    """Guarda un dato en datos.json (en formato JSON)"""
    # datos del formulario 
    dato = {
        'nombre': request.form.get('nombre', ''),
        'autor': request.form.get('autor', ''),
        'precio': request.form.get('precio', '0'),
        'cantidad': request.form.get('cantidad', '0')
    }
    ruta = os.path.join('inventario', 'data', 'datos.json')
    # Leer el archivo existente o crear una lista nueva
    try:
        with open(ruta, 'r') as f:
            lista = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        lista = []
    lista.append(dato)
    # Guardar la lista actualizada
    with open(ruta, 'w') as f:
        json.dump(lista, f, indent=4)
    return 'Dato guardado en JSON'

@inventario_bp.route('/leer_json')
def leer_json():
    """Lee y muestra todos los datos de datos.json"""
    ruta = os.path.join('inventario', 'data', 'datos.json')
    try:
        with open(ruta, 'r') as f:
            datos = json.load(f)
    except FileNotFoundError:
        datos = []
    return render_template('datos.html', datos=datos, formato='JSON')


@inventario_bp.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    """Guarda un dato en datos.csv"""
    nombre = request.form.get('nombre', '')
    autor = request.form.get('autor', '')
    precio = request.form.get('precio', '0')
    cantidad = request.form.get('cantidad', '0')
    ruta = os.path.join('inventario', 'data', 'datos.csv')
    # Verificar si el archivo ya existe para escribir cabecera solo una vez
    archivo_existe = os.path.isfile(ruta)
    with open(ruta, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(['nombre', 'autor', 'precio', 'cantidad'])
        writer.writerow([nombre, autor, precio, cantidad])
    return 'Dato guardado en CSV'

@inventario_bp.route('/leer_csv')
def leer_csv():
    """Lee y muestra todos los datos de datos.csv"""
    ruta = os.path.join('inventario', 'data', 'datos.csv')
    datos = []
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for fila in reader:
                datos.append(fila)
    except FileNotFoundError:
        pass
    return render_template('datos.html', datos=datos, formato='CSV')