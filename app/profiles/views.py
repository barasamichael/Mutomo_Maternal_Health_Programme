import flask, os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import login_required
from . import profiles
from .. import db
from .forms import (RegisterAllergyForm, RegisterSymptomForm, RegisterSurgeryForm, UpdateBodyPartForm,
        MedicationHistoryForm, FamilyHistoryForm, SocialHistoryForm, RegisterMiscarriageForm,
        UpdatePatientDocumentTypeForm, DocumentUploadForm)

from ..models import (Permission, patient, health_center, health_center_type,
        health_center_department, health_practitioner, health_practitioner_type, 
        patient_phone_no, health_practitioner_phone_no, pregnancy, checkup, next_of_kin,
        hc_contact, allergy, allergy_symptom, social_history, medication_history, 
        miscarriage, surgery, body_part, family_history, social_history, patient_document_type,
        patient_document, health_specialist_type)

@profiles.route('/patient_document_type_profile/<int:type_id>', methods = ['GET', 'POST'])
def patient_document_type_profile(type_id):
    Document_Type = patient_document_type.query\
            .filter_by(patient_document_type_id = type_id).first_or_404()

    form = UpdatePatientDocumentTypeForm()
    if form.validate_on_submit():
        Document_Type = patient_document_type.query\
            .filter_by(patient_document_type_id = type_id).first_or_404()

        Document_Type.title = form.title.data
        Document_Type.description = form.description.data

        db.session.add(Document_Type)
        db.session.commit()

        flask.flash('Update successfull.')
        return flask.redirect(
                flask.url_for('profiles.patient_document_type_profile', type_id = type_id))

    form.title.data = Document_Type.title
    form.description.data = Document_Type.description

    return flask.render_template('profiles/patient_document_type_profile.html', 
            form = form, type = Document_Type)

@profiles.route('/patient_document_types')
def patient_document_types():
    types = patient_document_type.query.order_by(patient_document_type.title.desc()).all()
    return flask.render_template('profiles/patient_document_types.html', 
            types = types)


@profiles.route('/family_history_profile/<int:family_history_id>', 
        methods = ['GET', 'POST'])
def family_history_profile(family_history_id):
    family = family_history.query.filter_by(family_history_id = family_history_id)\
            .join(patient, patient.patient_id == family_history.patient_id)\
            .add_columns(
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    family_history.family_history_id,
                    family_history.title,
                    family_history.description
                ).first_or_404()
    
    form = FamilyHistoryForm()
    if flask.request.method == 'POST' and form.validate_on_submit():
        family = family_history.query.filter_by(
                social_history_id = social_history_id).first_or_404()
        
        family.title = form.title.data
        family.description = form.description.data

        db.session.add(family)
        db.session.commit()

        flask.flash('Update of family history successfull')
        return flask.redirect(flask.url_for(
            'profiles.family_history_profile', family_history_id = family_history_id))

    form.title.data = family.title
    form.description.data = family.description
    return flask.render_template('profiles/family_history_profile.html', form = form,
            family = family)


@profiles.route('/social_history_profile/<int:social_history_id>', 
        methods = ['GET', 'POST'])
def social_history_profile(social_history_id):
    social = social_history.query.filter_by(social_history_id = social_history_id)\
            .join(patient, patient.patient_id == social_history.patient_id)\
            .add_columns(
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    social_history.social_history_id,
                    social_history.title,
                    social_history.description
                ).first_or_404()
    
    form = SocialHistoryForm()
    if flask.request.method == 'POST' and form.validate_on_submit():
        social = social_history.query.filter_by().first_or_404()
        
        social.title = form.title.data
        social.description = form.description.data

        db.session.add(social)
        db.session.commit()

        flask.flash('Update of social history successfull')
        return flask.redirect(flask.url_for(
            'profiles.social_history_profile', social_history_id = social_history_id))

    form.title.data = social.title
    form.description.data = social.description
    return flask.render_template('profiles/social_history_profile.html', form = form,
            social = social)


@profiles.route('/medication_profile/<int:medication_profile_id>', 
        methods = ['GET', 'POST'])
def medication_profile(medication_profile_id):
    medication = medication_history.query\
            .filter_by(medication_history_id = medication_profile_id)\
            .join(patient, patient.patient_id == medication_history.patient_id)\
            .add_columns(
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    medication_history.medication_history_id,
                    medication_history.description,
                    medication_history.remedy,
                    medication_history.start_date,
                    medication_history.nature,
                    medication_history.administration,
                    medication_history.dosage,
                    medication_history.frequency,
                    medication_history.source
                ).first_or_404()
    
    form = MedicationHistoryForm()
    admin_methods = [
            'Orally', 'Inhalation', 'Instillation', 'Injection', 
            'Transdermal', 'Rectal', 'Vaginal', 'Others'
            ]
    med_nature = ['Tablets', 'Capsules', 'Liquids', 'Mixture', 'Others']
    sources = ['prescription', 'over the counter (OTC)']
    
    form = MedicationHistoryForm()
    form.administration.choices = [((item), (item)) for item in admin_methods]
    form.nature.choices = [((item), (item)) for item in med_nature]
    form.source.choices = [((item), (item)) for item in sources]

    if flask.request.method == 'POST' and form.validate_on_submit():
        medication = medication.query.filter_by(
                medication_history_id = medication_profile_id).first_or_404()

        medication.description = form.description.data
        medication.remedy = form.remedy.data
        medication.dosage = form.dosage.data
        medication.frequency = form.frequency.data
        medication.nature = form.nature.data
        medication.administration = form.administration.data
        medication.start_date = form.start_date.data
        medication.source = form.source.data
        
        db.session.add(medication)
        db.session.commit()

        flask.flash('Update of medication history successfull.')
        return flask.redirect(flask.url_for('profiles.medication_profile', 
            medication_profile_id = medication_profile_id))

    form.description.data = medication.description
    form.remedy.data = medication.remedy
    form.dosage.data = medication.dosage
    form.frequency.data = medication.frequency
    form.nature.data = medication.nature
    form.administration.data = medication.administration
    form.start_date.data = medication.start_date
    form.source.data = medication.source

    return flask.render_template('profiles/medication_profile.html', 
            medication = medication, form = form)


@profiles.route('/body_part_profile/<int:body_part_id>', methods = ['GET', 'POST'])
def body_part_profile(body_part_id):
    part = body_part.query.filter_by(body_part_id = body_part_id).first_or_404()

    form = UpdateBodyPartForm()
    if flask.request.method == 'POST' and form.validate_on_submit():
        part = body_part.query.filter_by(body_part_id = body_part_id).first_or_404()

        part.title = form.title.data
        part.description = form.description.data

        db.session.add(part)
        db.session.commit()

        flask.flash('Update successfull')
        return flask.redirect(
                flask.url_for('profiles.body_part_profile', body_part_id = body_part_id))
    
    form.title.data = part.title
    form.description.data = part.description

    return flask.render_template('profiles/body_part_profile.html', part = part, form = form)


@profiles.route('/view_body_part_records')
def view_body_part_records():
    page = flask.request.args.get('page', 1, type = int)
    pagination = body_part.query.order_by(body_part.title.desc())\
            .paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], 
                    error_out = False)
    parts = pagination.items

    return flask.render_template('profiles/view_body_part_records.html', 
            pagination = pagination, parts = parts)


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


@profiles.route('/view_health_specialist_types')
def view_health_specialist_types():
    page = flask.request.args.get('page', 1, type = int)
    pagination = health_specialist_type.query.order_by(health_specialist_type.title.desc())\
            .paginate(page, flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
    specialities = pagination.items

    return flask.render_template('profiles/view_health_specialist_types.html', 
            specialities = specialities, pagination = pagination)



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


@profiles.route('/conditions/<int:patient_id>')
def conditions(patient_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('profiles.patient_profile', patient_id = patient_id)))
    response.set_cookie('tab_var', '4', max_age = 60*60)
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
        document_form = DocumentUploadForm()
        
        types = patient_document_type.query.order_by(patient_document_type.title.desc()).all()
        document_form.type_id.choices = [((type.patient_document_type_id), (type.title)) for type in types] 
        
        if document_form.validate_on_submit():
            uploaded_file = document_form.file.data
            filename = secure_filename(uploaded_file.filename)

            folder = os.path.join(flask.current_app.config['DOCUMENT_UPLOAD_PATH'], 'patients')
            if not os.path.isdir(folder):
                os.makedirs(folder)

            #save file on server
            uploaded_file.save(os.path.join(folder, filename))

            #update database
            Document = patient_document(
                    filename = filename,
                    patient_document_type_id = document_form.type_id.data,
                    patient_id = patient_id
                    )
            db.session.add(Document)
            db.session.commit()

            flask.flash('Document registered successfully.')
            return flask.redirect(flask.url_for('profiles.patient_profile', 
                patient_id = patient_id))

        phone_numbers = patient_phone_no.query.filter_by(patient_id = patient_id).all()
        kins = next_of_kin.query.filter_by(patient_id = patient_id).all()
        documents = patient_document.query.filter_by(patient_id = patient_id)\
                .join(
                        patient_document_type, 
                        patient_document_type.patient_document_type_id == patient_document.patient_document_type_id)\
                .add_columns(
                        patient_document.patient_document_id,
                        patient_document.filename,
                        patient_document.date_created,
                        patient_document_type.patient_document_type_id,
                        patient_document_type.title
                        ).all()
        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                tab_variable = tab_variable, phone_numbers = phone_numbers, kins = kins,
                documents = documents, form = document_form)
    
    #medical history details
    if tab_variable == 4:
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

            return flask.redirect(flask.url_for('profiles.conditions', patient_id = patient_id))

        allergies = allergy.query.filter_by(patient_id = patient_id)\
                .order_by(allergy.description.asc()).all()

        #get symptoms for each allergy and store it in a dictionary
        symptoms = {}
        for _allergy in allergies:
            allergy_symptoms = allergy_symptom.query.filter_by(allergy_id = _allergy.allergy_id).all()
            symptoms.update({_allergy.allergy_id: allergy_symptoms})

        #---------------------------------------------------------#
        #                       SURGERIES                         #
        #---------------------------------------------------------#

        surgery_form = RegisterSurgeryForm()

        body_parts = body_part.query.order_by(body_part.title.desc()).all()
        surgery_form.body_part_id.choices = [((part.body_part_id), (part.title)) for part in body_parts]
    
        if flask.request.method == 'POST' and surgery_form.validate_on_submit():
            Surgery = surgery(
                    description = surgery_form.description.data,
                    status = surgery_form.status.data,
                    date = surgery_form.date.data,
                    body_part_id = surgery_form.body_part_id.data,
                    patient_id = patient_id,
                    )

            db.session.add(Surgery)
            db.session.commit()

            flask.flash('Surgery recorded successfully')
            return flask.redirect(flask.url_for('profiles.conditions', patient_id = patient_id))

        surgeries = surgery.query.filter_by(patient_id = patient_id)\
                .join(body_part, body_part.body_part_id == surgery.body_part_id)\
                .add_columns(
                        surgery.surgery_id,
                        surgery.description,
                        surgery.status,
                        surgery.date,
                        body_part.body_part_id,
                        body_part.title
                    ).order_by(surgery.date.desc()).all()

        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                allergies = allergies, symptoms = symptoms, allergy_form = allergy_form,
                surgeries = surgeries, surgery_form = surgery_form, tab_variable = tab_variable)
    
    #other details

    if tab_variable == 1:
        socials = social_history.query.filter_by(patient_id = patient_id)\
                .order_by(social_history.title.desc()).all()
        social_form = SocialHistoryForm()
        if flask.request.method == 'POST' and social_form.validate_on_submit():
            social = social_history(
                    title = social_form.title.data,
                    description = social_form.description.data,
                    patient_id = patient_id
                    )
            db.session.add(social)
            db.session.commit()

            flask.flash('Social history updated successfully')
            return flask.redirect(
                    flask.url_for('profiles.patient_profile', patient_id = patient_id))
        
        families = family_history.query.filter_by(patient_id = patient_id)\
                .order_by(family_history.title.desc()).all()
        family_form = FamilyHistoryForm()
        if flask.request.method == 'POST' and family_form.validate_on_submit():
            family = family_history(
                    title = family_form.title.data,
                    description = family_form.description.data,
                    patient_id = patient_id
                    )
            db.session.add(family)
            db.session.commit()

            flask.flash('Family history updated successfully')
            return flask.redirect(
                    flask.url_for('profiles.patient_profile', patient_id = patient_id))

        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                family_form = family_form, social_form = social_form,
                socials = socials, families = families, tab_variable = tab_variable)
    

    if tab_variable == 2:
        medication = medication_history.query.filter_by(patient_id = patient_id)\
                .order_by(medication_history.start_date.desc()).limit(15)
        
        #Select field data
        admin_methods = [
                'Orally', 'Inhalation', 'Instillation', 'Injection', 
                'Transdermal', 'Rectal', 'Vaginal', 'Others'
                ]
        med_nature = ['Tablets', 'Capsules', 'Liquids', 'Mixture', 'Others']
        sources = ['prescribed', 'over the counter (OTC)']

        medication_form = MedicationHistoryForm()
        medication_form.administration.choices = [((item), (item)) for item in admin_methods]
        medication_form.nature.choices = [((item), (item)) for item in med_nature]
        medication_form.source.choices = [((item), (item)) for item in sources]

        if flask.request.method == 'POST' and medication_form.validate_on_submit():
            Medication = medication_history(
                    description = medication_form.description.data,
                    remedy = medication_form.remedy.data,
                    dosage = medication_form.dosage.data,
                    frequency = medication_form.frequency.data,
                    start_date = medication_form.start_date.data,
                    administration = medication_form.administration.data,
                    nature = medication_form.nature.data,
                    source = medication_form.source.data,
                    patient_id = patient_id
                    )
            db.session.add(Medication)
            db.session.commit()

            flask.flash('Medication history updated successfully')
            return flask.redirect(
                    flask.url_for('profiles.patient_profile', patient_id = patient_id))

        return flask.render_template('profiles/patient_profile.html', patient = Patient, 
                medication = medication, medication_form = medication_form, 
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

        miscarriages = miscarriage.query.filter_by(patient_id = patient_id).all()

        miscarriage_form = RegisterMiscarriageForm()

        trimesters = ['first', 'second', 'third']
        miscarriage_form.trimester.choices = [((item), (item)) for item in trimesters]

        if miscarriage_form.validate_on_submit():
            Miscarriage = miscarriage(
                    trimester = miscarriage_form.trimester.data,
                    cause = miscarriage_form.cause.data,
                    patient_id = patient_id
                    )
            db.session.add(Miscarriage)
            db.session.commit()

            return flask.redirect(
                    flask.url_for('profiles.patient_profile', patient_id = patient_id))

        return flask.render_template('profiles/patient_profile.html', patient = Patient,
                tab_variable = tab_variable, pregnancies = pregnancies, dates = dates,
                miscarriage_form = miscarriage_form, miscarriages = miscarriages)

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


@profiles.route('/list_of_health_specialists')
def list_of_health_specialists():
    page = flask.request.args.get('page', 1, type = int)
    
    pagination = health_specialist.query\
        .join(health_specialist_type, 
                health_specialist_type.health_specialist_type_id == health_specialist.health_specialist_type_id)\
        .add_columns(
                health_specialist.practitioner_id,
                health_specialist.first_name,
                health_specialist.middle_name,
                health_specialist.last_name,
                health_specialist.gender,
                health_specialist.email_address,
                health_specialist_type.health_specialist_type_id,
                health_specialist_type.title,
                health_specialist_type.health_center
            ).order_by(health_specialist.practitioner_id.desc()).paginate(page,
                    flask.current_app.config['FLASKY_POSTS_PER_PAGE'], error_out = False)
    specialists = pagination.items

    return flask.render_template('profiles/list_of_health_specialists.html', 
            pagination = pagination, specialists = specialists)


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
