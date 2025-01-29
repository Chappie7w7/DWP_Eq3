from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from app.models import Usuario, UsuarioModulo, Modulo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión y limpiar datos de la sesión"""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Validar campos vacíos
        if not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.login'))

        # Validar formato del correo 
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash('Por favor, ingrese un correo válido.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar si el usuario existe en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('El correo no está registrado.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar contraseña
        if usuario.password != password:
            flash('La contraseña es incorrecta.', 'danger')
            return redirect(url_for('auth.login'))

        # Obtener módulos permitidos para el usuario desde la base de datos
        modulos_asignados = UsuarioModulo.query.filter_by(usuario_id=usuario.id).all()
        modulos = [modulo.modulo.nombre for modulo in modulos_asignados]

        # Guardar información en sesión
        session['usuario_id'] = usuario.id
        session['usuario_nombre'] = usuario.nombre
        session['modulos'] = modulos  # Lista con los módulos a los que tiene acceso

        return redirect(url_for('main.inicio'))

    # Para solicitudes GET, devuelve el formulario de inicio de sesión
    return render_template('auth/login.jinja')


@auth_bp.route('/auth/check-email', methods=['POST'])
def check_email():
    """Verifica si el correo ya está registrado"""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'El correo es obligatorio'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    return jsonify({'exists': bool(usuario)}), 200 if usuario else 404
