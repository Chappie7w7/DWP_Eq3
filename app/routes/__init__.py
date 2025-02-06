from flask import Blueprint

from .rt_auth import auth_bp
from .rt_dashboard import dashboard_bp
from .rt_main import main_bp
from .rt_permisos import permisos_bp
from .rt_roles import roles_bp
from .rt_secciones import secciones_bp

def register_blueprints(app):
    """Registrar todos los blueprints en Flask."""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(main_bp)
    app.register_blueprint(permisos_bp, url_prefix='/permisos')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(secciones_bp, url_prefix='/secciones')
