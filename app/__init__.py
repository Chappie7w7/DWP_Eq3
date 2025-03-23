from flask import Flask, app, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from app.utils.filters import tiene_permiso  

# Inicializar extensiones
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    mail.init_app(app)
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


    from app.routes import register_blueprints
    register_blueprints(app)

    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_404.jinja'), 404

    
    with app.app_context():
        db.create_all()
        
    app.jinja_env.globals['tiene_permiso'] = tiene_permiso


    return app
