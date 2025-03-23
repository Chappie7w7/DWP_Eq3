from flask import session

def tiene_permiso(nombre_permiso):
    """
    Verifica si el permiso está en la sesión del usuario.
    Ejemplo: 'materias_editar'
    """
    permisos = session.get('permisos', [])
    return nombre_permiso in permisos
