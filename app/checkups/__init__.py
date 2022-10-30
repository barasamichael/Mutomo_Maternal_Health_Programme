from flask import Blueprint, current_app
checkups = Blueprint('checkups', __name__)
from . import views, errors

@checkups.app_context_processor
def global_variables():
    return dict(app_name = current_app.config['ORGANISATION_NAME'])
