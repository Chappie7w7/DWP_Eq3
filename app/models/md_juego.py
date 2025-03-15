from app import db

class Juego(db.Model):
    __tablename__ = 'juego'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)

    # Relaciones
    modulo = db.relationship('Modulo', back_populates='juegos')
    usuario = db.relationship('Usuario', back_populates='juegos')

    def __repr__(self):
        return f'<Juego {self.nombre}>'
