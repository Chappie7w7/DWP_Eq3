from app import db

class IntentosRecuperacion(db.Model):
    __tablename__ = 'intentos_recuperacion'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    intentos = db.Column(db.Integer, default=0)
    ultimo_intento = db.Column(db.DateTime, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)