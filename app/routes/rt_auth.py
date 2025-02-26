from datetime import datetime, timedelta 
import secrets
from flask import Blueprint, app, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, mail 
from app.models import Usuario, UsuarioModulo, Modulo, Seccion
from app.models.md_rol import Rol


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    """
    Cerrar sesión y limpiar datos de la sesión.
    """
    logout_user()
    session.clear()  # Limpiar la sesión
    flash('Has cerrado sesión correctamente.', 'info')  # Mensaje para cerrar sesión
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
        
        login_user(usuario)

        # Obtener los módulos y secciones exclusivamente del usuario
        modulos_asignados = UsuarioModulo.query.filter_by(usuario_id=usuario.id).all()
        modulos = []

        for um in modulos_asignados:
            modulo = Modulo.query.get(um.modulo_id)
            if modulo:
                # Filtrar las secciones que pertenecen al módulo actual
                secciones = Seccion.query.filter_by(modulo_id=modulo.id).all()
                modulos.append({
                    "nombre_modulo": modulo.nombre_modulo,
                    "privilegio": um.privilegio,
                    "secciones": [{"nombre": s.nombre, "url": s.url} for s in secciones]
                })

        # Guardar información en sesión
        session['usuario_id'] = usuario.id
        session['usuario_nombre'] = usuario.nombre
        session['rol'] = usuario.rol.nombre
        session['modulos'] = modulos  # Guardar los módulos y secciones del usuario

        return redirect(url_for('main.inicio'))  
    
    if request.method == 'GET' and request.headers.get("Accept") == "application/json":
        return jsonify({"message": "Por favor, inicia sesión para continuar."}), 401
    

    return render_template('auth/login.jinja')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not nombre or not email or not password or not confirm_password:
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
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, rol_id=2)  
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada exitosamente. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.jinja')


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

        flash('Tu contraseña ha sido actualizada exitosamente.', 'success')
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
            flash('Por favor, ingresa tu número de teléfono.', 'danger')
            return render_template('auth/forgot_password_phone.jinja')

        usuario = Usuario.query.filter_by(telefono=phone).first()
        if not usuario:
            flash('No existe una cuenta registrada con ese número de teléfono.', 'danger')
            return render_template('auth/forgot_password_phone.jinja')

        # Generar un código de verificación (ejemplo: 6 dígitos aleatorios)
        verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))
        usuario.reset_token = verification_code
        usuario.reset_token_expiration = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        # Enviar el código por SMS (integrar con Twilio u otro servicio)
        flash(f'Se ha enviado un código de recuperación a tu teléfono: {phone}', 'success')

        return redirect(url_for('auth.verify_phone_code'))

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
