from app import db
from sqlalchemy.orm import relationship

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    # Relación inversa con Usuario
    usuarios = relationship('Usuario', back_populates='rol')

    def __repr__(self):
        return f'<Rol {self.nombre}>'
