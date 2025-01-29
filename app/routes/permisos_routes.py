from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario_modulo import UsuarioModulo
from app.models.usuario import Usuario
from app.models.modulo import Modulo
from app import db

permisos_bp = Blueprint('permisos', __name__, url_prefix='/permisos')
