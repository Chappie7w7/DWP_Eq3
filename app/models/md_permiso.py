from app import db

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    # Relación muchos a muchos con Rol
    roles = db.relationship('Rol', secondary='rol_permiso', back_populates='permisos')


    def __repr__(self):
        return f'<Permiso {self.nombre}>'