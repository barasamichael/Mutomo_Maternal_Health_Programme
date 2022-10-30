from flask import render_template
from . import checkups


@checkups.app_errorhandler(403)
def forbidden(e):
    return render_template('checkups/403.html'), 403


@checkups.app_errorhandler(404)
def page_not_found(e):
    return render_template('checkups/404.html'), 404


@checkups.app_errorhandler(500)
def internal_server_error(e):
    return render_template('checkups/500.html'), 500
