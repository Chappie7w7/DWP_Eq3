from app import db

class UsuarioModulo(db.Model):
    __tablename__ = 'usuario_modulo'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id', ondelete='CASCADE'), nullable=False)
    privilegio = db.Column(db.String(50), nullable=False)  # Ejemplo: "lectura", "escritura", "admin"

    
    usuario = db.relationship('Usuario', back_populates='usuario_modulos', lazy='joined')
    modulo = db.relationship('Modulo', back_populates='usuario_modulos', lazy='joined')

    def __repr__(self):
        return f'<UsuarioModulo Usuario: {self.usuario_id}, Modulo: {self.modulo_id}, Privilegio: {self.privilegio}>'
