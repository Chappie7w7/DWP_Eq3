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


ejecutar antes de iniciar la app
python init_db.py