from datetime import datetime
from functools import wraps
from flask import Config, current_app, jsonify, redirect, session, abort, url_for
import jwt
from app import db
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
            exp_time = decoded_token.get("exp")

            print(f"📥 Token recibido en sesión: {token}")
            print(f"⌛ Expiración del token: {datetime.fromtimestamp(exp_time)}")
            print(f"🕒 Hora actual: {datetime.now()}")

            if datetime.now().timestamp() > exp_time:
                print("⏳ Token expirado, eliminando...")

                usuario = Usuario.query.get(decoded_token["usuario_id"])
                if usuario:
                    usuario.token = None  
                    db.session.commit()
                    print("🗑️ Token eliminado de la base de datos.")

                session['token_expired'] = "Tu sesión ha expirado. Por favor, inicia sesión nuevamente."
                session.modified = True  # Permite modificar la sesión antes de limpiarla
                return redirect(url_for('auth.login'))

            current_user = Usuario.query.get(decoded_token["usuario_id"])
            if not current_user:
                print("❌ Usuario no encontrado")
                session.clear()
                return redirect(url_for('auth.login'))

        except jwt.ExpiredSignatureError:
            print("🔥 Token expirado, eliminando en BD...")

            session['token_expired'] = "Tu sesión ha expirado. Por favor, inicia sesión nuevamente."
            session.modified = True  

            usuario = Usuario.query.filter_by(token=token).first()
            if usuario:
                usuario.token = None
                db.session.commit()
                print("🗑️ Token eliminado de la base de datos.")

            return redirect(url_for('auth.login'))  

        except jwt.InvalidTokenError:
            print("⚠️ Token inválido")
            session.clear()
            return redirect(url_for('auth.login'))

        return f(current_user, *args, **kwargs)

    return decorator
