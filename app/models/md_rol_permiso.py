from app import db

class RolPermiso(db.Model):
    __tablename__ = 'rol_permiso'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id', ondelete='CASCADE'), nullable=False)
    permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<RolPermiso rol_id={self.rol_id} permiso_id={self.permiso_id}>'
