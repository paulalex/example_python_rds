"""
Error handler page routing for 404 and 500 errors and
defines and exports the error blueprint (see ../__init__.py)
"""
import traceback

from flask import Flask, render_template, request, Blueprint, send_from_directory
from flask import current_app as app

mod_error = Blueprint('error', __name__, template_folder='templates')


@app.errorhandler(404)
def not_found(e):
    """Error handler for 404 page not found errors"""
    print(e)
    return render_template('404.html')


@app.errorhandler(500)
def general_exception(e):
    """Error handler for 500 internal server errors"""
    print(e)
    print(traceback.format_exc())
    return render_template('error.html')

