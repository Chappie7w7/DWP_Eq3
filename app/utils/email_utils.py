from flask_mail import Message
from app import mail

def enviar_codigo_otp(email, usuario_id, codigo):
    # Generar el enlace con el ID 
    enlace = f"http://127.0.0.1:5000/auth/verificar-otp/{usuario_id}/{codigo}"

    msg = Message("Confirmación de inicio de sesión", 
                  recipients=[email])
    msg.body = f"Hola, haz clic en el siguiente enlace para confirmar tu inicio de sesión:\n\n{enlace}\n\nEste enlace expirará en 2 minutos."
    
    mail.send(msg)
