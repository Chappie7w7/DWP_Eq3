from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)

    # Registrar Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app
