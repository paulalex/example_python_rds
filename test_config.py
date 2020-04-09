"""
Configuration file for integration tests
"""
from datetime import datetime as dt

import pytest

from project.user.model import User
from project import db, create_app

flask_app = create_app()


@pytest.fixture(scope='module')
def non_admin_user():
    user = User('Test User', 'test_user@gmail.com', '2019-11-07 23:37:57.373846', False)
    return user


@pytest.fixture(scope='module')
def admin_user():
    user = User('Test User Admin', 'test_user_admin@gmail.com', '2019-11-07 23:38:57.373846', True)
    return user


@pytest.fixture(scope='module')
def test_client():
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    print("[INFO] Creating database as part of test run")
    # Create the database and the database table

    db.create_all()

    # Insert user data
    user_admin = User('test_user_admin', 'test_user_admin@gmail.com', dt.now(), True)
    user = User('test_user', 'test_user@gmail.com', dt.now(), False)

    db.session.add(user_admin)
    db.session.add(user)

    # Commit the changes for the users
    db.session.commit()

    yield db

    db.drop_all()


