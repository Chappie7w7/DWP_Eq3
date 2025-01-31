from app.models.md_modulo import Modulo

def obtener_todos_los_modulos():
    """
    Recupera todos los módulos disponibles.
    :return: Lista de módulos.
    """
    return Modulo.query.all()
