from app import db

class UsuarioPermiso(db.Model):
    __tablename__ = "usuario_permiso"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    permiso_id = db.Column(db.Integer, db.ForeignKey("permiso.id", ondelete="CASCADE"), nullable=False)
    
    permiso = db.relationship("Permiso", backref=db.backref("permisos_usuarios", lazy="dynamic"))

    def __repr__(self):
        return f"<UsuarioPermiso usuario={self.usuario_id} permiso={self.permiso_id}>"
