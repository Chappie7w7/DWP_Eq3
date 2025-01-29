from app import db

class Modulo(db.Model):
    __tablename__ = 'Modulo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
