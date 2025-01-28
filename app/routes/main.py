from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

# Ruta para el login
@main_bp.route('/')
def home():
    return render_template('auth/login.jinja')

# Ruta para el inicio (dashboard)
@main_bp.route('/inicio')
def inicio():
    return render_template('dashboard/home.jinja')

# Ruta para Josué
@main_bp.route('/josue')
def josue():
    return render_template('josue/josue.jinja')



@main_bp.route('/juegos')
def juegos():
    return render_template('alexis/juegos/juegos.jinja')


@main_bp.route('/juegos/clash_royale')
def clash_royale():
    return render_template('alexis/juegos/clash_royale.jinja')

@main_bp.route('/juegos/gta_v')
def gta_v():
    return render_template('alexis/juegos/gta_v.jinja')





@main_bp.route('/materias')
def materias():
    return render_template('alexis/materias/materias.jinja')


@main_bp.route('/materias/ingles')
def ingles():
    return render_template('alexis/materias/ingles.jinja')

@main_bp.route('/materias/matematicas')
def matematicas():
    return render_template('alexis/materias/matematicas.jinja')




@main_bp.route('/proyectos')
def proyectos():
    return render_template('alexis/proyectos/proyectos.jinja')


@main_bp.route('/proyectos/prototipos')
def prototipos():
    return render_template('alexis/proyectos/prototipos.jinja')

@main_bp.route('/proyectos/app_movil')
def app_movil():
    return render_template('alexis/proyectos/app_movil.jinja')




# Error 404
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.jinja'), 404


