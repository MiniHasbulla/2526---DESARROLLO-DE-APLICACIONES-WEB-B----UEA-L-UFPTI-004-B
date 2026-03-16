from flask import Blueprint, render_template, request, redirect, url_for
from .bd import db
from .productos import Producto
from form import ProductoForm
from form import UsuarioForm
from .usuarios import Usuario
import json, csv, os

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/')
def index():
    """Muestra todos los productos (libros) guardados en la BD"""
    productos = Producto.query.all()
    return render_template('libros.html', productos=productos)

@inventario_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Formulario para agregar un nuevo libro a la BD"""
    form = ProductoForm()
    if form.validate_on_submit():  # Si el formulario se envió y es válido
        # Crear un nuevo producto con los datos del formulario
        producto = Producto(
            titulo=form.nombre.data,
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

# ============================================================
# RUTAS PARA USUARIOS (CRUD)
# ============================================================

@inventario_bp.route('/usuarios')
def listar_usuarios():
    """Muestra todos los usuarios"""
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@inventario_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    """Formulario para crear un nuevo usuario"""
    form = UsuarioForm()
    if form.validate_on_submit():  # Si el formulario fue enviado y es válido
        # Crear un nuevo usuario con los datos del formulario
        usuario = Usuario(
            nombre=form.nombre.data,
            mail=form.mail.data,
            password=form.password.data
        )
        # Guardar en la base de datos
        db.session.add(usuario)
        db.session.commit()
        # Redirigir a la lista de usuarios
        return redirect(url_for('inventario.listar_usuarios'))
    # Si no se envió el formulario, mostrar el formulario vacío
    return render_template('usuario_form.html', form=form, titulo='Nuevo Usuario')

@inventario_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    """Editar un usuario existente"""
    # Buscar el usuario por su ID
    usuario = Usuario.query.get_or_404(id)
    # Crear un formulario con los datos del usuario
    form = UsuarioForm(obj=usuario)
    
    if form.validate_on_submit():  # Si enviaron el formulario editado
        # Actualizar los datos del usuario
        usuario.nombre = form.nombre.data
        usuario.mail = form.mail.data
        usuario.password = form.password.data
        # Guardar los cambios
        db.session.commit()
        return redirect(url_for('inventario.listar_usuarios'))
    
    return render_template('usuario_form.html', form=form, titulo='Editar Usuario')

@inventario_bp.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    """Eliminar un usuario"""
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('inventario.listar_usuarios'))

@inventario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    """Editar un libro existente"""
    from .productos import Producto
    from ..form import ProductoForm  # Asegúrate de que esta importación esté al inicio también
    
    libro = Producto.query.get_or_404(id)
    form = ProductoForm(obj=libro)  # Rellenamos el formulario con los datos del libro
    
    if form.validate_on_submit():
        libro.titulo = form.nombre.data
        libro.autor = form.autor.data
        libro.precio = form.precio.data
        libro.cantidad = form.cantidad.data
        db.session.commit()
        return redirect(url_for('inventario.index'))
    
    return render_template('libro_form.html', form=form, titulo='Editar Libro')

@inventario_bp.route('/eliminar/<int:id>')
def eliminar_libro(id):
    """Eliminar un libro"""
    from .productos import Producto
    libro = Producto.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('inventario.index'))