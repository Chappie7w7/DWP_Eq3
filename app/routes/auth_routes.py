from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    
    return redirect(url_for('auth.login'))

# Expresión regular para validar correos
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        # Validar si los campos están vacíos
        if not email or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('auth/login.jinja')

        # Verificar las credenciales del usuario
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.password == password:
            return redirect(url_for('main.inicio'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('auth/login.jinja')

    return render_template('auth/login.jinja')
