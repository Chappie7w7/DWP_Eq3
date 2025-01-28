from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from app.models.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    # Limpia la sesión del usuario
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))

# Expresión regular para validar correos
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Validar campos vacíos
        if not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar si el correo existe
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('El correo no está registrado.', 'danger')
            return redirect(url_for('auth.login'))

        # Verificar contraseña
        if usuario.password != password:
            flash('La contraseña es incorrecta.', 'danger')
            return redirect(url_for('auth.login'))

        # Si todo es válido, guarda el nombre del usuario en la sesión
        session['usuario_nombre'] = usuario.nombre
        return redirect(url_for('main.inicio'))

    return render_template('auth/login.jinja')


@auth_bp.route('/auth/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'El correo es obligatorio'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return jsonify({'exists': True}), 200
    else:
        return jsonify({'exists': False}), 404
