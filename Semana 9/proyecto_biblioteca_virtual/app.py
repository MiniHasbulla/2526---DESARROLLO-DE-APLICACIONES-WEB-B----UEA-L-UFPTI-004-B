from flask import Flask, render_template
from Conexion.conexion import MySQLConfig
from flask_sqlalchemy import SQLAlchemy

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
# punto entrada
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)