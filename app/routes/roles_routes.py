from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.rol import Rol
from app.models.modulo import Modulo
from app.models.usuario import Usuario
from app.models.usuario_modulo import UsuarioModulo
from app import db

roles_bp = Blueprint('roles', __name__, url_prefix='/roles')

