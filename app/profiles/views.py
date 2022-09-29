import flask
from flask_login import login_required
from . import profiles
from .. import db

from ..models import (Permission, patient, health_center, health_center_type,
        health_center_department, health_practitioner, health_practitioner_type)


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


@profiles.route('/view_health_practitioner_types')
def view_health_practitioner_types():
    page = flask.request.args.get('page', 1, type = int)
    pagination = health_practitioner_type.query.order_by(health_practitioner_type.title.desc())\
            .paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
    specialities = pagination.items

    return flask.render_template('profiles/view_health_practitioner_types.html', 
            specialities = specialities, pagination = pagination)


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


@profiles.route('/list_of_health_practitioners')
def list_of_health_practitioners():
    page = flask.request.args.get('page', 1, type = int)
    
    pagination = health_practitioner.query\
        .join(health_practitioner_type, 
                health_practitioner_type.hp_type_id == health_practitioner.hp_type_id)\
        .join(health_center_department, 
                health_center_department.hc_department_id == health_practitioner.department_id)\
        .join(health_center, 
                health_center.health_center_id == health_center_department.health_center_id)\
        .add_columns(
                health_practitioner.health_practitioner_id,
                health_practitioner.practitioner_id,
                health_practitioner.first_name,
                health_practitioner.middle_name,
                health_practitioner.last_name,
                health_practitioner.gender,
                health_practitioner.email_address,
                health_practitioner_type.hp_type_id,
                health_practitioner_type.title,
                health_center.health_center_id,
                health_center.title.label('health_center'),
                health_center_department.hc_department_id,
                health_center_department.title.label('department')
            ).order_by(health_practitioner.health_practitioner_id).paginate(page,
                    flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
    practitioners = pagination.items

    return flask.render_template('profiles/list_of_health_practitioners.html', 
            pagination = pagination, practitioners = practitioners)


@profiles.route('/health_practitioner_personal/<int:health_practitioner_id>')
def health_practitioner_personal(health_practitioner_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.health_practitioner_profile', 
                health_practitioner_id = health_practitioner_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/health_practitioner_profile/<int:health_practitioner_id>', 
        methods = ['GET', 'POST'])
def health_practitioner_profile(health_practitioner_id):
    Practitioner = health_practitioner.query.filter_by(
            health_practitioner_id = health_practitioner_id).first_or_404()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = flask.request.cookies.get('tab_var')

    #personal details
    if tab_variable == 0:
        return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)
    
    return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)


@profiles.route('/departments/<int:health_center_id>')
def departments(health_center_id):
    response = flask.make_response(
        flask.redirect(
            flask.url_for('profiles.health_center_profile', health_center_id = health_center_id)))
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/health_center_profile/<int:health_center_id>', 
        methods = ['GET', 'POST'])
def health_center_profile(health_center_id):
    Health_Center = health_center.query.filter_by(health_center_id = health_center_id)\
            .join(health_center_type, health_center_type.hc_type_id == health_center.hc_type_id)\
            .add_columns(
                    health_center.health_center_id,
                    health_center.title,
                    health_center.location_address,
                    health_center.email_address,
                    health_center.associated_image,
                    health_center.x_coordinate,
                    health_center.y_coordinate,
                    health_center.active,
                    health_center_type.hc_type_id,
                    health_center_type.title.label('type')
                ).first_or_404()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    #personal details
    if tab_variable == 0:
        page = flask.request.args.get('page', 1, type = int)
        pagination = health_center_department.query.filter_by(
            health_center_id = health_center_id).paginate(page, 
                flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
        departments = pagination.items

        return flask.render_template('profiles/health_center_profile.html', 
            departments = departments, center = Health_Center, tab_variable = tab_variable)
    
    return flask.render_template('profiles/health_center_profile.html', 
            center = Health_Center, tab_variable = tab_variable)


@profiles.route('/department_schedule/<int:hc_department_id>')
def department_schedule(hc_department_id):
    response = flask.make_response(
        flask.redirect(
            flask.url_for('profiles.center_department', hc_department_id = hc_department_id)))
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response

@profiles.route('/department_practitioners/<int:hc_department_id>')
def department_practitioners(hc_department_id):
    response = flask.make_response(
        flask.redirect(
            flask.url_for('profiles.center_department', hc_department_id = hc_department_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/center_department/<int:hc_department_id>', 
        methods = ['GET', 'POST'])
def center_department(hc_department_id):
    Department = health_center_department.query\
        .filter_by(hc_department_id = hc_department_id).join(health_center, 
        health_center.health_center_id == health_center_department.health_center_id)\
                .add_columns(
                        health_center_department.hc_department_id,
                        health_center_department.title,
                        health_center_department.description,
                        health_center_department.associated_image,
                        health_center_department.date_created,
                        health_center_department.last_updated,
                        health_center.health_center_id,
                        health_center.title.label('health_center')
                ).first_or_404()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    #personal details
    if tab_variable == 0:
        return flask.render_template('profiles/center_department.html', 
            department = Department, tab_variable = tab_variable)
    
    #department health practitioners
    if tab_variable == 1:
        page = flask.request.args.get('page', 1, type = int)
        pagination = health_practitioner.query\
            .filter_by(department_id = Department.hc_department_id)\
            .join(health_practitioner_type,
                    health_practitioner_type.hp_type_id == health_practitioner.hp_type_id)\
            .add_columns(
                    health_practitioner.health_practitioner_id,
                    health_practitioner.first_name,
                    health_practitioner.middle_name,
                    health_practitioner.last_name,
                    health_practitioner.gender,
                    health_practitioner.email_address,
                    health_practitioner.practitioner_id,
                    health_practitioner_type.hp_type_id,
                    health_practitioner_type.title,
                    ).order_by(health_practitioner.health_practitioner_id).paginate(page, 
                            flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
        practitioners = pagination.items

        return flask.render_template('profiles/center_department.html', 
            practitioners = practitioners, department = Department, 
            tab_variable = tab_variable)
    
    return flask.render_template('profiles/center_department.html', 
            department = Department, tab_variable = tab_variable)
