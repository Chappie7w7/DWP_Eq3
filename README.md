# 🟢 DWP_Eq3 

python -m venv .venv        # 🔹 Crea el entorno virtual
.\.venv\Scripts\activate    # 🔹 Activa el entorno virtual
deactivate .venv            # 🔹 Desactiva el entorno virtual (cuando sea necesario)

# 📦 Instalación de dependencias
pip install -r requirements.txt  # 🔹 Instala las dependencias del proyecto
python.exe -m pip install --upgrade pip  # 🔹 Actualiza pip a la última versión

# 🚀 Ejecución del servidor Flask
flask run --debug  # 🔥 Modo Debug (Para desarrollo)
flask run          # 🚀 Modo normal (Para producción)



# 🌟 Configuración de Entorno en Flask
# 🔧 Variables de entorno
FLASK_ENV=development
SECRET_KEY=tu_secret_key_generado
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:tu_contraseña@127.0.0.1:3306/Nombre_BD



# 📌 Inicialización y Migraciones de Base de Datos
# 🔹 Inicializa la carpeta de migraciones
flask db init

# 🔹 Genera una nueva migración
flask db migrate -m "Mensaje"

# 🔹 Aplica la migración a la base de datos
flask db upgrade



# Guía Rápida: Configuración de Usuarios y Contraseñas

## 1. Generar Contraseñas Hasheadas
1. Abre el archivo `generar_passwords.py`.
2. Ejecuta el script:
   ```bash
   python generar_passwords.py

INSERT INTO usuario (nombre, email, password, rol_id) VALUES
('Administrador', 'admin@example.com', 'hashed_password_admin', 1),
('Alexis', 'alexis@example.com', 'hashed_password_alexis', 2),
('Josue', 'josue@example.com', 'hashed_password_josue', 2);


2. Modifica las líneas para agregar el nuevo usuario:
   ```python
   passwords = {
       "NuevoUsuario": "nueva_contraseña"
   }
   
   Ejecuta el script:

python generar_passwords.py

Inserta el nuevo usuario con su contraseña hasheada:

INSERT INTO usuario (nombre, email, password, rol_id) VALUES
('Nuevo Usuario', 'nuevo@example.com', 'hashed_password_nuevo_usuario', id_rol);