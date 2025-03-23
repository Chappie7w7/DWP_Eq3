from app.models.md_permiso import Permiso
from app.models.md_usuario_permiso import UsuarioPermiso
from flask import session
from app import db

def cargar_permisos_usuario(usuario_id):
    permisos = (
        db.session.query(Permiso.nombre)
        .join(UsuarioPermiso)
        .filter(UsuarioPermiso.usuario_id == usuario_id)
        .all()
    )
    session['permisos'] = [p.nombre for p in permisos]
