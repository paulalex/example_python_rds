"""
Index page routing for default url context and /index
defines and exports the index blueprint (see ../__init__.py)
"""
from flask import Flask, render_template, Blueprint
from flask import current_app as app

mod_index = Blueprint('index', __name__, template_folder='templates')


@app.route('/')
def index():
    """Route handler for /"""
    return render_template('index.html')


@app.route('/index')
def home():
    """Route handler for /index"""
    return render_template('index.html')
