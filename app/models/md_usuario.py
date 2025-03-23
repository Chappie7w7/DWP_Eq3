from datetime import datetime, timedelta
import random
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
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)  # Aquí agregas el campo
    token = db.Column(db.String(500), nullable=True) 
    token_sesion = db.Column(db.String(500), nullable=True)  # Para manejar sesiones únicas
    
        # 🔹 Opciones de seguridad para control de sesiones
    cerrar_sesiones_activas = db.Column(db.Boolean, default=True)  # Nuevo campo
    confirmar_inicio_sesion = db.Column(db.Boolean, default=True)  # Nuevo campo

    # 🔹 Método para actualizar preferencias de seguridad
    def actualizar_preferencias(self, cerrar_sesiones, confirmar_sesion):
        self.cerrar_sesiones_activas = cerrar_sesiones
        self.confirmar_inicio_sesion = confirmar_sesion
        db.session.commit()

    
    # OTP (One-Time Password) para autenticación multifactor
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiration = db.Column(db.DateTime, nullable=True)

    # Relación con la tabla 'rol'
    rol = db.relationship('Rol', back_populates='usuarios', lazy='joined')
    usuario_permisos = db.relationship('UsuarioPermiso', backref='usuario', cascade='all, delete-orphan')


    # Relación con 'UsuarioModulo'
    usuario_modulos = db.relationship('UsuarioModulo', back_populates='usuario', cascade='all, delete-orphan', lazy='joined')

    respuestas_preguntas = db.relationship('RespuestasP', back_populates='usuario')
    
    # Relaciones con Materia, Juego y Proyecto
    materias = db.relationship('Materia', back_populates='usuario', cascade='all, delete-orphan')
    juegos = db.relationship('Juego', back_populates='usuario', cascade='all, delete-orphan')
    proyectos = db.relationship('Proyecto', back_populates='usuario', cascade='all, delete-orphan')

    def set_password(self, password):
        """Genera un hash seguro para la contraseña."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash."""
        return check_password_hash(self.password, password)
    
    def generar_otp(self):
        """Genera un código OTP de 6 dígitos con 2 minutos de expiración."""
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.otp_expiration = datetime.now() + timedelta(minutes=2)

    def __repr__(self):
        return f'<Usuario {self.email}>'
    