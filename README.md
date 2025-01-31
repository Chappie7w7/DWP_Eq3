# DWP_Eq3
 
#crea entono virtual 
 python -m venv .venv       

 #activar entorno virtual
  .\.venv\Scripts\activate   

  #instalar requirements
  pip install -r requirements.txt 
  python.exe -m pip install --upgrade pip  


Ejecutar
  flask run --debug
         O
  flask run
  
  #GENERAR SECRET KEY
   pwsh/python
Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import secrets
>>> print(secrets.token_hex(32))
4a15b75b799645eb3c35b2b4845418d2ff966c48294bbc4fc32758fd3cf0e239


#ejecutar antes de iniciar la app para creación de tablas
python init_db.py

#crea archivo .env 
FLASK_ENV=development
SECRET_KEY=a15b75b799645eb3c35b2b4845418d2ff966c48294bbc4fc32758fd3cf0e239
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:contraseña@127.0.0.1:3306/Nombre_BD

#Inicializa la carpeta de migraciones:
flask db init

#Genera la migración:
flask db migrate -m "Creación inicial de tablas"

#Aplica la migración:
flask db upgrade

