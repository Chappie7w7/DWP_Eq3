from app import db


class UsuarioModulo(db.Model):
    __tablename__ = 'usuario_modulo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    privilegio = db.Column(db.String(50), nullable=False)  # Ejemplo: "lectura", "escritura", "admin"

    # Relaciones
    usuario = db.relationship('Usuario', backref='usuario_modulos')
    modulo = db.relationship('Modulo', backref='usuario_modulos')

    def __repr__(self):
        return f'<UsuarioModulo Usuario: {self.usuario_id}, Modulo: {self.modulo_id}, Privilegio: {self.privilegio}>'
