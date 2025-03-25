from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_required
from app import db
from app.models.md_permiso import Permiso
from app.models.md_rol import Rol
from app.models.md_usuario import Usuario
from app.models.md_usuario_permiso import UsuarioPermiso
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

            # Asignar los nuevos
            for permiso_id in permisos_seleccionados:
                db.session.add(UsuarioPermiso(usuario_id=usuario_id, permiso_id=int(permiso_id)))

            db.session.commit()

            # Redireccionar para evitar doble submit y mostrar mensaje
            return redirect(url_for(
                'permiso.gestionar_permisos',
                usuario_id=usuario_id,
                mensaje="✅ Permisos actualizados correctamente.",
                tipo="success"
            ))

    # Cargar permisos asignados si ya hay usuario seleccionado
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
