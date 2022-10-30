import flask
from datetime import datetime
from flask_login import login_required
from . import profiles
from .. import db
from .forms import (RegisterAllergyForm, RegisterSymptomForm)

from ..models import (Permission, patient, health_center, health_center_type,
        health_center_department, health_practitioner, health_practitioner_type, 
        patient_phone_no, health_practitioner_phone_no, pregnancy, checkup,
        hc_contact, allergy, allergy_symptom, social_history, medication_history, 
        miscarriage, surgery)


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


@profiles.route('/pregnancies/<int:patient_id>')
def pregnancies(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '3', max_age = 60*60)
    return response


@profiles.route('/history/<int:patient_id>')
def history(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '2', max_age = 60*60)
    return response


@profiles.route('/medical/<int:patient_id>')
def medical(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@profiles.route('/personal/<int:patient_id>')
def personal(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/patient_profile/<int:patient_id>', methods = ['GET', 'POST'])
def patient_profile(patient_id):
    Patient = patient.query.filter_by(patient_id = patient_id).first_or_404()

    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    #personal details
    if tab_variable == 0:
        phone_numbers = patient_phone_no.query.filter_by(patient_id = patient_id).all()
        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                tab_variable = tab_variable, phone_numbers = phone_numbers)
    
    #medical history details
    if tab_variable == 1:
        #---------------------------------------------------------#
        #                       ALLERGIES                         #
        #---------------------------------------------------------#

        allergy_form = RegisterAllergyForm()
        if flask.request.method == 'POST' and allergy_form.validate_on_submit():
            Allergy = allergy(
                    description = allergy_form.description.data,
                    cause = allergy_form.cause.data,
                    remedy = allergy_form.remedy.data,
                    patient_id = patient_id)
            
            db.session.add(Allergy)
            db.session.commit()
            flask.flash('Allergy added successfully.')

            return flask.redirect(flask.url_for('profiles.medical', patient_id = patient_id))

        allergies = allergy.query.filter_by(patient_id = patient_id)\
                .order_by(allergy.description.asc()).all()

        #get symptoms for each allergy and store it in a dictionary
        symptoms = {}
        for _allergy in allergies:
            allergy_symptoms = allergy_symptom.query.filter_by(allergy_id = _allergy.allergy_id).all()
            symptoms.update({_allergy.allergy_id: allergy_symptoms})

        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                allergies = allergies, symptoms = symptoms, allergy_form = allergy_form,
                tab_variable = tab_variable)
    
    #other details
    if tab_variable == 2:
        return flask.render_template('profiles/patient_profile.html', patient = Patient, 
                tab_variable = tab_variable)
    
    #pregnancies details
    if tab_variable == 3:
        pregnancies = pregnancy.query.filter_by(patient_id = patient_id).all()

        #conversion of string dates to datetime objects
        #allows easy working with moment.js
        dates = {}

        for item in pregnancies:
            conception_date = datetime.strptime(str(item.conception_date), '%Y-%m-%d')
            due_date = datetime.strptime(str(item.due_date), '%Y-%m-%d')

            dates.update({item.pregnancy_id : [conception_date, due_date]})
        
        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                tab_variable = tab_variable, pregnancies = pregnancies, dates = dates)

    return flask.render_template('profiles/patient_profile.html', patient = Patient)


@profiles.route('/allergy_profile/<int:allergy_id>', methods = ['GET', 'POST'])
def allergy_profile(allergy_id):
    Allergy = allergy.query.filter_by(allergy_id = allergy_id)\
            .join(patient, patient.patient_id == allergy.patient_id)\
            .add_columns(
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    allergy.allergy_id,
                    allergy.description,
                    allergy.cause,
                    allergy.remedy
                ).first_or_404()

    symptoms = allergy_symptom.query.filter_by(allergy_id = allergy_id)\
            .order_by(allergy_symptom.description.desc()).all()

    allergy_form = RegisterAllergyForm()
    if flask.request.method == 'POST' and allergy_form.validate_on_submit():
        Allergy = allergy.query.filter_by(allergy_id = allergy_id).first_or_404()

        Allergy.description = allergy_form.description.data
        Allergy.cause = allergy_form.cause.data
        Allergy.remedy= allergy_form.remedy.data
        
        db.session.add(Allergy)
        db.session.commit()
        
        flask.flash('Update successfull')
        return flask.redirect(flask.url_for('profiles.allergy_profile', allergy_id = allergy_id))

    allergy_form.description.data = Allergy.description
    allergy_form.cause.data = Allergy.cause
    allergy_form.remedy.data = Allergy.remedy

    symptom_form = RegisterSymptomForm()
    if flask.request.method == 'POST' and symptom_form.validate_on_submit():
        Symptom = allergy_symptom(
                description = symptom_form.description.data,
                allergy_id = allergy_id)
        
        db.session.add(Symptom)
        db.session.commit()
        flask.flash('Symptom added successfully')

        return flask.redirect(flask.url_for('profiles.allergy_profile', allergy_id = allergy_id))
    
    return flask.render_template('profiles/allergy_profile.html', allergy = Allergy,
            symptoms = symptoms, symptom_form = symptom_form, allergy_form = allergy_form)


@profiles.route('/pregnancy_profile/<int:pregnancy_id>')
def pregnancy_profile(pregnancy_id):
    profile = pregnancy.query.filter_by(pregnancy_id = pregnancy_id)\
            .join(patient, patient.patient_id == pregnancy.pregnancy_id)\
            .add_columns(
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    pregnancy.pregnancy_id
                ).first_or_404()
    
    page = flask.request.args.get('page', 1, type = int)
    pagination = checkup.query.filter_by(pregnancy_id = pregnancy_id)\
            .join(
                    health_practitioner, 
                    health_practitioner.health_practitioner_id == checkup.health_practitioner_id)\
            .join(
                    health_center_department, 
                    health_center_department.hc_department_id == health_practitioner.department_id)\
            .join(health_center, health_center.health_center_id == health_center_department.hc_department_id)\
                            .add_columns(
                                    checkup.checkup_id,
                                    checkup.date_created,
                                    checkup.last_updated,
                                    health_practitioner.health_practitioner_id,
                                    health_practitioner.first_name,
                                    health_practitioner.middle_name,
                                    health_practitioner.last_name,
                                    health_center.health_center_id,
                                    health_center.title,
                                    health_center_department.hc_department_id,
                                    health_center_department.title.label('department')
                            ).order_by(checkup.date_created.desc())\
                            .paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
                                    error_out = False)
    checkups = pagination.items
    return flask.render_template('profiles/pregnancy_profile.html', profile = profile, checkups = checkups)


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
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/health_practitioner_profile/<int:health_practitioner_id>', 
        methods = ['GET', 'POST'])
def health_practitioner_profile(health_practitioner_id):
    Practitioner = health_practitioner.query.filter_by(
            health_practitioner_id = health_practitioner_id).first_or_404()

    tab_variable = 0

    #personal details
    if tab_variable == 0:
        phone_numbers = health_practitioner_phone_no.query.filter_by(
                health_practitioner_id = health_practitioner_id).all()

        return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable,
            phone_numbers = phone_numbers)
    
    elif tab_variable == 1:
        return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)
    
    elif tab_variable == 2:
        return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)
    
    elif tab_variable == 3:
        return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)
    
    return flask.render_template('profiles/health_practitioner_profile.html', 
            practitioner = Practitioner, tab_variable = tab_variable)


@profiles.route('/center_profile/<int:health_center_id>')
def center_profile(health_center_id):
    response = flask.make_response(
        flask.redirect(
            flask.url_for('profiles.health_center_profile', health_center_id = health_center_id)))
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@profiles.route('/departments/<int:health_center_id>')
def departments(health_center_id):
    response = flask.make_response(
        flask.redirect(
            flask.url_for('profiles.health_center_profile', health_center_id = health_center_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
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
        phone_numbers = hc_contact.query.filter_by(health_center_id = health_center_id)\
                .order_by(hc_contact.hc_contact_id).all()

        return flask.render_template('profiles/health_center_profile.html', 
            phone_numbers = phone_numbers, center = Health_Center, 
            tab_variable = tab_variable)
    
    elif tab_variable == 1:
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
