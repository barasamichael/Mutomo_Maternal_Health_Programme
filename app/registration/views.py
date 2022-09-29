import flask, os, iso3166, imghdr
from flask_login import login_required
from werkzeug.utils import secure_filename
from . import registration
from .. import db

from .forms import (RegisterPatientForm, RegisterHealthCenterTypeForm, RegisterHealthCenterForm, 
        ImageForm, RegisterDepartmentForm, RegisterHealthPractitionerForm,
        RegisterHealthPractitionerTypeForm)

from ..models import (Permission, patient, health_center_type, health_center, patient_phone_no, 
        health_practitioner, health_center_department, health_practitioner_type)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@registration.route('/register_department_service/<int:hc_department_id>')
def register_department_service(hc_department_id):
    form = RegisterDepartmentServiceForm()

    if form.validate_on_submit():
        Service = department_service(
                title = form.title.data,
                description = form.description.data,
                hc_department_id = hc_department_id
                )
        db.session.add(Service)
        db.session.commit()
        flask.flash('Service registered successfully')
        
        return flask.redirect(
            flask.url_for('registration.register_department_service', 
                hc_department_id = hc_department_id))

    return flask.render_template('registration/register_department_service.html',
            form = form)

@registration.route('/register_health_center_type/<int:health_center_id>', 
        methods = ['GET', 'POST'])
def register_department(health_center_id):
    form = RegisterDepartmentForm()

    if form.validate_on_submit():
        Department = health_center_department(
                title = form.title.data,
                description = form.description.data,
                health_center_id = health_center_id
        )
        db.session.add(Department)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully')
        return flask.redirect(flask.url_for('registration.register_department', 
            health_center_id = health_center_id))

    return flask.render_template('registration/register_department.html', 
            form = form)


@registration.route('/register_health_center_type', methods = ['GET', 'POST'])
def register_health_center_type():
    form = RegisterHealthCenterTypeForm()

    if form.validate_on_submit():
        Health_Center_Type = health_center_type(
                title = form.title.data,
                description = form.description.data
        )
        db.session.add(Health_Center_Type)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully')
        return flask.redirect(flask.url_for('registration.register_health_center_type'))

    return flask.render_template('registration/register_health_center_type.html', 
            form = form)


@registration.route('/register_health_center', methods = ['GET', 'POST'])
def register_health_center():
    form = RegisterHealthCenterForm()

    types = health_center_type.query.order_by(health_center_type.title.asc()).all()
    form.hc_type_id.choices = [((hc_type.hc_type_id), (hc_type.title)) 
            for hc_type in types]

    if form.validate_on_submit():
        Health_Center = health_center(
                title = form.title.data,
                email_address = form.email_address.data,
                location_address = form.location_address.data,
                x_coordinate = form.x_coordinate.data,
                y_coordinate = form.y_coordinate.data,
                z_coordinate = form.z_coordinate.data,
                hc_type_id = form.hc_type_id.data
        )
        db.session.add(Health_Center)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully')
        return flask.redirect(flask.url_for('registration.register_health_center'))

    return flask.render_template('registration/register_health_center.html', form = form)


@registration.route('/upload_health_department_image/<int:hc_department_id>', 
        methods = ['GET', 'POST'])
def upload_health_department_image(hc_department_id):
    Department = health_center_department.query.filter_by(
            hc_department_id = hc_department_id).first_or_404()

    form = ImageForm()    
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS']\
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

        #save file in storage
        folder = flask.current_app.config['CENTER_DEPARTMENT_UPLOAD_PATH']
        if not os.path.isdir(folder):
            os.makedirs(folder)

        uploaded_file.save(os.path.join(folder, filename))

        #save filename in database
        Department.associated_image = filename
        db.session.add(Department)
        db.session.commit()

        return flask.redirect(flask.url_for('profiles.center_department', 
            hc_department_id = hc_department_id))

    return flask.render_template('registration/upload_health_department_image.html', form =  form)


@registration.route('/upload_health_practitioner_image/<int:health_practitioner_id>', 
        methods = ['GET', 'POST'])
def upload_health_practitioner_image(health_practitioner_id):
    Practitioner = health_practitioner.query.filter_by(practitioner_id = health_practitioner_id)\
            .first_or_404()

    form = ImageForm()    
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS']\
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

        #save file in storage
        folder = flask.current_app.config['HEALTH_PRACTITIONER_UPLOAD_PATH']
        if not os.path.isdir(folder):
            os.makedirs(folder)

        uploaded_file.save(os.path.join(folder, filename))

        #save filename in database
        Practitioner.associated_image = filename
        db.session.add(Practitioner)
        db.session.commit()

        return flask.redirect(flask.url_for('profiles.health_practitioner_profile', 
            health_practitioner_id = Practitioner.health_practitioner_id))

    return flask.render_template('registration/upload_health_practitioner_image.html', form =  form)


@registration.route('/upload_health_center_image/<int:health_center_id>', 
        methods = ['GET', 'POST'])
def upload_health_center_image(health_center_id):
    Health_Center = health_center.query.filter_by(health_center_id = health_center_id)\
            .first_or_404()

    form = ImageForm()    
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS']\
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

        #save file in storage
        folder = flask.current_app.config['HEALTH_CENTER_UPLOAD_PATH']
        if not os.path.isdir(folder):
            os.makedirs(folder)

        uploaded_file.save(os.path.join(folder, filename))

        #save filename in database
        Health_Center.associated_image = filename
        db.session.add(Health_Center)
        db.session.commit()

        return flask.redirect(flask.url_for('profiles.health_center_profile', 
            health_center_id = health_center_id))

    return flask.render_template('registration/upload_health_center_image.html', form =  form)


@registration.route('/upload_patient_image/<int:patient_id>', methods = ['GET', 'POST'])
def upload_patient_image(patient_id):
    Patient = patient.query.filter_by(patient_id = patient_id).first_or_404()
    form = ImageForm()
    
    if form.validate_on_submit():
        uploaded_file = form.file.data
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in flask.current_app.config['UPLOAD_EXTENSIONS']\
                    or file_ext != validate_image(uploaded_file.stream):
                        return 'Invalid Image', 400

        #save file in storage
        folder = flask.current_app.config['PATIENT_UPLOAD_PATH']
        if not os.path.isdir(folder):
            os.makedirs(folder)

        uploaded_file.save(os.path.join(folder, filename))

        #save filename in database
        Patient.associated_image = filename
        db.session.add(Patient)
        db.session.commit()

        return flask.redirect(flask.url_for('profiles.patient_profile', 
            patient_id = patient_id))

    return flask.render_template('registration/upload_patient_image.html', form =  form)


@registration.route('/register_health_practitioner_type', methods = ['GET', 'POST'])
def register_health_practitioner_type():
    form = RegisterHealthPractitionerTypeForm()

    if form.validate_on_submit():
        Practitioner_Type = health_practitioner_type(
                title = form.title.data,
                description = form.description.data
                )

        db.session.add(Practitioner_Type)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully')
        return flask.redirect(flask.url_for('registration.register_health_practitioner_type'))

    return flask.render_template('registration/register_health_practitioner_type.html', form = form)


@registration.route('/register_health_practitioner/<int:department_id>', 
        methods = ['GET', 'POST'])
def register_health_practitioner(department_id):
    form = RegisterHealthPractitionerForm()
    practitioner_types = health_practitioner_type.query.all()
    countries_list = [((country.name), (country.name)) for country in iso3166.countries]
    
    form.nationality.choices = countries_list
    form.gender.choices = [(('female'), ('female')), (('male'), ('male'))]
    form.hp_type_id.choices = [((item.hp_type_id), (item.title)) for item in practitioner_types]

    if form.validate_on_submit():
        Health_Practitioner = health_practitioner(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                location_address = form.location_address.data,
                nationality = form.nationality.data,
                national_id_no = form.national_id_no.data,
                hp_type_id = form.hp_type_id.data,
                practitioner_id = form.practitioner_id.data,
                department_id = department_id
        )
        db.session.add(Health_Practitioner)

        db.session.commit()
        flask.flash(f'{form.first_name.data} {form.middle_name.data} {form.last_name.data} registered successfully')
        return flask.redirect(flask.url_for('registration.register_health_practitioner', 
            department_id = department_id))

    return flask.render_template('registration/register_health_practitioner.html', form = form)


@registration.route('/register_patient', methods = ['GET', 'POST'])
def register_patient():
    form = RegisterPatientForm()
    
    countries_list = [((country.name), (country.name)) for country in iso3166.countries]
    form.nationality.choices = countries_list

    form.marital_status.choices = [
            (('single'), ('single')),
            (('engaged'), ('engaged')),
            (('married'), ('married')),
            (('separated'), ('separated')),
            (('divorced'), ('divorced')),
            (('widowed'), ('widowed'))
    ]
    if form.validate_on_submit():
        Patient = patient(
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                date_of_birth = form.date_of_birth.data,
                email_address = form.email_address.data,
                location_address = form.location_address.data,
                nationality = form.nationality.data,
                national_id_no = form.national_id_no.data,
                marital_status = form.marital_status.data
        )
        db.session.add(Patient)

        db.session.commit()
        flask.flash(f'{form.first_name.data} {form.middle_name.data} {form.last_name.data} registered successfully')
        
        return flask.redirect(flask.url_for('registration.register_patient'))
    
    return flask.render_template('registration/register_patient.html', form = form)
