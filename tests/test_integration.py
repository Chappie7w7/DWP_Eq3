# test_integration.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app as App

@pytest.fixture
def app():
    application = App()
    application.testing = True
    return application

def test_customer_count(app):
    # placeholder temporal
    assert True

def test_existence_of_customer(app):
    assert True
