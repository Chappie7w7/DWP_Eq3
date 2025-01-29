from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config  # Importa la configuración correctamente

# Inicializar SQLAlchemy y Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Cargar la configuración desde config.py

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.main import main_bp
    from app.routes.roles_routes import roles_bp
    from app.routes.permisos_routes import permisos_bp

    app.register_blueprint(roles_bp)
    app.register_blueprint(permisos_bp)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_404.jinja'), 404

    return app
