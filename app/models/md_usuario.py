from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.models.md_rol import Rol
from app.models.md_usuario_modulo import UsuarioModulo  

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id', ondelete='CASCADE'), nullable=False)

    # Relación con la tabla 'rol'
    rol = db.relationship('Rol', back_populates='usuarios', lazy='joined')

    # Relación con 'UsuarioModulo'
    usuario_modulos = db.relationship('UsuarioModulo', back_populates='usuario', cascade='all, delete-orphan', lazy='joined')

    def set_password(self, password):
        """Genera un hash seguro para la contraseña."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'
