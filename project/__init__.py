"""
This script intitialises the application, sets up the blueprints and
create the flask application and context
"""
#  Import standard modules
import os

# Import Third party modules
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def get_database_url(app):
    print(f'[INFO] Database Environment: {os.environ.get("ENVIRONMENT")}')
    if os.environ.get('USE_DEV_ENV') is None and (os.environ.get('ENVIRONMENT') == 'JENKINS'
                                                  or os.environ.get('ENVIRONMENT') == 'LOCAL'):
        database_endpoint = f"sqlite:///{os.path.join(app.config['BASE_DIR'], 'data.sqlite')}"
    else:
        engine = app.config['DATABASE_ENGINE']
        user = app.config['DATABASE_USER']
        password = app.config['DATABASE_PASSWORD']
        url = app.config['DATABASE_URL']
        port = app.config['DATABASE_PORT']
        db_name = app.config['DATABASE_NAME']

        database_endpoint = f"{engine}://{user}:{password}@{url}:{port}/{db_name}"

    return database_endpoint


def create_app():
    # Load any environment files
    app_root = os.path.join(os.path.dirname(__file__), '..')

    if os.environ.get('USE_DEV_ENV') is not None:
        dotenv_path = os.path.join(app_root, 'dev.env')
        load_dotenv(dotenv_path, verbose=True)

    # Define the WSGI application object
    app = Flask(__name__)

    # Push the app into the application context
    # so it can be used throughout the application
    app.app_context().push()

    # Run init routines
    init_config(app)

    db.init_app(app)

    Migrate(app, db)

    register_blueprints(app)

    return app


def register_blueprints(app):
    # Import local feature modules using blueprint handler
    from .user.route import mod_user as user_module
    from .route.error_handler import mod_error as error_module
    from .route.index import mod_index as index_module

    # Register blueprints
    app.register_blueprint(index_module)
    app.register_blueprint(user_module)
    app.register_blueprint(error_module)


def init_config(app):
    # Load Configuration
    app.config.from_object('config')

    # Register database
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url(app)


def create_db():
    # Create database tables from models if they do not exist
    print(f'[INFO] INITIALISING DATABASE')
    db.create_all()


