from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configurar LoginManager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para continuar.'
    login_manager.login_message_category = 'info'

    # Importar modelos para cargar usuarios
    from app.models.md_usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        """Cargar el usuario por su ID desde la base de datos"""
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.main import main_bp
    from app.routes.roles_routes import roles_bp
    from app.routes.permisos_routes import permisos_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(permisos_bp, url_prefix='/permisos')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Manejador de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_404.jinja'), 404

    return app
