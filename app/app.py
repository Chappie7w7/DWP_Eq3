from flask import Flask, render_template

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

# Ruta para manejar errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.html'), 404


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
