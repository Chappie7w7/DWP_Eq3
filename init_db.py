from app import create_app, db
from app.models.models import Usuario

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()
    print("Tablas creadas correctamente.")

    # Crear un usuario de prueba
    usuario = Usuario(nombre="juan", email="alexis@example.com", password="1234")
    
    db.session.add(usuario)
    db.session.commit()

    print("Usuario de prueba creado.")
