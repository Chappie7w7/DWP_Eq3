from app import db

class Modulo(db.Model):
    __tablename__ = 'modulo'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_modulo = db.Column(db.String(100), nullable=False)  
    propietario = db.Column(db.String(100), nullable=False)  

    # Relaciones
    secciones = db.relationship('Seccion', back_populates='modulo', cascade='all, delete-orphan', lazy='joined')
    usuario_modulos = db.relationship('UsuarioModulo', back_populates='modulo', cascade='all, delete-orphan', lazy='joined')
    
    # Relaciones con las nuevas tablas
    materias = db.relationship('Materia', back_populates='modulo', cascade='all, delete-orphan')
    juegos = db.relationship('Juego', back_populates='modulo', cascade='all, delete-orphan')
    proyectos = db.relationship('Proyecto', back_populates='modulo', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Modulo {self.nombre_modulo} - {self.propietario}>'
