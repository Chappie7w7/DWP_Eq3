from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from app import db
from app.models.md_juego import Juego
from app.models.md_modulo import Modulo
from app.models.md_seccion import Seccion
from app.utils.decorators import permiso_requerido, token_required  

juego_bp = Blueprint('juego', __name__, url_prefix='/juegos')

@juego_bp.route('/agregar', methods=['GET', 'POST'])
@token_required
@permiso_requerido('juegos_crear')
def agregar_juego():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        usuario_id = session.get('usuario_id')

        # ✅ Buscar módulo que le pertenece al usuario
        modulo = Modulo.query.filter_by(nombre_modulo="Juegos", propietario=usuario_id).first()

        if not nombre or not descripcion or not modulo:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('juego.agregar_juego'))

        nuevo_juego = Juego(
            nombre=nombre,
            descripcion=descripcion,
            modulo_id=modulo.id,
            usuario_id=usuario_id
        )
        db.session.add(nuevo_juego)
        db.session.commit()

        nueva_seccion = Seccion(
            categoria="juegos",
            nombre=nombre,
            descripcion=descripcion,
            url=f"/juegos/{nombre.lower().replace(' ', '_')}",
            modulo_id=modulo.id,
            usuario_id=usuario_id
        )
        db.session.add(nueva_seccion)
        db.session.commit()

        flash('Juego agregado con éxito.', 'success')
        return redirect(url_for('juego.listar_juegos'))

    return render_template('juego/agregar_juego.jinja')



@juego_bp.route('/', methods=['GET'])
def fix_trailing_slash():
    return redirect(url_for('juego.listar_juegos'), code=301)

@juego_bp.route('', methods=['GET'])  
@token_required
@permiso_requerido('ver_juegos')
def listar_juegos():
    usuario_id = session.get("usuario_id")

    # Obtener el módulo de juegos que le pertenece al usuario
    modulo = Modulo.query.filter_by(nombre_modulo="Juegos", propietario=usuario_id).first()

    secciones = []
    if modulo:
        secciones = Seccion.query.filter_by(modulo_id=modulo.id, usuario_id=usuario_id).all()

    return render_template("dinamico.jinja", titulo="Juegos", secciones=secciones, breadcrumb=[
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Juegos"}
    ])




@juego_bp.route('/editar/<int:juego_id>', methods=['GET', 'POST'])
@token_required
@permiso_requerido('juegos_actualizar')
def editar_juego(juego_id):
    usuario_id = session.get("usuario_id")

    juego = Seccion.query.filter_by(id=juego_id, usuario_id=usuario_id).first_or_404()

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nueva_descripcion = request.form.get('descripcion')

        if not nuevo_nombre or not nueva_descripcion:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('juego.editar_juego', juego_id=juego.id))

        seccion = Seccion.query.filter_by(nombre=juego.nombre, modulo_id=juego.modulo_id).first()

        if seccion:
            seccion.nombre = nuevo_nombre
            seccion.descripcion = nueva_descripcion
            seccion.url = f"/juegos/{nuevo_nombre.lower().replace(' ', '_')}"  
        else:
            nueva_seccion = Seccion(
                nombre=nuevo_nombre,
                descripcion=nueva_descripcion,
                url=f"/juegos/{nuevo_nombre.lower().replace(' ', '_')}",
                modulo_id=juego.modulo_id
            )
            db.session.add(nueva_seccion)

        juego.nombre = nuevo_nombre
        juego.descripcion = nueva_descripcion
        db.session.commit()

        breadcrumb = [
            {"name": "Inicio", "url": url_for('main.inicio')},
            {"name": "Juegos", "url": url_for('juego.listar_juegos')},
            {"name": nuevo_nombre, "url": f"/juegos/{nuevo_nombre.lower().replace(' ', '_')}"}
        ]
        session['breadcrumb'] = breadcrumb
        session.modified = True

        flash('Juego y sección actualizados correctamente.', 'success')
        return redirect(url_for('juego.listar_juegos'))

    breadcrumb = session.get('breadcrumb', [
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Juegos", "url": url_for('juego.listar_juegos')},
        {"name": juego.nombre, "url": f"/juegos/{juego.nombre.lower().replace(' ', '_')}"}
    ])

    return render_template('juego/editar_juego.jinja', juego=juego, breadcrumb=breadcrumb)

@juego_bp.route('/eliminar/<int:juego_id>', methods=['POST'])
@token_required
@permiso_requerido('juegos_eliminar')
def eliminar_juego(juego_id):
    usuario_id = session.get("usuario_id")

    juego = Seccion.query.filter_by(id=juego_id, usuario_id=usuario_id).first_or_404()
    db.session.delete(juego)
    db.session.commit()

    flash('Juego y su sección asociada eliminados con éxito.', 'success')
    return redirect(url_for('juego.listar_juegos'))
