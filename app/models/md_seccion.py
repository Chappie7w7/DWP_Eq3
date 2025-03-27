from app import db

class Seccion(db.Model):
    __tablename__ = 'seccion'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)

    # Relaciones
    modulo = db.relationship('Modulo', back_populates='secciones', lazy='joined')
    usuario = db.relationship('Usuario', backref='secciones', lazy=True)

    def __repr__(self):
        return f'<Seccion {self.nombre}>'
