from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class RespuestasP(db.Model):
    __tablename__ = 'respuestas_preguntas'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    respuesta_hash = db.Column(db.String(255), nullable=False)  # Almacenar el hash de la respuesta
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta_secreta.id', ondelete='CASCADE'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='respuestas_preguntas')
    pregunta = db.relationship('PreguntaSecreta', back_populates='respuestas')

    def set_respuesta(self, respuesta):
        """Genera un hash seguro para la respuesta."""
        self.respuesta_hash = generate_password_hash(respuesta, method='scrypt')

    def check_respuesta(self, respuesta):
        """Verifica si la respuesta ingresada coincide con el hash almacenado."""
        return check_password_hash(self.respuesta_hash, respuesta)