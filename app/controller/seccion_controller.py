from app.models.md_seccion import Seccion

def obtener_secciones_por_categoria(categoria):
    """
    Recupera las secciones de la base de datos filtradas por categoría.
    :param categoria: Categoría de las secciones (e.g., 'materia', 'juego', 'proyecto').
    :return: Lista de secciones.
    """
    return Seccion.query.filter_by(categoria=categoria).all()


def obtener_categorias_unicas():
    """
    Recupera las categorías únicas de la tabla secciones.
    :return: Lista de categorías únicas.
    """
    return Seccion.query.with_entities(Seccion.categoria).distinct().all()
