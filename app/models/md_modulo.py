from app import db

class Modulo(db.Model):
    __tablename__ = 'modulo'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    # Relaciones
    secciones = db.relationship('Seccion', back_populates='modulo', cascade='all, delete-orphan', lazy='joined')
    usuario_modulos = db.relationship('UsuarioModulo', back_populates='modulo', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f'<Modulo {self.nombre}>'
