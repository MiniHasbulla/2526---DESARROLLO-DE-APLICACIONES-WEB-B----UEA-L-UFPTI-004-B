from flask import Flask, render_template, redirect, url_for, flash, request
from Conexion.conexion import MySQLConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash




# Crear Flask
app = Flask(__name__)

# Clave formularios
app.config['SECRET_KEY'] = 'clave-secreta-para-formularios'

# conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = MySQLConfig.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# objeto que maneja
db = SQLAlchemy(app)

# ============================================================
# rutas de otras partes
# ============================================================

# ============================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ============================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Ruta a la que redirigir si no está autenticado
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."


# Importar el modelo Usuario (después de db para evitar circular imports)
from inventario.usuarios import Usuario

@login_manager.user_loader
def load_user(user_id):
    """Carga un usuario desde la base de datos por su ID"""
    return Usuario.query.get(int(user_id))


# app.py

from werkzeug.security import generate_password_hash, check_password_hash
from form import LoginForm, RegistroForm
from inventario.usuarios import Usuario

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar usuario por email
        usuario = Usuario.query.filter_by(mail=form.email.data).first()
        
        # Verificar credenciales
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        # Verificar si el email ya existe
        usuario_existente = Usuario.query.filter_by(mail=form.email.data).first()
        if usuario_existente:
            flash('Este correo ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        # Crear nuevo usuario con contraseña hasheada
        hashed_password = generate_password_hash(form.password.data)
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            mail=form.email.data,
            password=hashed_password
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html', form=form)

@app.route('/logout')
@login_required  # Solo usuarios logueados pueden cerrar sesión
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))


# Importar las rutas del inventario 
from inventario.inventario import inventario_bp
app.register_blueprint(inventario_bp)

# ============================================================
# rutas principales
# ============================================================

@app.route('/')
def index():
    """Página principal de la biblioteca"""
    return render_template('index.html')

# ============================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================

from form import LoginForm, RegistroForm  # Lo crearemos después

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(mail=form.email.data).first()
        
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(mail=form.email.data).first()
        if usuario_existente:
            flash('Este correo ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        hashed_password = generate_password_hash(form.password.data)
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            mail=form.email.data,
            password=hashed_password
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))


# ============================================================
# punto entrada
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)