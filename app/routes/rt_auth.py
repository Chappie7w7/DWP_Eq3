from datetime import datetime, timedelta 
import secrets
from flask import Blueprint, Config, app, current_app, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, mail 
from app.models import Usuario, UsuarioModulo, Modulo, Seccion, PreguntaSecreta, RespuestasP, IntentosRecuperacion
from app.models.md_rol import Rol
from app.utils.email_utils import enviar_codigo_otp
from app.utils.sms_helper import enviar_codigo_sms  # Importar la función de envío de SMS


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Cerrar sesión, limpiar datos de la sesión y eliminar el token de sesión del usuario.
    """
    usuario = current_user

    # Eliminar el token de sesión del usuario en la base de datos
    usuario.token_sesion = None
    db.session.commit()

    # Cerrar sesión en Flask-Login
    logout_user()
    session.clear()  # Limpiar la sesión en Flask

    flash('Has cerrado sesión correctamente.', 'info')  # Mensaje de confirmación
    return redirect(url_for('auth.login'))  # Redirigir al login

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Validar campos vacíos
        if not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar si el usuario existe en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('El correo no está registrado.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar contraseña encriptada
        if not check_password_hash(usuario.password, password):
            flash('La contraseña es incorrecta.', 'danger')
            return redirect(url_for('auth.login'))

        # 🔹 Si el usuario ya tiene una sesión activa en otro dispositivo
        if usuario.token_sesion:
            flash('Ya tienes una sesión activa en otro dispositivo.', 'warning')

            # 🔹 Mostrar la opción de cerrar otras sesiones
            return render_template('auth/login.jinja', usuario_id=usuario.id, mostrar_cerrar_sesion=True)

        # 🔹 Generar OTP y guardarlo en la base de datos
        usuario.generar_otp()
        db.session.commit()

        # 🔹 Enviar OTP por correo
        enviar_codigo_otp(usuario.email, usuario.id, usuario.otp_code)

        flash('Hemos enviado un correo con un enlace de verificación. Revisa tu correo.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.jinja')



@auth_bp.route('/confirmar-sesion/<int:usuario_id>', methods=['POST'])
def confirmar_sesion(usuario_id):
    """Cierra la sesión anterior y permite al usuario continuar."""
    usuario = Usuario.query.get_or_404(usuario_id)

    # Cerrar la sesión anterior eliminando el token_sesion
    usuario.token_sesion = None
    db.session.commit()

    flash('Se cerraron las sesiones anteriores. Ahora puedes continuar.', 'info')
    return redirect(url_for('auth.login'))



@auth_bp.route('/verificar-otp/<int:usuario_id>/<codigo>')
def verificar_otp(usuario_id, codigo):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.otp_code != codigo or usuario.otp_expiration < datetime.now():
        flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(usuario)

    # 🔹 Limpiar OTP después de la verificación
    usuario.otp_code = None
    usuario.otp_expiration = None
    db.session.commit()

    # 🔹 Generar token JWT con expiración de 3 minutos
    expira = datetime.now() + timedelta(minutes=3)
    token = jwt.encode(
        {"usuario_id": usuario.id, "exp": int(expira.timestamp())}, 
        current_app.config['JWT_SECRET_KEY'], algorithm="HS256"
    )

    usuario.token = token
    usuario.token_sesion = token  # 🔹 Guardar token de sesión para identificar dispositivos
    db.session.commit()

    # 🔹 Cargar módulos y secciones asignados al usuario
    modulos_asignados = UsuarioModulo.query.filter_by(usuario_id=usuario.id).all()
    modulos = []

    for um in modulos_asignados:
        modulo = Modulo.query.get(um.modulo_id)
        if modulo:
            # Obtener las secciones del módulo
            secciones = Seccion.query.filter_by(modulo_id=modulo.id).all()
            modulos.append({
                "nombre_modulo": modulo.nombre_modulo,
                "privilegio": um.privilegio,
                "secciones": [{"nombre": s.nombre, "url": s.url} for s in secciones]
            })

    # 🔹 Guardar información en sesión
    session['usuario_id'] = usuario.id
    session['token'] = token
    session['usuario_nombre'] = usuario.nombre
    session['rol'] = usuario.rol.nombre
    session['modulos'] = modulos  

    flash('Código correcto. Iniciando sesión...', 'success')
    return redirect(url_for('main.inicio'))




@auth_bp.route('/cerrar-otros-dispositivos/<int:usuario_id>', methods=['POST'])
def cerrar_otros_dispositivos(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    # 🔹 Invalidar todas las sesiones anteriores eliminando el token de sesión
    usuario.token_sesion = None  
    db.session.commit()

    flash('Se han cerrado todas las sesiones anteriores. Continúa con tu nueva sesión.', 'success')

    # 🔹 Generar OTP y enviarlo nuevamente
    usuario.generar_otp()
    db.session.commit()

    # 🔹 Enviar OTP por correo
    enviar_codigo_otp(usuario.email, usuario.id, usuario.otp_code)

    flash('Hemos enviado un nuevo código de verificación a tu correo.', 'info')

    # 🔹 Redirigir al login para que pueda continuar con la nueva sesión
    return redirect(url_for('auth.login'))



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        num_tel = request.form.get('telefono')
        pregunta1_id = request.form.get('selecPregunta1')
        respuesta1 = request.form.get('respuesta1')
        pregunta2_id = request.form.get('selecPregunta2')
        respuesta2 = request.form.get('respuesta2')

        if not nombre or not email or not password or not confirm_password or not num_tel or not pregunta1_id or not respuesta1 or not pregunta2_id or not respuesta2:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('auth.register'))

        # Verificar si el usuario ya existe
        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        # Crear un nuevo usuario
        hashed_password = generate_password_hash(password, method='scrypt')
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, rol_id=2, telefono=num_tel)  
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        #resp_hash1 = generate_password_hash(respuesta1, method='scrypt')
        #resp_hash2 = generate_password_hash(respuesta2, method='scrypt')

        respuesta1_db = RespuestasP(usuario_id=nuevo_usuario.id, pregunta_id=pregunta1_id, respuesta_hash=respuesta1)
        respuesta2_db = RespuestasP(usuario_id=nuevo_usuario.id, pregunta_id=pregunta2_id, respuesta_hash=respuesta2)

        db.session.add(respuesta1_db)
        db.session.add(respuesta2_db)
        db.session.commit()

        flash('Cuenta creada exitosamente. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    # Obtener todas las preguntas desde la base de datos
    preguntas = PreguntaSecreta.query.all()

    # Dividir las preguntas en dos mitades
    mitad = len(preguntas) // 2
    preguntas_1 = preguntas[:mitad]
    preguntas_2 = preguntas[mitad:]

    return render_template('auth/register.jinja', preguntas_1=preguntas_1, preguntas_2=preguntas_2)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        if not email:
            flash('Por favor, ingresa tu correo electrónico.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('No existe una cuenta registrada con ese correo.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        # Generar token de recuperación
        usuario.reset_token = secrets.token_hex(16)
        usuario.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        reset_link = url_for('auth.reset_password', token=usuario.reset_token, _external=True)

        try:
            msg = Message(
                'Recuperación de contraseña',
                sender='desarrollopractica0@gmail.com',  
                recipients=[email],
                body=f'Hola {usuario.nombre},\n\nPara restablecer tu contraseña, haz clic en el siguiente enlace: {reset_link}\n\nSi no solicitaste este cambio, ignora este mensaje.'
            )
            mail.send(msg)  
            flash('Se ha enviado un correo con las instrucciones para restablecer tu contraseña.', 'success')
        except Exception as e:
            flash(f'Hubo un problema al enviar el correo: {e}', 'danger')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.jinja')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    usuario = Usuario.query.filter_by(reset_token=token).first()

    # Verificar si el token es válido
    if not usuario or usuario.reset_token_expiration < datetime.utcnow():
        flash('El enlace para restablecer la contraseña ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        # Actualizar la contraseña y eliminar el token
        usuario.set_password(password)
        usuario.reset_token = None
        usuario.reset_token_expiration = None
        db.session.commit()

        flash('Tu contraseña ha sido actualizada exitosamente felicidades.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.jinja', token=token)

@auth_bp.route('/auth/check-email', methods=['POST'])
def check_email():
    """Verifica si el correo ya está registrado"""
    data = request.get_json()
    email = data.get('email')

    if not email or '@' not in email:
        return jsonify({'error': 'Correo inválido'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    return jsonify({'exists': bool(usuario)}), 200 if usuario else 404
    

#ruta para recupercion con telefono
@auth_bp.route('/forgot-password-phone', methods=['GET', 'POST'])
def forgot_password_phone():
    if request.method == 'POST':
        phone = request.form.get('phone')

        if not phone:
            flash('Por favor, ingresa tu número de teléfono personal.', 'danger')
            return render_template('auth/forgot_password_phone.jinja')

        usuario = Usuario.query.filter_by(telefono=phone).first()
        if not usuario:
            flash('No existe una cuenta registrada con ese número de teléfono.', 'danger')
            return render_template('auth/forgot_password_phone.jinja')

        # Generar código de verificación
        verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))

        try:
            usuario.reset_token = verification_code
            usuario.reset_token_expiration = datetime.utcnow() + timedelta(minutes=2)
            db.session.commit()

            # Aquí aseguramos que estamos usando la función con ClickSend
            if enviar_codigo_sms(phone, verification_code):
                flash(f'Se ha enviado un código de recuperación a tu teléfono: {phone}', 'success')
                return redirect(url_for('auth.verify_phone_code'))
            else:
                flash('Error al enviar el SMS. Inténtalo nuevamente.', 'danger')

        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar el código de verificación: {str(e)}', 'danger')

    return render_template('auth/forgot_password_phone.jinja')




@auth_bp.route('/verify-phone-code', methods=['GET', 'POST'])
def verify_phone_code():
    if request.method == 'POST':
        phone = request.form.get('phone')
        code = request.form.get('code')

        usuario = Usuario.query.filter_by(telefono=phone).first()

        if not usuario:
            flash('No existe una cuenta registrada con ese número de teléfono.', 'danger')
            return redirect(url_for('auth.forgot_password_phone'))

        if usuario.reset_token != code or usuario.reset_token_expiration < datetime.utcnow():
            flash('Código inválido o expirado.', 'danger')
            return render_template('auth/verify_phone_code.jinja')

        # Redirigir a la página para cambiar la contraseña
        return redirect(url_for('auth.reset_password_phone', phone=usuario.telefono))

    return render_template('auth/verify_phone_code.jinja')



@auth_bp.route('/reset-password-phone/<phone>', methods=['GET', 'POST'])
def reset_password_phone(phone):
    usuario = Usuario.query.filter_by(telefono=phone).first()

    if not usuario:
        flash('Hubo un error, intenta nuevamente.', 'danger')
        return redirect(url_for('auth.forgot_password_phone'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.reset_password_phone', phone=phone))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return redirect(url_for('auth.reset_password_phone', phone=phone))

        # Actualizar la contraseña y eliminar el código de verificación
        usuario.set_password(password)
        usuario.reset_token = None
        usuario.reset_token_expiration = None
        db.session.commit()

        flash('Tu contraseña ha sido actualizada exitosamente.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_phone.jinja', phone=phone)

@auth_bp.route('/forgot-password-questions', methods=['GET', 'POST'])
def forgot_password_questions():
    if request.method == 'POST':
        email = request.form.get('preguntas')

        if not email:
            flash('Por favor, ingresa tu correo electrónico.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('No existe una cuenta registrada con ese correo.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        preguntas = PreguntaSecreta.query.join(RespuestasP).filter(RespuestasP.usuario_id == usuario.id).all()
        if len(preguntas) < 2:
            flash('Este usuario no tiene preguntas de seguridad configuradas.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        mit = len(preguntas) // 2
        pregunta_1 = preguntas[:mit]
        pregunta_2 = preguntas[mit:]
        
        session['reset_email'] = email
        return render_template('auth/forgot_password_questions.jinja', pregunta_1=pregunta_1, pregunta_2=pregunta_2)
        
    return render_template('auth/forgot_password_questions.jinja')


@auth_bp.route('/validate-security-questions', methods=['POST'])
def validate_security_questions():
    if request.method == 'POST':
        email = session.get('reset_email')
        respuesta1 = request.form.get('respuesta1')
        respuesta2 = request.form.get('respuesta2')
        usuario = Usuario.query.filter_by(email=email).first()
    
        if not usuario:
            flash('No existe una cuenta registrada con ese correo.', 'danger')
            return redirect(url_for('auth.forgot_password_questions'))
    
        intentos = IntentosRecuperacion.query.filter_by(usuario_id=usuario.id).first()
        # Si hay intentos registrados y han pasado más de 1 minuto, eliminamos el registro
        if intentos and datetime.utcnow() >= intentos.ultimo_intento + timedelta(minutes=1):
            db.session.delete(intentos)
            db.session.commit()
            intentos = None

        if intentos and intentos.intentos >= 3:
            flash('Demasiados intentos fallidos. Espera 1 minuto.', 'danger')
            return redirect(url_for('auth.forgot_password'))
    
        preguntas_2 = PreguntaSecreta.query.join(RespuestasP).filter(RespuestasP.usuario_id == usuario.id).all()
        mita = len(preguntas_2) // 2
        pregunta_1 = preguntas_2[:mita]
        pregunta_2 = preguntas_2[mita:]
        preguntas = RespuestasP.query.join(PreguntaSecreta).filter(RespuestasP.usuario_id == usuario.id).all()
        respuestas = [respuesta1, respuesta2]

        if not respuesta1 or not respuesta2:
            flash('Debes responder ambas preguntas.', 'danger')
            return render_template('auth/forgot_password_questions.jinja', pregunta_1=pregunta_1, pregunta_2=pregunta_2)

        if len(respuestas) != len(preguntas):
            flash('Respuestas inválidas.', 'danger')
            return render_template('auth/forgot_password_questions.jinja', pregunta_1=pregunta_1, pregunta_2=pregunta_2)
    
        #correctas = all(check_password_hash(pregunta.respuesta_hash, respuesta) for pregunta, respuesta in zip(preguntas, respuestas))
        correctas = all(pregunta.respuesta_hash == respuesta for pregunta, respuesta in zip(preguntas, respuestas))
    
        if correctas:
            if intentos:
                db.session.delete(intentos)
                usuario.reset_token = secrets.token_hex(16)
                usuario.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
                db.session.commit()
                flash('Respuestas correctas. Restablezca su contraseña.', 'success')
                return render_template('auth/reset_password.jinja', token=usuario.reset_token)
        else:
            if not intentos:
                intentos = IntentosRecuperacion(usuario_id=usuario.id, intentos=1, ultimo_intento=datetime.utcnow())
                db.session.add(intentos)
                db.session.commit()
                flash('Respuestas incorrectas. Inténtalo de nuevo.', 'danger')
                return render_template('auth/forgot_password_questions.jinja', pregunta_1=pregunta_1, pregunta_2=pregunta_2)
            else:
                intentos.intentos += 1
                intentos.ultimo_intento = datetime.utcnow()
                db.session.commit()
                flash('Respuestas incorrectas. Inténtalo de nuevo.', 'danger')
                return render_template('auth/forgot_password_questions.jinja', pregunta_1=pregunta_1, pregunta_2=pregunta_2)

    usuario.reset_token = secrets.token_hex(16)
    usuario.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    flash('Respuestas correctas. Restablezca su contraseña.', 'success')
    return render_template('auth/reset_password.jinja', token=usuario.reset_token)