from flask import Blueprint, redirect, render_template, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    # Aquí puedes agregar lógica para limpiar sesiones si es necesario
    return redirect(url_for('auth.login'))

@auth_bp.route('/login')
def login():
    return render_template('auth/login.jinja')  # Asegúrate de que esta plantilla exista
