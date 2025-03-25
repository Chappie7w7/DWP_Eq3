from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from flask_login import login_required
from app import db
from app.models.md_materia import Materia
from app.models.md_modulo import Modulo
from app.models.md_seccion import Seccion
from app.utils.decorators import permiso_requerido  

materia_bp = Blueprint('materia', __name__, url_prefix='/materias')

@materia_bp.route('/agregar', methods=['GET', 'POST'])
@login_required
@permiso_requerido('agregar_materia')
def agregar_materia():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        usuario_id = session.get('usuario_id')

        modulo = Modulo.query.filter_by(nombre_modulo="Materias").first()

        if not nombre or not descripcion or not modulo:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('materia.agregar_materia'))

        nueva_materia = Materia(
            nombre=nombre,
            descripcion=descripcion,
            modulo_id=modulo.id,
            usuario_id=usuario_id
        )
        db.session.add(nueva_materia)
        db.session.commit()

        nueva_seccion = Seccion(
            categoria="materias",
            nombre=nombre,
            descripcion=descripcion,
            url=f"/materias/{nombre.lower().replace(' ', '_')}",
            modulo_id=modulo.id
        )
        db.session.add(nueva_seccion)
        db.session.commit()

        flash('Materia agregada con éxito.', 'success')

        # ✅ Redirige a listar_materias con la lista actualizada
        return redirect(url_for('materia.listar_materias'))

    return render_template('materia/agregar_materia.jinja')


@materia_bp.route('', methods=['GET'])
def listar_materias():
    """
    Vista de materias usando `dinamico.jinja` para mantener el scroll infinito.
    """
    secciones = Seccion.query.filter_by(categoria="materias").all()
    return render_template("dinamico.jinja", titulo="Materias", secciones=secciones, breadcrumb=[
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Materias"}
    ])




@materia_bp.route('/editar/<int:materia_id>', methods=['GET', 'POST'])
@login_required
@permiso_requerido('editar_materia')
def editar_materia(materia_id):
    materia = Seccion.query.get_or_404(materia_id)

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nueva_descripcion = request.form.get('descripcion')

        if not nuevo_nombre or not nueva_descripcion:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('materia.editar_materia', materia_id=materia.id))

        # 🔹 Buscar y actualizar la sección correspondiente
        seccion = Seccion.query.filter_by(nombre=materia.nombre, modulo_id=materia.modulo_id).first()

        if seccion:
            # 🔹 Si la sección existe, actualizar nombre, descripción y URL
            seccion.nombre = nuevo_nombre
            seccion.descripcion = nueva_descripcion
            seccion.url = f"/materias/{nuevo_nombre.lower().replace(' ', '_')}"  
        else:
            # 🔹 Si no existe, crear una nueva entrada en la tabla `seccion`
            nueva_seccion = Seccion(
                nombre=nuevo_nombre,
                descripcion=nueva_descripcion,
                url=f"/materias/{nuevo_nombre.lower().replace(' ', '_')}",
                modulo_id=materia.modulo_id
            )
            db.session.add(nueva_seccion)

        # 🔹 Actualizar la materia en la base de datos
        materia.nombre = nuevo_nombre
        materia.descripcion = nueva_descripcion
        db.session.commit()

        # 🔹 Actualizar breadcrumb en la sesión
        breadcrumb = [
            {"name": "Inicio", "url": url_for('main.inicio')},
            {"name": "Materias", "url": url_for('materia.listar_materias')},
            {"name": nuevo_nombre, "url": f"/materias/{nuevo_nombre.lower().replace(' ', '_')}"}
        ]
        session['breadcrumb'] = breadcrumb
        session.modified = True

        flash('Materia y sección actualizadas correctamente.', 'success')
        return redirect(url_for('materia.listar_materias'))

    # 🔹 Obtener el breadcrumb actualizado para la plantilla
    breadcrumb = session.get('breadcrumb', [
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Materias", "url": url_for('materia.listar_materias')},
        {"name": materia.nombre, "url": f"/materias/{materia.nombre.lower().replace(' ', '_')}"}
    ])

    return render_template('materia/editar_materia.jinja', materia=materia, breadcrumb=breadcrumb)

@materia_bp.route('/eliminar/<int:materia_id>', methods=['POST'])
@login_required
@permiso_requerido('eliminar_materia')
def eliminar_materia(materia_id):
    materia = Seccion.query.get_or_404(materia_id)

    # Buscar y eliminar la sección asociada
    seccion = Seccion.query.filter_by(nombre=materia.nombre, modulo_id=materia.modulo_id).first()
    if seccion:
        db.session.delete(seccion)

    # Eliminar la materia
    db.session.delete(materia)
    db.session.commit()

    flash('Materia y su sección asociada eliminadas con éxito.', 'success')
    return redirect(url_for('materia.listar_materias'))
