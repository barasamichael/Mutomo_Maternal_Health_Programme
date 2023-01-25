import flask, os, iso3166, imghdr
from flask_login import login_required
from werkzeug.utils import secure_filename
from random import randint
from . import checkups
from .. import db

from .forms import (RegisterCheckUpDocumentTypeForm, DocumentUploadForm, RegisterSymptomForm,
        RegisterRecommendationForm, RegisterAffirmativeForm)

from ..models import (pregnancy, checkup, patient, health_practitioner, checkup_document_type, checkup_document,
        checkup_symptom, body_part, recommendation, affirmative)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


@checkups.route('/documents/<int:checkup_id>')
def checkup_documents(checkup_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('checkups.checkup_profile', checkup_id = checkup_id)))
    response.set_cookie('tab_var', '0', max_age = 60*60)
    return response


@checkups.route('/diagnosis/<int:checkup_id>')
def checkup_diagnosis(checkup_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('checkups.checkup_profile', checkup_id = checkup_id)))
    response.set_cookie('tab_var', '1', max_age = 60*60)
    return response


@checkups.route('/recommendations/<int:checkup_id>')
def checkup_recommendations(checkup_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('checkups.checkup_profile', checkup_id = checkup_id)))
    response.set_cookie('tab_var', '2', max_age = 60*60)
    return response


@checkups.route('/affirmatives/<int:checkup_id>')
def checkup_affirmatives(checkup_id):
    response = flask.make_response(
        flask.redirect(flask.url_for('checkups.checkup_profile', checkup_id = checkup_id)))
    response.set_cookie('tab_var', '3', max_age = 60*60)
    return response


@checkups.route('/checkup_profile/<int:checkup_id>', methods = ['GET', 'POST'])
def checkup_profile(checkup_id):
    profile = checkup.query.filter_by(checkup_id = checkup_id)\
            .join(pregnancy, pregnancy.pregnancy_id == checkup.pregnancy_id)\
            .join(patient, patient.patient_id == pregnancy.patient_id)\
            .join(
                    health_practitioner,
                    health_practitioner.health_practitioner_id == checkup.health_practitioner_id)\
            .add_columns(
                    checkup.checkup_id,
                    pregnancy.pregnancy_id,
                    pregnancy.conception_date,
                    pregnancy.due_date,
                    patient.patient_id,
                    patient.first_name,
                    patient.middle_name,
                    patient.last_name,
                    health_practitioner.health_practitioner_id,
                    health_practitioner.first_name.label('health_first_name'),
                    health_practitioner.middle_name.label('health_middle_name'),
                    health_practitioner.last_name.label('health_last_name'),
                ).first_or_404()
    
    tab_variable = 0
    if flask.request.cookies.get('tab_var') is not None:
        tab_variable = int(flask.request.cookies.get('tab_var'))

    #personal details
    if tab_variable == 0:
        document_form = DocumentUploadForm()
        
        types = checkup_document_type.query.order_by(checkup_document_type.title.desc()).all()
        document_form.type_id.choices = [((type.checkup_document_type_id), (type.title)) for type in types] 
        
        if document_form.validate_on_submit():
            uploaded_file = document_form.file.data
            filename = secure_filename(uploaded_file.filename)

            folder = os.path.join(flask.current_app.config['DOCUMENT_UPLOAD_PATH'], 'checkups')
            if not os.path.isdir(folder):
                os.makedirs(folder)

            #save file on server
            uploaded_file.save(os.path.join(folder, filename))

            #update database
            Document = checkup_document(
                    filename = filename,
                    checkup_document_type_id = document_form.type_id.data,
                    checkup_id = checkup_id
                    )
            db.session.add(Document)
            db.session.commit()

            flask.flash('Checkup document registered successfully.')     
            return flask.redirect(flask.url_for('checkups.checkup_profile', 
                checkup_id = checkup_id))
        
        return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable, document_form = document_form)
    
    elif tab_variable == 1:
        symptom_form = RegisterSymptomForm()

        body_parts = [((item.body_part_id), (item.title)) for item in body_part.query.all()]
        symptom_form.body_part_id.choices = body_parts

        if symptom_form.validate_on_submit():
            Symptom = checkup_symptom(
                    body_part_id = symptom_form.body_part_id.data,
                    description = symptom_form.description.data,
                    checkup_id = profile.checkup_id
                    )
            db.session.add(Symptom)
            db.session.commit()

            flask.flash('Symptom added successfully.')
            return flask.redirect(flask.url_for('checkups.checkup_profile', 
                checkup_id = checkup_id))

        symptoms = checkup_symptom.query.filter_by(checkup_id = checkup_id)\
                .join(body_part, body_part.body_part_id == checkup_symptom.body_part_id)\
                .add_columns(
                        checkup_symptom.checkup_symptom_id,
                        checkup_symptom.description,
                        body_part.body_part_id,
                        body_part.title,
                        ).order_by(checkup_symptom.description.desc()).all()

        return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable, symptom_form = symptom_form, symptoms = symptoms)
    
    elif tab_variable == 2:
        recommendations = recommendation.query.filter_by(checkup_id = checkup_id).all()

        recommendation_form = RegisterRecommendationForm()
        if recommendation_form.validate_on_submit():
            Recommendation = recommendation(
                    description = recommendation_form.description.data,
                    checkup_id = checkup_id
                    )
            
            db.session.add(Recommendation)
            db.session.commit()

            flask.flash("Recommendation added successfully.")

            return flask.redirect(flask.url_for('checkups.checkup_profile', 
                checkup_id = checkup_id))

        return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable, recommendation_form = recommendation_form, 
            recommendations = recommendations)

    elif tab_variable == 3:
        affirmatives = affirmative.query.filter_by(checkup_id = checkup_id).all()

        affirmative_form = RegisterAffirmativeForm()
        if affirmative_form.validate_on_submit():
            Affirmative = affirmative(
                    description = affirmative_form.description.data,
                    checkup_id = checkup_id
                    )
            
            db.session.add(Affirmative)
            db.session.commit()

            flask.flash("Affirmative added successfully.")

            return flask.redirect(flask.url_for('checkups.checkup_profile', 
                checkup_id = checkup_id))

        return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable, affirmative_form = affirmative_form, 
            affirmatives = affirmatives)


    return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable)


    return flask.render_template('checkups/checkup_profile.html', profile = profile,
            tab_variable = tab_variable)


@checkups.route('/register_checkup/<int:pregnancy_id>')
def register_checkup(pregnancy_id):
    Checkup = checkup(
            pregnancy_id = pregnancy_id,
            health_practitioner_id = randint(30, 100)
            )
    db.session.add(Checkup)
    db.session.commit()

    flask.flash("New antenatal session created successfully.")
    return flask.redirect(flask.url_for('profiles.pregnancy_profile', pregnancy_id = pregnancy_id))


@checkups.route('/register_checkup_document_type', methods = ['GET', 'POST'])
def register_checkup_document_type():
    form = RegisterCheckUpDocumentTypeForm()
    if form.validate_on_submit():
        Document_Type = checkup_document_type(
                title = form.title.data,
                description = form.description.data
                )
        db.session.add(Document_Type)
        db.session.commit()

        flask.flash(f'{form.title.data} registered successfully.')
        return flask.redirect(flask.url_for('main.homepage'))
    
    return flask.render_template('checkups/register_checkup_document_type.html', form = form)


@checkups.route('/upload_checkup_document/<int:checkup_id>', methods = ['GET', 'POST'])
def upload_checkup_document(checkup_id):
    return flask.render_template('checkups/upload_checkup_document.html')


@checkups.route('/view_checkup_document_types')
def view_checkup_document_types():
    document_types = checkup_document_type.query.\
            order_by(checkup_document_type.title.desc()).all()

    return flask.render_template('checkups/view_checkup_document_types.html',
            document_types = document_types)
