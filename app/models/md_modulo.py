from app import db

class Modulo(db.Model):
    __tablename__ = 'modulo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    # Relación inversa con Seccion
    secciones = db.relationship("Seccion", back_populates="modulo")

    def __repr__(self):
        return f'<Modulo {self.nombre}>'
