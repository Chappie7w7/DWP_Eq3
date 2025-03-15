from app import db

class Proyecto(db.Model):
    __tablename__ = 'proyecto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)

    # Relaciones
    modulo = db.relationship('Modulo', back_populates='proyectos')
    usuario = db.relationship('Usuario', back_populates='proyectos')

    def __repr__(self):
        return f'<Proyecto {self.nombre}>'
