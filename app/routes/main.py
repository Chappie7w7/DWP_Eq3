from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

# Ruta principal
@main_bp.route('/')
def home():
    return render_template('dashboard/index.jinja')

# Ruta de inicio
@main_bp.route('/inicio')
def inicio():
    return render_template('home.jinja')

# Ruta para vista Josué
@main_bp.route('/josue')
def josue():
    return render_template('josue/josue.html')

# Ruta para vista materias
@main_bp.route('/materias')
def materias():
    return render_template('josue/materias.html')

# Ruta para vista juegos
@main_bp.route('/juegos')
def juegos():
    return render_template('josue/juegos.html')

# Ruta para vista proyectos
@main_bp.route('/proyectos')
def proyectos():
    return render_template('josue/proyectos.html')

# Ruta para manejar errores 404
@main_bp.errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.html'), 404
