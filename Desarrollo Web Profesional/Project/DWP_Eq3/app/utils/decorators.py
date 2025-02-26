from functools import wraps
from flask import session, abort

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
