import flask
from flask_login import login_required
from . import profiles
from .. import db

from ..models import (Permission, patient, health_center, health_center_type)


@profiles.route('/view_health_center_types')
def view_health_center_types():
    page = flask.request.args.get('page', 1, type = int)
    pagination = health_center_type.query.order_by(
            health_center_type.title.desc()\
                    ).paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
                            error_out = False)
    center_types = pagination.items

    return flask.render_template('profiles/view_health_center_types.html',
            center_types = center_types, pagination = pagination)


@profiles.route('/view_health_centers')
def view_health_centers():
    page = flask.request.args.get('page', 1, type = int)
    pagination = health_center.query.order_by(health_center.hc_type_id.desc())\
            .join(health_center_type, 
                    health_center_type.hc_type_id == health_center.hc_type_id)\
            .add_columns(
                    health_center.health_center_id,
                    health_center.title,
                    health_center.location_address,
                    health_center.email_address,
                    health_center_type.hc_type_id,
                    health_center_type.title.label('type')
                ).order_by(health_center.hc_type_id.desc())\
                        .paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
                                error_out = False)
    centers = pagination.items

    return flask.render_template('profiles/view_health_centers.html', centers = centers, 
            pagination = pagination)


@profiles.route('/list_of_patients')
def list_of_patients():
    page = flask.request.args.get('page', 1, type = int)
    pagination = patient.query.order_by(patient.patient_id.desc()).paginate(page, 
            flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
            error_out = False)
    patients = pagination.items

    return flask.render_template('profiles/list_of_patients.html', patients = patients, 
            pagination = pagination)


@profiles.route('/personal/<int:patient_id>')
def personal(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/patient_profile/<int:patient_id>', methods = ['GET', 'POST'])
def patient_profile(patient_id):
    Patient = patient.query.filter_by(patient_id = patient_id).first_or_404()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    #personal details
    if tab_variable == 0:
        return flask.render_template('profiles/patient_profile.html', patient = Patient)
    

    return flask.render_template('profiles/patient_profile.html', patient = Patient)

