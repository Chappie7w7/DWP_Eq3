from flask import Blueprint, render_template
from app.utils.decorators import requiere_modulo


roles_bp = Blueprint('roles', __name__, url_prefix='/roles')

@roles_bp.route('/')
@requiere_modulo('roles', 'admin')  # Requiere permiso de administrador para acceder
def index():
    return render_template('roles/index.jinja')
