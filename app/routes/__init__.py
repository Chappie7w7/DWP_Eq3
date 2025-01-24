from flask import Blueprint, render_template

index_bp = Blueprint('IndexRoute', __name__)


@index_bp.get('/')
def index():
    return render_template('index.jinja2')
