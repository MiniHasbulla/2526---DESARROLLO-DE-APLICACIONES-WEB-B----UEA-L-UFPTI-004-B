from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libro/<titulo>')
def libro(titulo):
    libros_disponibles = {
        'cien años de soledad': 'Gabriel García Márquez',
        '1984': 'George Orwell',
        'don quijote': 'Miguel de Cervantes',
        'rayuela': 'Julio Cortázar'
    }
    
    titulo_lower = titulo.lower()
    if titulo_lower in libros_disponibles:
        autor = libros_disponibles[titulo_lower]
        mensaje = f"Libro: '{titulo.title()}' de {autor} – Disponible en la biblioteca"
        disponible = True
    else:
        mensaje = f"Libro: '{titulo}' – No disponible en nuestro catálogo"
        disponible = False
    
    return render_template('libro.html', titulo=titulo, mensaje=mensaje, disponible=disponible)

@app.route('/categoria/<nombre_categoria>')
def categoria(nombre_categoria):
    categorias = {
        'novela': ['Cien años de soledad', '1984', 'Rayuela'],
        'clasicos': ['Don Quijote', 'La Iliada', 'La Odisea'],
        'poesia': ['Veinte poemas de amor', 'Antología poética']
    }
    
    if nombre_categoria.lower() in categorias:
        libros = categorias[nombre_categoria.lower()]
        return render_template('categoria.html', categoria=nombre_categoria, libros=libros)
    else:
        return f"Categoría '{nombre_categoria}' no encontrada", 404

if __name__ == '__main__':
    print(" Iniciando servidor Flask...")
    app.run(debug=True, host='127.0.0.1', port=5000)