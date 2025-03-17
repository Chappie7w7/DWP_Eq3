from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from app import db
from app.models.md_materia import Materia

materia_bp = Blueprint('materia', __name__, url_prefix='/materias')

from app.models.md_seccion import Seccion  

@materia_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_materia():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        modulo_id = request.form.get('modulo_id')  # Asegurar que se recibe
        usuario_id = session.get('usuario_id')  # Obtener el usuario logueado

        if not nombre or not descripcion or not modulo_id:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('materia.agregar_materia'))

        # Crear la materia
        nueva_materia = Materia(
            nombre=nombre, 
            descripcion=descripcion, 
            modulo_id=modulo_id,
            usuario_id=usuario_id
        )
        db.session.add(nueva_materia)
        db.session.commit()

        # Crear automáticamente una sección en la tabla "seccion"
        nueva_seccion = Seccion(
            categoria="materias",
            nombre=nombre,
            descripcion=descripcion,
            url=f"/materias/{nombre.lower().replace(' ', '_')}",
            modulo_id=modulo_id
        )
        db.session.add(nueva_seccion)
        db.session.commit()

        flash('Materia agregada con éxito.', 'success')
        return redirect(url_for('materia.listar_materias'))

    return render_template('materia/agregar_materia.jinja')


# 🔹 usenlo si tienen problemas de rutas, si no no
@materia_bp.route('/', methods=['GET'])
def fix_trailing_slash():
    return redirect(url_for('materia.listar_materias'), code=301)  # 🔹 Redirección manual

@materia_bp.route('', methods=['GET'])  
def listar_materias():
    """
    Vista de materias usando `dinamico.jinja` para mantener el scroll infinito.
    """
    return render_template("dinamico.jinja", titulo="Materias", breadcrumb=[
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Materias"}
    ])



@materia_bp.route('/editar/<int:materia_id>', methods=['GET', 'POST'])
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
