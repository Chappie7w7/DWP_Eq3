from flask import Blueprint, render_template, abort
from app.models.md_seccion import Seccion

secciones_bp = Blueprint('secciones', __name__, url_prefix='/secciones')

@secciones_bp.route('/<modulo>/<archivo>')
def mostrar_contenido(modulo, archivo):
    """
    Carga dinámicamente el contenido según el módulo y archivo especificado.
    """
    # Buscar la sección directamente en la base de datos
    seccion_data = Seccion.query.filter_by(categoria=modulo, nombre=archivo).first()
    if not seccion_data:
        abort(404)  # Error si no existe

    # Generar breadcrumb dinámico
    breadcrumb = [
        {"name": "Inicio", "url": "/inicio"},
        {"name": modulo.capitalize(), "url": f"/secciones/{modulo}"},
        {"name": seccion_data.nombre, "url": None},  # La última entrada no necesita URL
    ]
    
    return render_template('dinamico_seccion.jinja', breadcrumb=breadcrumb, titulo=seccion_data.nombre, seccion=seccion_data)
