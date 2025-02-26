# DWP_Eq3
 
python -m venv .venv       # Crea el entorno virtual
.\.venv\Scripts\activate   # Activa el entorno virtual
deactivate .venv           # Desactiva el entorno virtual (cuando sea necesario)
 

  #instalar requirements
  pip install -r requirements.txt 
  python.exe -m pip install --upgrade pip  


Ejecutar
flask run --debug   # Con modo debug
flask run           # Sin modo debug

  
  #GENERAR SECRET KEY
   pwsh/python
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import secrets
>>> print(secrets.token_hex(32))
4a15b75b799645eb3c35b2b4845418d2ff966c48294bbc4fc32758fd3cf0e239



FLASK_ENV=development
SECRET_KEY=tu_secret_key_generado
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:tu_contraseña@127.0.0.1:3306/Nombre_BD


#Inicializa la carpeta de migraciones:
flask db init

#Genera la migración:
flask db migrate -m "Mensaje"

#Aplica la migración:
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