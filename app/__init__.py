from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config['SECRET_KEY'] = '4a15b75b799645eb3c35b2b4845418d2ff966c48294bbc4fc32758fd3cf0e239'  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Ruta de la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar advertencias innecesarias


    db.init_app(app)

    # Registrar Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.main import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
      # Manejador de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_404.jinja'), 404

    return app

