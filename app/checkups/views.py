import flask, os, iso3166, imghdr
from flask_login import login_required
from werkzeug.utils import secure_filename
from random import randint
from . import checkups
from .. import db

from .forms import (RegisterCheckUpDocumentTypeForm)

from ..models import (pregnancy, checkup, patient, health_practitioner, checkup_document_type, checkup_document)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)

    if not format:
        return None

    return '.' + (format if format == 'jpeg' else 'jpg')


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
    return flask.render_template('checkups/checkup_profile.html', profile = profile)


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
