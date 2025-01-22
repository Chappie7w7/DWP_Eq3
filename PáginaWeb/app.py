from flask import Flask, render_template, request, abort

app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta de inicio
@app.route('/inicio')
def inicio():
    return render_template('home.html')

# Ruta para vista Josué
@app.route('/josue')
def josue():
    return render_template('josue/josue.html')

# Ruta para vista materias
@app.route('/materias')
def materias():
    return render_template('josue/materias.html')

# Ruta para vista juegos
@app.route('/juegos')
def juegos():
    return render_template('josue/juegos.html')

# Ruta para vista proyectos
@app.route('/proyectos')
def proyectos():
    return render_template('josue/proyectos.html')

# Ruta para manejar errores 400
@app.errorhandler(400)
def handle_bad_request(e):
    return render_template('josue/error.html'), 400

# Ruta para generar error 400
@app.route('/suma')
def suma():
    # Verifica que los parámetros estén presentes
    try:
        a = int(request.args['a'])
        b = int(request.args['b'])
        return f"El resultado es: {a + b}"
    except KeyError:
        # Genera un error 400 si falta un parámetro
        abort(400)
    except ValueError:
        # Genera un error 400 si los parámetros no son válidos
        abort(400)

# Ruta para manejar errores 404
#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('josue/error.html'), 404


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
