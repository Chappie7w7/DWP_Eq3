from app import db
from .usuario import Usuario
from .modulo import Modulo

class UsuarioModulo(db.Model):
    __tablename__ = 'UsuarioModulo'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id', ondelete='CASCADE'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('Modulo.id', ondelete='CASCADE'), nullable=False)
    privilegio = db.Column(db.Enum('lectura', 'admin'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('modulos', lazy=True))
    modulo = db.relationship('Modulo', backref=db.backref('usuarios', lazy=True))
