from werkzeug.security import generate_password_hash

# Lista de usuarios con sus contraseñas
usuarios = [
    {"nombre": "Administrador", "email": "admin@example.com", "contraseña": "admin123"},
    {"nombre": "Alexis", "email": "alexis@example.com", "contraseña": "alexis123"},
    {"nombre": "Josue", "email": "josue@example.com", "contraseña": "josue123"},
]

# Generar y mostrar los hashes
for usuario in usuarios:
    hash_contraseña = generate_password_hash(usuario["contraseña"])
    print(f"Hash para {usuario['nombre']} ({usuario['email']}): {hash_contraseña}")
