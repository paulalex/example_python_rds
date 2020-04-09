"""
Configuration class that is fed to the init script (__init__.py) in this
directory to bootstrap the application
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "secret"

ENVIRONMENT = os.getenv('ENVIRONMENT')

SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_URL = os.getenv('DATABASE_URL')

DATABASE_ENGINE = os.getenv('DATABASE_ENGINE')

DATABASE_PORT = os.getenv('DATABASE_PORT')

DATABASE_USER = os.getenv('DATABASE_USER')

DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

DATABASE_PORT = os.getenv('DATABASE_PORT')

DATABASE_NAME = os.getenv('DATABASE_NAME')
