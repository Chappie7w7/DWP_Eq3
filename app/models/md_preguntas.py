from app import db

class PreguntaSecreta(db.Model):
    __tablename__ = 'pregunta_secreta'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pregunta = db.Column(db.String(255), nullable=False)

    # Relación con la tabla Respuestas
    respuestas = db.relationship('RespuestasP', back_populates='pregunta')

    def __repr__(self):
        return f'<PreguntaSecreta {self.pregunta}>'