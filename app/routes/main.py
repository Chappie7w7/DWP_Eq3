from flask import Blueprint, render_template, session, abort
from functools import wraps

main_bp = Blueprint('main', __name__)

# Función decoradora para restringir acceso a módulos según los permisos
def requiere_modulo(modulo_nombre):
    """Verifica si el usuario tiene acceso al módulo"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'modulos' not in session or modulo_nombre not in session['modulos']:
                abort(403)  # Retorna error 403 si el usuario no tiene permiso
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Ruta para el login
@main_bp.route('/')
def home():
    return render_template('auth/login.jinja')

# Ruta para el inicio (dashboard)
@main_bp.route('/inicio')
def inicio():
    return render_template('dashboard/home.jinja')

# 🔹 Materias (Protegido)
@main_bp.route('/materias')
@requiere_modulo('materias')
def materias():
    return render_template('alexis/materias/materias.jinja')

@main_bp.route('/materias/ingles')
@requiere_modulo('materias')
def ingles():
    return render_template('alexis/materias/ingles.jinja')

@main_bp.route('/materias/matematicas')
@requiere_modulo('materias')
def matematicas():
    return render_template('alexis/materias/matematicas.jinja')

# 🔹 Juegos (Protegido)
@main_bp.route('/juegos')
@requiere_modulo('juegos')
def juegos():
    return render_template('alexis/juegos/juegos.jinja')

@main_bp.route('/juegos/clash_royale')
@requiere_modulo('juegos')
def clash_royale():
    return render_template('alexis/juegos/clash_royale.jinja')

@main_bp.route('/juegos/gta_v')
@requiere_modulo('juegos')
def gta_v():
    return render_template('alexis/juegos/gta_v.jinja')

# 🔹 Proyectos (Protegido)
@main_bp.route('/proyectos')
@requiere_modulo('proyectos')
def proyectos():
    return render_template('alexis/proyectos/proyectos.jinja')

@main_bp.route('/proyectos/prototipos')
@requiere_modulo('proyectos')
def prototipos():
    return render_template('alexis/proyectos/prototipos.jinja')

@main_bp.route('/proyectos/app_movil')
@requiere_modulo('proyectos')
def app_movil():
    return render_template('alexis/proyectos/app_movil.jinja')

# Ruta para Josué (Sin Restricción)
@main_bp.route('/josue')
def josue():
    return render_template('josue/josue.jinja')

# Error 404
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.jinja'), 404
