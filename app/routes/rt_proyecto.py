from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from app import db
from app.models.md_proyecto import Proyecto
from app.models.md_seccion import Seccion

proyecto_bp = Blueprint('proyecto', __name__, url_prefix='/proyectos')

@proyecto_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_proyecto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        modulo_id = request.form.get('modulo_id')
        usuario_id = session.get('usuario_id')

        if not nombre or not descripcion or not modulo_id:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('proyecto.agregar_proyecto'))

        nuevo_proyecto = Proyecto(
            nombre=nombre, 
            descripcion=descripcion, 
            modulo_id=modulo_id,
            usuario_id=usuario_id
        )
        db.session.add(nuevo_proyecto)
        db.session.commit()

        nueva_seccion = Seccion(
            categoria="proyectos",
            nombre=nombre,
            descripcion=descripcion,
            url=f"/proyectos/{nombre.lower().replace(' ', '_')}",
            modulo_id=modulo_id
        )
        db.session.add(nueva_seccion)
        db.session.commit()

        flash('Proyecto agregado con éxito.', 'success')
        return redirect(url_for('proyecto.listar_proyectos'))

    return render_template('proyecto/agregar_proyecto.jinja')

@proyecto_bp.route('/', methods=['GET'])
def fix_trailing_slash():
    return redirect(url_for('proyecto.listar_proyectos'), code=301)

@proyecto_bp.route('', methods=['GET'])  
def listar_proyectos():
    return render_template("dinamico.jinja", titulo="Proyectos", breadcrumb=[
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Proyectos"}
    ])

@proyecto_bp.route('/editar/<int:proyecto_id>', methods=['GET', 'POST'])
def editar_proyecto(proyecto_id):
    proyecto = Seccion.query.get_or_404(proyecto_id)

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nueva_descripcion = request.form.get('descripcion')

        if not nuevo_nombre or not nueva_descripcion:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('proyecto.editar_proyecto', proyecto_id=proyecto.id))

        seccion = Seccion.query.filter_by(nombre=proyecto.nombre, modulo_id=proyecto.modulo_id).first()
        if seccion:
            seccion.nombre = nuevo_nombre
            seccion.descripcion = nueva_descripcion
            seccion.url = f"/proyectos/{nuevo_nombre.lower().replace(' ', '_')}"
        else:
            nueva_seccion = Seccion(
                nombre=nuevo_nombre,
                descripcion=nueva_descripcion,
                url=f"/proyectos/{nuevo_nombre.lower().replace(' ', '_')}",
                modulo_id=proyecto.modulo_id
            )
            db.session.add(nueva_seccion)

        proyecto.nombre = nuevo_nombre
        proyecto.descripcion = nueva_descripcion
        db.session.commit()
        
        
        # 🔹 Actualizar breadcrumb en la sesión
        breadcrumb = [
            {"name": "Inicio", "url": url_for('main.inicio')},
            {"name": "Proyectos", "url": url_for('proyecto.listar_proyectos')},
            {"name": nuevo_nombre, "url": f"/proyectos/{nuevo_nombre.lower().replace(' ', '_')}"}
        ]
        session['breadcrumb'] = breadcrumb
        session.modified = True

        flash('Proyecto actualizado correctamente.', 'success')
        return redirect(url_for('proyecto.listar_proyectos'))

 # 🔹 Obtener el breadcrumb actualizado para la plantilla
    breadcrumb = session.get('breadcrumb', [
        {"name": "Inicio", "url": url_for('main.inicio')},
        {"name": "Proyectos", "url": url_for('proyecto.listar_proyectos')},
        {"name": proyecto.nombre, "url": f"/proyectos/{proyecto.nombre.lower().replace(' ', '_')}"}
    ])

    return render_template('proyecto/editar_proyecto.jinja', proyecto=proyecto)

@proyecto_bp.route('/eliminar/<int:proyecto_id>', methods=['POST'])
def eliminar_proyecto(proyecto_id):
    proyecto = Seccion.query.get_or_404(proyecto_id)
    
    seccion = Seccion.query.filter_by(nombre=proyecto.nombre, modulo_id=proyecto.modulo_id).first()
    if seccion:
        db.session.delete(seccion)

    db.session.delete(proyecto)
    db.session.commit()

    flash('Proyecto eliminado con éxito.', 'success')
    return redirect(url_for('proyecto.listar_proyectos'))
