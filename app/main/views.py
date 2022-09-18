import flask
from flask_login import login_required
from . import main
from .. import db

from ..models import (Permission)


@main.route('/')
@main.route('/home')
@main.route('/homepage')
def homepage():
    return flask.render_template('main/homepage.html')


@main.route('/contact_us')
def contact_us():
    return flask.render_template('main/contact_us.html')
