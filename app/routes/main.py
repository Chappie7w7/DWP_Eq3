from flask import Blueprint, render_template, session, abort
from app.models.md_seccion import Seccion
from app.models.md_usuario_modulo import UsuarioModulo

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Página principal del sistema.
    """
    return render_template('auth/login.jinja')

@main_bp.route('/inicio')
def inicio():
    """
    Página de inicio (dashboard).
    """
    return render_template('dashboard/home.jinja')

@main_bp.route('/<modulo>')
def mostrar_modulo(modulo):
    """
    Muestra todas las secciones de un módulo específico para el usuario actual.
    """
    usuario_id = session.get('usuario_id')

    # Validar si el usuario tiene acceso al módulo
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).filter(
        Seccion.categoria == modulo,
        UsuarioModulo.usuario_id == usuario_id
    ).all()

    if not secciones:
        abort(404)  # Si no hay secciones o el módulo no existe, muestra error 404

    # Construir breadcrumb
    breadcrumb = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': modulo.capitalize(), 'url': None},
    ]

    return render_template(
        'dinamico.jinja',
        titulo=modulo.capitalize(),
        secciones=secciones,
        breadcrumb=breadcrumb
    )

@main_bp.route('/<modulo>/<seccion>')
def mostrar_seccion(modulo, seccion):
    """
    Muestra una sección específica dentro de un módulo.
    """
    usuario_id = session.get('usuario_id')

    # Normalizar el nombre de la sección para manejar guiones bajos en la URL
    seccion_normalizada = seccion.replace('_', ' ')

    # Validar si la sección pertenece al usuario actual
    seccion_data = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).filter(
        Seccion.categoria == modulo,
        Seccion.nombre == seccion_normalizada,
        UsuarioModulo.usuario_id == usuario_id
    ).first()

    if not seccion_data:
        abort(404)

    # Construir breadcrumb
    breadcrumb = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': modulo.capitalize(), 'url': f'/{modulo}'},
        {'name': seccion_data.nombre, 'url': None},  # Último nivel
    ]

    return render_template(
        'dinamico_seccion.jinja',
        titulo=seccion_data.nombre,
        seccion=seccion_data,
        breadcrumb=breadcrumb
    )
