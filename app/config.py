from dotenv import load_dotenv
import os

load_dotenv('.env')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

