from flask import Blueprint, render_template
from app.utils.decorators import requiere_modulo


permisos_bp = Blueprint('permisos', __name__, url_prefix='/permisos')

@permisos_bp.route('/')
@requiere_modulo('permisos', 'lectura')  # Requiere permiso de lectura para acceder
def index():
    return render_template('permisos/index.jinja')
