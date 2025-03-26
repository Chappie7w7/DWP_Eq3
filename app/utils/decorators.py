from datetime import datetime
from functools import wraps
from flask import Config, current_app, flash, jsonify, redirect, session, abort, url_for
import jwt
from app import db
from app.models.md_permiso import Permiso
from app.models.md_rol import Rol
from app.models.md_usuario import Usuario

def requiere_modulo(modulo_nombre, permiso_requerido='lectura'):
    """Verifica si el usuario tiene acceso a un módulo con el permiso adecuado"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            modulos = session.get('modulos', {})
            # Verificar si el módulo existe en los permisos del usuario
            if modulo_nombre not in modulos:
                abort(403)  # Acceso denegado si no está permitido

            # Validar el permiso requerido
            if permiso_requerido == 'admin' and modulos[modulo_nombre] != 'admin':
                abort(403)  # Acceso denegado si no tiene permiso de administrador

            return f(*args, **kwargs)
        return wrapper
    return decorator

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = session.get('token')

        if not token:
            print("❌ No hay token en la sesión")
            return redirect(url_for('auth.login'))

        try:
            decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            usuario = Usuario.query.get(decoded_token["usuario_id"])

            # 🔹 Verificar si la sesión actual sigue siendo válida
            if not usuario or usuario.token_sesion != token:
                print("🚫 Sesión inválida o cerrada en otro dispositivo")
                session.clear()
                flash('Tu sesión ha sido cerrada en otro dispositivo. Vuelve a iniciar sesión.', 'danger')
                return redirect(url_for('auth.login'))

            # 🔹 Verificar si el token ha expirado
            exp_time = decoded_token.get("exp")
            if datetime.now().timestamp() > exp_time:
                print("🔥 Token expirado, eliminando...")
                usuario.token_sesion = None
                db.session.commit()
                session.clear()
                flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'danger')
                return redirect(url_for('auth.login'))

        except jwt.ExpiredSignatureError:
            print("⚠️ Token expirado")
            session.clear()
            flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'danger')
            return redirect(url_for('auth.login'))

        except jwt.InvalidTokenError:
            print("⚠️ Token inválido")
            session.clear()
            flash('Sesión inválida. Por favor, inicia sesión nuevamente.', 'danger')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)


    return decorator


def permiso_requerido(nombre_permiso):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario_id = session.get('usuario_id')

            if not usuario_id:
                flash("Debes iniciar sesión.", "warning")
                return redirect(url_for('auth.login'))

            permisos = session.get('permisos', [])
            if nombre_permiso not in permisos:
                flash("No tienes permiso para realizar esta acción.", "danger")
                return redirect(url_for('main.inicio'))

            return func(*args, **kwargs)
        return wrapper
    return decorador



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuario_id = session.get('usuario_id')
        print(f"🧪 ID usuario: {usuario_id}")  

        if not usuario_id:
            print("⚠️ No logueado, redirigiendo a login")
            flash('Debes iniciar sesión.', 'warning')
            return redirect(url_for('auth.login'))

        usuario = Usuario.query.get(usuario_id)
        print(f"🧪 Rol del usuario: {usuario.rol.nombre}")  

        if not usuario or usuario.rol.nombre.lower() != 'administrador':
            print("🚫 No es admin")
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('main.inicio'))

        print("✅ Acceso como admin")
        return f(*args, **kwargs)
    return decorated_function
