from app import db

class Materia(db.Model):
    __tablename__ = 'materia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)

    # Relaciones
    modulo = db.relationship('Modulo', back_populates='materias')
    usuario = db.relationship('Usuario', back_populates='materias')

    def __repr__(self):
        return f'<Materia {self.nombre}>'
