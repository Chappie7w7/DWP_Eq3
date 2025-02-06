import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class Config:
    # Clave secreta para la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Desactivar seguimiento de modificaciones (optimización)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
