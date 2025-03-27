from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_required
from app import db
from app.models.md_permiso import Permiso
from app.models.md_rol import Rol
from app.models.md_usuario import Usuario
from app.models.md_usuario_permiso import UsuarioPermiso
from app.models.md_modulo import Modulo
from app.models.md_usuario_modulo import UsuarioModulo
from app.utils.decorators import token_required

permiso_bp = Blueprint('permiso', __name__, url_prefix='/permisos')


@permiso_bp.route('/gestionar', methods=['GET', 'POST'])
@login_required
@token_required
def gestionar_permisos():
    current_user = Usuario.query.get(session.get("usuario_id"))
    usuarios = Usuario.query.join(Rol).filter(Rol.nombre != "Administrador").all()
    permisos = Permiso.query.all()

    mensaje = request.args.get('mensaje')
    tipo_mensaje = request.args.get('tipo')
    permisos_usuario = []

    usuario_id = request.form.get('usuario_id') or request.args.get('usuario_id')
    if usuario_id:
        usuario_id = int(usuario_id)

    # 🔄 Guardar permisos
    if request.method == 'POST':
        permisos_seleccionados = request.form.getlist('permisos[]')
        print("📥 Permisos seleccionados:", permisos_seleccionados)

        if not usuario_id:
            mensaje = "⚠️ Debes seleccionar un usuario."
            tipo_mensaje = "error"
        else:
            # Limpiar permisos anteriores
            UsuarioPermiso.query.filter_by(usuario_id=usuario_id).delete()

            # Asignar los nuevos permisos
            for permiso_id in permisos_seleccionados:
                db.session.add(UsuarioPermiso(usuario_id=usuario_id, permiso_id=int(permiso_id)))

            # Obtener los nombres de los permisos seleccionados
            permisos_nombres = [
                p.nombre for p in Permiso.query.filter(Permiso.id.in_(permisos_seleccionados)).all()
            ]

            for nombre in permisos_nombres:
                if nombre.endswith("_crear"):
                    nombre_modulo = nombre.replace("_crear", "").capitalize()

                    # Verificar si ya existe un módulo con ese nombre para ese usuario
                    modulo_existente = Modulo.query.filter_by(nombre_modulo=nombre_modulo, propietario=str(usuario_id)).first()

                    if not modulo_existente:
                        nuevo_modulo = Modulo(nombre_modulo=nombre_modulo, propietario=str(usuario_id))
                        db.session.add(nuevo_modulo)
                        db.session.flush()  # Obtener ID del nuevo módulo

                        db.session.add(UsuarioModulo(
                            usuario_id=usuario_id,
                            modulo_id=nuevo_modulo.id,
                            privilegio='admin'
                        ))
                    else:
                        ya_asignado = UsuarioModulo.query.filter_by(
                            usuario_id=usuario_id,
                            modulo_id=modulo_existente.id
                        ).first()
                        if not ya_asignado:
                            db.session.add(UsuarioModulo(
                                usuario_id=usuario_id,
                                modulo_id=modulo_existente.id,
                                privilegio='admin'
                            ))

            db.session.commit()

            return redirect(url_for(
                'permiso.gestionar_permisos',
                usuario_id=usuario_id,
                mensaje="✅ Permisos actualizados correctamente.",
                tipo="success"
            ))

    if usuario_id:
        permisos_usuario = [
            up.permiso_id for up in UsuarioPermiso.query.filter_by(usuario_id=usuario_id).all()
        ]
        print("🔍 Permisos ya asignados al usuario:", permisos_usuario)

    return render_template(
        'permisos/gestionar_permisos.jinja',
        usuarios=usuarios,
        permisos=permisos,
        permisos_usuario=permisos_usuario,
        mensaje=mensaje,
        tipo_mensaje=tipo_mensaje,
        usuario_id_seleccionado=usuario_id
    )
