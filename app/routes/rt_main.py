from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, abort, url_for
from flask_login import login_required
from sqlalchemy import func
from app.models.md_modulo import Modulo
from app.models.md_seccion import Seccion
from app.models.md_usuario import Usuario
from app.models.md_usuario_modulo import UsuarioModulo
from app.utils.decorators import token_required
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Página principal del sistema.
    """
    return render_template('auth/login.jinja')

@main_bp.route('/inicio')
@login_required
@token_required
def inicio():
    current_user = Usuario.query.get(session.get("usuario_id"))
    permisos = session.get("permisos", [])

    modulos_visibles = []

    if 'ver_materias' in permisos or 'materias_agregar' in permisos:
        modulos_visibles.append('materias')
    if 'ver_juegos' in permisos or 'juegos_agregar' in permisos:
        modulos_visibles.append('juegos')
    if 'ver_proyectos' in permisos or 'proyectos_agregar' in permisos:
        modulos_visibles.append('proyectos')

    return render_template('dashboard/home.jinja', modulos=modulos_visibles)


@main_bp.route('/<modulo>')
@login_required
@token_required
def mostrar_modulo(modulo):
    current_user = Usuario.query.get(session.get("usuario_id"))

    permisos = session.get("permisos", [])
    permiso_necesario = f"ver_{modulo.lower()}"

    if permiso_necesario not in permisos:
        flash("No tienes permiso para acceder a este módulo.", "danger")
        return redirect(url_for("main.inicio"))

    usuario_id = session.get('usuario_id')

    # Solo secciones del módulo asignado al usuario Y creadas por él
    secciones = Seccion.query.join(Modulo).join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id,
        Seccion.usuario_id == usuario_id
    ).all()


    if not secciones:
        permiso_agregar = f"{modulo.lower()}_crear"
        if permiso_agregar not in permisos:
            abort(404)

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
@login_required
@token_required
def mostrar_seccion(modulo, seccion):
    current_user = Usuario.query.get(session.get("usuario_id"))
    """
    Muestra una sección específica dentro de un módulo.
    """
    
    # Verificar permiso de ver el módulo
    permisos = session.get("permisos", [])
    permiso_necesario = f"ver_{modulo.lower()}"

    if permiso_necesario not in permisos:
        flash("No tienes permiso para acceder a esta sección.", "danger")
        return redirect(url_for("main.inicio"))
    
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
        breadcrumb=breadcrumb,
        modulo=modulo
    )

@main_bp.route('/buscar/<modulo>', methods=['GET'])
def buscar(modulo):
    usuario_id = session.get('usuario_id')
    query = request.args.get('simple_query', '').strip()

    if not query:
        flash('Por favor, ingresa un término de búsqueda.', 'warning')
        return redirect(url_for('main.mostrar_modulo', modulo=modulo))

    # Obtener permisos
    permisos = session.get('permisos', [])
    modulo_lower = modulo.lower()

    # Buscar secciones
    secciones_raw = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%'))
    ).all()

    # Enriquecer con permisos
    secciones = []
    for s in secciones_raw:
        secciones.append({
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "url": url_for('main.mostrar_seccion', modulo=modulo, seccion=s.nombre.replace(" ", "_")),
            "permisos": {
                "actualizar": f"{modulo_lower}_actualizar" in permisos,
                "eliminar": f"{modulo_lower}_eliminar" in permisos
            }
        })

    # Breadcrumb
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
    usuario_id = session.get('usuario_id')
    query = request.args.get('advanced_query', '').strip()
    categoria = request.args.get('categoria', '').strip()

    if not query:
        flash('Por favor, ingresa un término de búsqueda.', 'warning')
        return redirect(url_for('main.inicio'))

    permisos = session.get('permisos', [])

    # ✅ Validar permiso de visualización por categoría
    if categoria:
        permiso_modulo = f"ver_{categoria.lower()}"
        if permiso_modulo not in permisos:
            flash("No tienes permiso para acceder a esta categoría.", "danger")
            return redirect(url_for("main.inicio"))

    # Buscar secciones
    secciones_raw = Seccion.query.join(Modulo, Modulo.id == Seccion.modulo_id).join(
        UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id
    ).filter(
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%')),
        (Seccion.categoria == categoria if categoria else True)
    ).all()

    # Enriquecer cada sección con permisos
    secciones = []
    for s in secciones_raw:
        modulo_lower = s.modulo.nombre_modulo.lower()
        secciones.append({
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "url": url_for('main.mostrar_seccion', modulo=s.modulo.nombre_modulo, seccion=s.nombre.replace(" ", "_")),
            "modulo": modulo_lower,
            "permisos": {
                "actualizar": f"{modulo_lower}_actualizar" in permisos,
                "eliminar": f"{modulo_lower}_eliminar" in permisos
            }
        })

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
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 403
    

    #Asegurar que los permisos estén en sesión
    print("📌 Permisos de sesión disponibles en la API:", session.get('permisos'))

    permisos = session.get('permisos', [])
    if not isinstance(permisos, list):
        permisos = []

    offset = request.args.get('offset', default=0, type=int)
    limit = 6

    secciones = Seccion.query.join(UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id).join(
        Modulo, Modulo.id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id
    ).offset(offset).limit(limit).all()

    modulo_lower = modulo.lower()

    secciones_json = [
    {
        "id": s.id,
        "nombre": s.nombre,
        "descripcion": s.descripcion,
        "url": s.url,
        "permisos": {
            "actualizar": f"{modulo_lower}_actualizar" in permisos if permisos else False,
            "eliminar": f"{modulo_lower}_eliminar" in permisos if permisos else False,
            #"ver": f"{modulo_lower}_consultar" in permisos if permisos else False
        }
    }
    for s in secciones
    ]

    print("🔄 Datos enviados al frontend:")
    for s in secciones_json:
        print(s)


    return jsonify({
        "secciones": secciones_json,
        "has_more": len(secciones) == limit
    })


@main_bp.route('/api/seccion/<modulo>/<seccion>', methods=['GET'])
def api_obtener_seccion(modulo, seccion):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({"error": "Usuario no autenticado"}), 403

    permisos = session.get("permisos", [])
    modulo_lower = modulo.lower()

    seccion_formateada = seccion.replace("_", " ")

    seccion_obj = Seccion.query.join(Modulo, Modulo.id == Seccion.modulo_id).filter(
        func.lower(Modulo.nombre_modulo) == modulo_lower,
        func.lower(Seccion.nombre) == seccion_formateada.lower(),
        UsuarioModulo.usuario_id == usuario_id
    ).first()

    if not seccion_obj:
        return jsonify({"error": "Sección no encontrada"}), 404

    return jsonify({
        "id": seccion_obj.id,
        "nombre": seccion_obj.nombre,
        "descripcion": seccion_obj.descripcion,
        "modulo": modulo_lower,
        "permisos": {
            "actualizar": f"{modulo_lower}_actualizar" in permisos,
            "eliminar": f"{modulo_lower}_eliminar" in permisos
        }
    })

@main_bp.route('/api/buscar/<modulo>', methods=['GET'])
def api_buscar(modulo):
    usuario_id = session.get('usuario_id')
    query = request.args.get('q', '').strip()
    offset = request.args.get('offset', default=0, type=int)
    limit = 6

    if not query:
        return jsonify({"secciones": [], "has_more": False})

    permisos = session.get('permisos', [])
    modulo_lower = modulo.lower()

    secciones_query = Seccion.query.join(Modulo, Modulo.id == Seccion.modulo_id).join(
        UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id
    ).filter(
        Modulo.nombre_modulo == modulo,
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%'))
    )

    total = secciones_query.count()
    secciones = secciones_query.offset(offset).limit(limit).all()

    secciones_json = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "modulo": modulo_lower,
            "permisos": {
                "actualizar": f"{modulo_lower}_actualizar" in permisos,
                "eliminar": f"{modulo_lower}_eliminar" in permisos
            }
        }
        for s in secciones
    ]

    return jsonify({
        "secciones": secciones_json,
        "has_more": offset + limit < total
    })




@main_bp.route('/api/buscar-avanzada', methods=['GET'])
def api_buscar_avanzada():
    usuario_id = session.get('usuario_id')
    query = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()
    offset = request.args.get('offset', default=0, type=int)
    limit = 6

    if not query:
        return jsonify({"secciones": [], "has_more": False})

    permisos = session.get('permisos', [])

    # Base query
    secciones_query = Seccion.query.join(Modulo, Modulo.id == Seccion.modulo_id).join(
        UsuarioModulo, UsuarioModulo.modulo_id == Seccion.modulo_id
    ).filter(
        UsuarioModulo.usuario_id == usuario_id,
        (Seccion.nombre.ilike(f'%{query}%')) | (Seccion.descripcion.ilike(f'%{query}%'))
    )

    # ✅ Si hay categoría, verificar permiso
    if categoria:
        permiso_modulo = f"ver_{categoria.lower()}"
        if permiso_modulo not in permisos:
            return jsonify({"secciones": [], "has_more": False})
        secciones_query = secciones_query.filter(Seccion.categoria == categoria)
    else:
        # ✅ Si no hay categoría, filtrar solo por módulos con permiso de visualización
        modulos_visibles = [p.replace("ver_", "") for p in permisos if p.startswith("ver_")]
        secciones_query = secciones_query.filter(func.lower(Modulo.nombre_modulo).in_(modulos_visibles))

    total = secciones_query.count()
    secciones = secciones_query.offset(offset).limit(limit).all()

    secciones_json = [
        {
            "id": s.id,
            "nombre": s.nombre,
            "descripcion": s.descripcion,
            "modulo": s.modulo.nombre_modulo.lower(),
            "permisos": {
                "actualizar": f"{s.modulo.nombre_modulo.lower()}_actualizar" in permisos,
                "eliminar": f"{s.modulo.nombre_modulo.lower()}_eliminar" in permisos
            }
        }
        for s in secciones
    ]

    return jsonify({
        "secciones": secciones_json,
        "has_more": offset + limit < total
    })
