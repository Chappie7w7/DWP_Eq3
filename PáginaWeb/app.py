from flask import Flask, render_template, abort

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
#@app.route('/juegos')
#def juegos():
    #return render_template('josue/juegos.html')

# Ruta para vista proyectos
@app.route('/proyectos')
def proyectos():
    return render_template('josue/proyectos.html')

# Ruta para manejar errores 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.html'), 404

# Ruta para vista Yahir
@app.route('/yahir')
def yahir():
    return render_template('yahir/yahir.html')

# Ruta para vista materias
@app.route('/materia_yahir')
def materia_yahir():
    return render_template('yahir/materia.html')


# Ruta para vista integrantes
@app.route('/integrantes')
def integrantes():
    return render_template('yahir/integrantes.html')

# ruta matematicas

@app.route('/matematicas')
def matematicas():
    return render_template('yahir/matematicas.html')
# ruta ingles
@app.route('/ingles')
def ingles():
    return render_template('yahir/ingles.html')
# ruta desarrollo
@app.route('/desarrollo')
def desarrollo():
    return render_template('yahir/desarrollo.html')

# ruta juegos
@app.route('/juego')
def juego():
    return render_template('yahir/juegos.html')

# ruta free
@app.route('/free')
def free():
    return render_template('yahir/free.html')

# ruta aspa
@app.route('/aspa')
def aspa():
    return render_template('yahir/aspa.html')

# ruta aspa
@app.route('/fifa')
def fifa():
    return render_template('yahir/fifa.html')




# Ruta restringida que provoca un error 403
@app.route('/restri')
def restri():
    abort(403)  # Forzar un error 403

# Manejar errores 403 (Prohibido)
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('yahir/error_403.html'), 403


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
