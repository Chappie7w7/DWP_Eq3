from app import db

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    # Relación con la tabla 'usuario'
    usuarios = db.relationship('Usuario', back_populates='rol', cascade='all, delete-orphan', lazy='joined')

    # Relación muchos a muchos con Permiso
    permisos = db.relationship('Permiso', secondary='rol_permiso', back_populates='roles')

    def __repr__(self):
        return f'<Rol {self.nombre}>'