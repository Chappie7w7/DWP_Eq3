import os
import requests
from dotenv import load_dotenv
import base64

# Cargar variables de entorno
load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Depuración: Verificar que las variables se están cargando correctamente
print("USERNAME:", USERNAME)
print("PASSWORD:", PASSWORD)

def enviar_codigo_sms(phone, verification_code):
    url = "https://rest.clicksend.com/v3/sms/send"
    
    # Crear la cadena de autenticación
    auth_string = f"{USERNAME}:{PASSWORD}"
    
    # Codificar en Base64
    auth_bytes = auth_string.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    
    # Configurar las cabeceras
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64_auth}"  # Incluir la autenticación Basic Auth
    }
    
    # Configurar el cuerpo de la solicitud
    payload = {
        "messages": [
            {
                "source": "python",
                "from": "YourAppName",  # Opcional, usa un remitente personalizado
                "body": f"Tu código de verificación es: {verification_code}",
                "to": phone
            }
        ]
    }
    
    # Enviar la solicitud
    response = requests.post(url, json=payload, headers=headers)
    
    # Manejar la respuesta
    if response.status_code == 401:
        print("Error de autenticación: Verifica tus credenciales de ClickSend.")
        print(f"Respuesta completa: {response.text}")
        return False
    elif response.status_code != 200:
        print(f"Error en la respuesta de ClickSend: {response.status_code}")
        print(f"Respuesta completa: {response.text}")
        return False
    
    return True  # Devuelve True si el SMS fue enviado correctamente
