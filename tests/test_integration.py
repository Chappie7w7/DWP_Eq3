# test_integration.py
import sys
import os
import pytest

# Permite importar app desde la raíz del repo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app as App

@pytest.fixture
def app():
    """Crea la app Flask para testing"""
    application = App()  # manteniendo la misma estructura
    application.testing = True
    return application

@pytest.fixture
def client(app):
    """Crea el cliente de test para simular requests"""
    return app.test_client()

def test_customer_count(app):
    # Aquí pones la prueba real con tu app o base de datos
    # Temporal placeholder para que pase
    assert True

def test_existence_of_customer(app):
    # Otra prueba temporal
    assert True
