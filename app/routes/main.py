from flask import Blueprint, render_template


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('dashboard/index.jinja')

@main_bp.route('/inicio')
def inicio():
    return render_template('dashboard/home.jinja')

@main_bp.route('/josue')
def josue():
    return render_template('josue/josue.jinja')

# Error 404
@main_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('josue/error.jinja'), 404
