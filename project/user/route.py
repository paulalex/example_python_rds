"""
User feature routing for routes related to the user part of the application,
defines and exports the user blueprint (see ../__init__.py)
"""
from flask import Flask, Blueprint
from flask import render_template

from . import service

mod_user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


@mod_user.route('/list', methods=['GET'])
def all_users_view():
    """Route handler for /list userlist"""
    all_users = service.fetch_all_users()

    return render_template('users.html', users=all_users, title="Show Users")


@mod_user.route('/create', methods=['POST'])
def create():
    """Route handler for /create user creation"""
    service.create_user()

    all_users = service.fetch_all_users()

    return render_template('users.html', users=all_users, title="Show Users")


@mod_user.route('/read', methods=['GET'])
def read():
    """Route handler for /read to get a user record in json format"""
    return service.read_user()


@mod_user.route('/update', methods=['PUT'])
def update():
    """Route handler for /update unimplemented database function"""
    return service.update_user()


@mod_user.route('/delete', methods=['POST', 'GET'])
def delete():
    """Route handler for /delete to delete a user from the database"""
    service.delete_user()

    all_users = service.fetch_all_users()

    return render_template('users.html', users=all_users, title="Show Users")


@mod_user.route('/add_user', methods=['GET'])
def add_user_view():
    """Route handler for /add_user view"""
    return render_template('add_user.html', title="Add Users")


@mod_user.route('/delete_user', methods=['GET'])
def delete_user_view():
    """Route handler for /delete_user user view"""
    return render_template('delete_user.html', title="Delete Users")



