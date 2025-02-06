from app import db

class Rol(db.Model):
    __tablename__ = 'rol'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    # Relación con la tabla 'usuario'
    usuarios = db.relationship('Usuario', back_populates='rol', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f'<Rol {self.nombre}>'
