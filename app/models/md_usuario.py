from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)

    # Relación con la tabla Rol
    rol = relationship('Rol', back_populates='usuarios')

    def set_password(self, password):
        """Crea un hash seguro para la contraseña"""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Verifica si la contraseña ingresada es correcta"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'
