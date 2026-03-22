from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required  # proteger rutas
from .bd import db
from .productos import Producto
from form import ProductoForm, UsuarioForm  
from .usuarios import Usuario
import json, csv, os

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')

# ============================================================
# RUTAS PARA LIBROS (PROTEGIDAS)
# ============================================================

@inventario_bp.route('/')
@login_required  # <--- PROTEGIDA
def index():
    """Muestra todos los libros guardados en la BD"""
    productos = Producto.query.all()
    return render_template('libros.html', productos=productos)

@inventario_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required  # <--- PROTEGIDA
def nuevo():
    """Formulario para agregar un nuevo libro"""
    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            titulo=form.nombre.data,
            autor=form.autor.data,
            precio=form.precio.data,
            cantidad=form.cantidad.data
        )
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('inventario.index'))
    return render_template('libro_form.html', form=form, titulo='Nuevo Libro')

@inventario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required  # <--- PROTEGIDA
def editar_libro(id):
    """Editar un libro existente"""
    libro = Producto.query.get_or_404(id)
    form = ProductoForm(obj=libro)
    if form.validate_on_submit():
        libro.titulo = form.nombre.data
        libro.autor = form.autor.data
        libro.precio = form.precio.data
        libro.cantidad = form.cantidad.data
        db.session.commit()
        return redirect(url_for('inventario.index'))
    return render_template('libro_form.html', form=form, titulo='Editar Libro')

@inventario_bp.route('/eliminar/<int:id>')
@login_required  # <--- PROTEGIDA
def eliminar_libro(id):
    """Eliminar un libro"""
    libro = Producto.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('inventario.index'))

# ============================================================
# RUTAS PARA USUARIOS (PROTEGIDAS)
# ============================================================

@inventario_bp.route('/usuarios')
@login_required  # <--- PROTEGIDA
def listar_usuarios():
    """Muestra todos los usuarios"""
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@inventario_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required  # <--- PROTEGIDA
def nuevo_usuario():
    """Formulario para crear un nuevo usuario"""
    form = UsuarioForm()
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash
        usuario = Usuario(
            nombre=form.nombre.data,
            mail=form.mail.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('inventario.listar_usuarios'))
    return render_template('usuario_form.html', form=form, titulo='Nuevo Usuario')

@inventario_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required  # <--- PROTEGIDA
def editar_usuario(id):
    """Editar un usuario existente"""
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash
        usuario.nombre = form.nombre.data
        usuario.mail = form.mail.data
        if form.password.data:  
            usuario.password = generate_password_hash(form.password.data)
        db.session.commit()
        return redirect(url_for('inventario.listar_usuarios'))
    return render_template('usuario_form.html', form=form, titulo='Editar Usuario')

@inventario_bp.route('/usuarios/eliminar/<int:id>')
@login_required  # <--- PROTEGIDA
def eliminar_usuario(id):
    """Eliminar un usuario"""
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('inventario.listar_usuarios'))

# ============================================================
# RUTAS PARA ARCHIVOS (TXT, JSON, CSV) - PROTEGIDAS
# ============================================================

@inventario_bp.route('/guardar_txt', methods=['POST'])
@login_required  # <--- PROTEGIDA
def guardar_txt():
    """Guarda un dato en datos.txt"""
    dato = request.form.get('dato', '')
    ruta = os.path.join('inventario', 'data', 'datos.txt')
    with open(ruta, 'a') as f:
        f.write(dato + '\n')
    return 'Dato guardado en TXT'

@inventario_bp.route('/leer_txt')
@login_required  # <--- PROTEGIDA
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
@login_required  # <--- PROTEGIDA
def guardar_json():
    """Guarda un dato en datos.json"""
    dato = {
        'nombre': request.form.get('nombre', ''),
        'autor': request.form.get('autor', ''),
        'precio': request.form.get('precio', '0'),
        'cantidad': request.form.get('cantidad', '0')
    }
    ruta = os.path.join('inventario', 'data', 'datos.json')
    try:
        with open(ruta, 'r') as f:
            lista = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        lista = []
    lista.append(dato)
    with open(ruta, 'w') as f:
        json.dump(lista, f, indent=4)
    return 'Dato guardado en JSON'

@inventario_bp.route('/leer_json')
@login_required  # <--- PROTEGIDA
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
@login_required  # <--- PROTEGIDA
def guardar_csv():
    """Guarda un dato en datos.csv"""
    nombre = request.form.get('nombre', '')
    autor = request.form.get('autor', '')
    precio = request.form.get('precio', '0')
    cantidad = request.form.get('cantidad', '0')
    ruta = os.path.join('inventario', 'data', 'datos.csv')
    archivo_existe = os.path.isfile(ruta)
    with open(ruta, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(['nombre', 'autor', 'precio', 'cantidad'])
        writer.writerow([nombre, autor, precio, cantidad])
    return 'Dato guardado en CSV'

@inventario_bp.route('/leer_csv')
@login_required  # <--- PROTEGIDA
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