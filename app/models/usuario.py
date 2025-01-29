from app import db
from .rol import Rol

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('Rol.id', ondelete='CASCADE'), nullable=False)
    rol = db.relationship('Rol', backref=db.backref('usuarios', lazy=True))
