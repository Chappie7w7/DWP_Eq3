from app import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.md_modulo import Modulo  # Importar Modulo, no redefinirlo

class Seccion(db.Model):
    __tablename__ = "seccion"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulo.id"), nullable=False)

    # Relación inversa con Modulo (importación diferida)
    modulo = relationship("Modulo", back_populates="secciones", lazy='joined')

    def __repr__(self):
        return f'<Seccion {self.nombre}>'