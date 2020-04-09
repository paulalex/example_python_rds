"""
Service that handles business logic related to the
user feature
"""
import json
from datetime import datetime as dt

from flask import request, render_template, make_response
from flask import abort

from .model import User
from project import db


def create_user():
    """Create a user."""
    username = request.form.get('username')
    email = request.form.get('email')

    if username and email:
        new_user = User(username=username,
                        email=email,
                        created=dt.now(),
                        admin=False)

        # Adds new User record to database
        db.session.add(new_user)

        # Commits all changes
        db.session.commit()

    return make_response(f"{new_user} successfully created!")


def read_user():
    """Read a user"""
    username = request.args.get('username')
    email = request.args.get('email')
    existing_user = User.query.filter(User.username == username, User.email == email).first()

    # Create json object to respond with
    if existing_user:
        user_dict = {
            'username': existing_user.username,
            'email': existing_user.email
        }

        return json.dumps(user_dict)
    else:
        abort(404)


def update_user():
    """Method not implemented"""
    # Not implemented
    abort(501)


def delete_user():
    """Delete a user."""
    username = request.form.get('username')
    print(f"username: {username}")
    if username:
        # Retrieve the user
        remove_user = User.query.filter_by(username=username).first()

        # Removes an existing user record from the database
        db.session.delete(remove_user)

        # Commits all changes
        db.session.commit()


def fetch_all_users():
    """Fetch all users"""
    all_users = User.query.all()

    return all_users
