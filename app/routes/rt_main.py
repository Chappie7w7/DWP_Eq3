from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, abort, url_for
from sqlalchemy import func
from app.models.md_modulo import Modulo
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
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,  # Usar nombre_modulo del modelo Modulo
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
    seccion_data = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,  # Cambiado
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

@main_bp.route('/buscar/<modulo>', methods=['GET'])
def buscar(modulo):
    usuario_id = session.get('usuario_id')
    query = request.args.get('simple_query', '').strip()

    if not query:
        flash('Por favor, ingresa un término de búsqueda.', 'warning')
        return redirect(url_for('main.mostrar_modulo', modulo=modulo))

    # Filtrar las secciones del módulo basado en el término de búsqueda (nombre o descripción)
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%'))  # Busca en nombre y descripción
    ).all()

    # Construir breadcrumb
    breadcrumb = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': modulo.capitalize(), 'url': f'/{modulo}'},
        {'name': f'Resultados de búsqueda: "{query}"', 'url': None},
    ]

    return render_template(
        'dinamico.jinja',
        titulo=modulo.capitalize(),
        secciones=secciones,
        breadcrumb=breadcrumb
    )


@main_bp.route('/buscar-avanzada', methods=['GET'])
def buscar_avanzada():
    """
    Realiza una búsqueda avanzada en todas las categorías y módulos.
    """
    usuario_id = session.get('usuario_id')
    query = request.args.get('advanced_query', '').strip()  # Cambiado de 'query' a 'advanced_query'
    categoria = request.args.get('categoria', '').strip()

    if not query:
        flash('Por favor, ingresa un término de búsqueda.', 'warning')
        return redirect(url_for('main.inicio'))

    # Filtrar secciones según el término de búsqueda y categoría
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%')),
        (Seccion.categoria == categoria if categoria else True)
    ).all()

    # Construir breadcrumb
    breadcrumb = [
        {'name': 'Inicio', 'url': '/inicio'},
        {'name': f'Resultados de búsqueda: "{query}"', 'url': None},
    ]

    return render_template(
        'resultados.jinja',
        titulo='Resultados de búsqueda',
        secciones=secciones,
        breadcrumb=breadcrumb
    )

@main_bp.route('/api/secciones/<modulo>', methods=['GET'])
def api_obtener_secciones(modulo):
    """
    API para obtener todas las secciones de un módulo en formato JSON.
    """
    usuario_id = session.get('usuario_id')

    # Buscar todas las secciones dentro del módulo
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id
    ).all()

    secciones_json = [
        {"nombre": s.nombre, "descripcion": s.descripcion, "url": s.url}
        for s in secciones
    ]

    return jsonify(secciones_json)

@main_bp.route('/api/seccion/<modulo>/<seccion>', methods=['GET'])
def api_obtener_seccion(modulo, seccion):
    """
    API para obtener una sección específica dentro de un módulo en formato JSON.
    """
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 403

    # Reemplazar _ por espacios para hacer match con la base de datos
    seccion_formateada = seccion.replace("_", " ")

    seccion_obj = Seccion.query.join(Modulo, Modulo.id == Seccion.modulo_id).filter(
        func.lower(Modulo.nombre_modulo) == modulo.lower(),
        func.lower(Seccion.nombre) == seccion_formateada.lower(),
        UsuarioModulo.usuario_id == usuario_id
    ).first()

    if not seccion_obj:
        return jsonify({"error": "Sección no encontrada"}), 404

    return jsonify({
        "nombre": seccion_obj.nombre,
        "descripcion": seccion_obj.descripcion,
        "url": seccion_obj.url
    })

@main_bp.route('/api/buscar/<modulo>', methods=['GET'])
def api_buscar(modulo):
    """
    API para buscar secciones dentro de un módulo en formato JSON.
    """
    usuario_id = session.get('usuario_id')
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])  # Devuelve un array vacío si no hay búsqueda

    # Filtrar las secciones del módulo basado en el término de búsqueda
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%'))  # Busca en nombre y descripción
    ).all()

    secciones_json = [
        {"nombre": s.nombre, "descripcion": s.descripcion, "url": url_for('main.mostrar_seccion', modulo=modulo, seccion=s.nombre.replace(" ", "_"))}
        for s in secciones
    ]

    return jsonify(secciones_json)

@main_bp.route('/api/buscar-avanzada', methods=['GET'])
def api_buscar_avanzada():
    """
    API para realizar una búsqueda avanzada en todas las categorías y módulos.
    """
    usuario_id = session.get('usuario_id')
    query = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()

    if not query:
        return jsonify([])  # Devuelve un array vacío si no hay búsqueda

    # Filtrar secciones según el término de búsqueda y categoría
    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%')),
        (Seccion.categoria == categoria if categoria else True)  # Si hay categoría, filtrar por ella
    ).all()

    secciones_json = [
        {
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "url": url_for('main.mostrar_seccion', modulo=s.modulo.nombre_modulo, seccion=s.nombre.replace(" ", "_"))
        }
        for s in secciones
    ]

    return jsonify(secciones_json)
