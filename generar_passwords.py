from werkzeug.security import generate_password_hash

# Generar hashes para los usuarios
hashed_password_admin = generate_password_hash('admin123', method='scrypt')
hashed_password_alexis = generate_password_hash('alexis123', method='scrypt')
hashed_password_josue = generate_password_hash('josue123', method='scrypt')

# Mostrar las contraseñas hasheadas
print("Hashed passwords:")
print(f"Admin: {hashed_password_admin}")
print(f"Alexis: {hashed_password_alexis}")
print(f"Josue: {hashed_password_josue}")
