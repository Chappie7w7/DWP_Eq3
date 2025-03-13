from app import db

class ActiveSession(db.Model):
    __tablename__ = 'session_active'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    session_id = db.Column(db.String(255), unique=True, nullable=False)