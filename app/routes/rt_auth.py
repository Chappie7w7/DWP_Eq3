from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import db  
from app.models import Usuario, UsuarioModulo, Modulo, Seccion
from app.models.md_rol import Rol


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/logout')
def logout():
    """
    Cerrar sesión y limpiar datos de la sesión.
    """
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

        # Obtener los módulos y secciones exclusivamente del usuario
        modulos_asignados = UsuarioModulo.query.filter_by(usuario_id=usuario.id).all()
        modulos = []

        for um in modulos_asignados:
            modulo = Modulo.query.get(um.modulo_id)
            if modulo:
                # Filtrar las secciones que pertenecen al módulo actual
                secciones = Seccion.query.filter_by(modulo_id=modulo.id).all()
                modulos.append({
                    "nombre": modulo.nombre,
                    "privilegio": um.privilegio,
                    "secciones": [{"nombre": s.nombre, "url": s.url} for s in secciones]
                })

        # Guardar información en sesión
        session['usuario_id'] = usuario.id
        session['usuario_nombre'] = usuario.nombre
        session['rol'] = usuario.rol.nombre
        session['modulos'] = modulos  # Guardar los módulos y secciones del usuario

        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('main.inicio'))  # Redirigir al dashboard o página principal

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
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, rol_id=2)  # Asignar rol por defecto
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada exitosamente. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.jinja')



@auth_bp.route('/auth/check-email', methods=['POST'])
def check_email():
    """Verifica si el correo ya está registrado"""
    data = request.get_json()
    email = data.get('email')

    if not email or '@' not in email:
        return jsonify({'error': 'Correo inválido'}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    return jsonify({'exists': bool(usuario)}), 200 if usuario else 404
