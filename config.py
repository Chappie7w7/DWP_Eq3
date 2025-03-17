import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class Config:
    # Clave secreta para la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecreto')  
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave_jwt_supersecreta')  # Para firmar los tokens

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Desactivar seguimiento de modificaciones (optimización)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Tu correo Gmail
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Contraseña de aplicación de Gmail
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')  # Remitente predeterminado
    MAIL_DEBUG = True  # Activa debug para pruebas (en desarrollo)

    # Tiempo de vida del OTP (en minutos)
    OTP_EXPIRATION_MINUTES = 2
