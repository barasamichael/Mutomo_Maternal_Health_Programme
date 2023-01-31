from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SelectField, BooleanField, SubmitField, IntegerField, 
        FileField, PasswordField, FloatField, TextField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField, TimeField
from wtforms import ValidationError
from ..models import (allergy, allergy_symptom, patient, patient_document)

class RegisterDepartmentScheduleForm(FlaskForm):
    day_id = SelectField('Day of the week', validators = [DataRequired()]) 
    start_time = TimeField('Start time', validators = [DataRequired()])
    end_time = TimeField('End time', validators = [DataRequired()]) 
    
    submit = SubmitField('submit')


class DocumentUploadForm(FlaskForm):
    type_id = SelectField('Document type', validators = [DataRequired(), Length(1, 255)])
    file = FileField('Select File', 
            validators = [FileRequired(), FileAllowed(['pdf'], 'Select PDF Files Only.')])
    
    submit = SubmitField('submit')


class UpdatePatientDocumentTypeForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 120)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')


class RegisterMiscarriageForm(FlaskForm):
    trimester = SelectField('trimester', validators = [DataRequired()])
    cause = TextField('cause', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')


class FamilyHistoryForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 120)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')


class SocialHistoryForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 120)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')


class UpdateBodyPartForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 120)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')


class MedicationHistoryForm(FlaskForm):
    remedy = StringField('condition (ailment)', validators = [DataRequired(), Length(1, 255)])
    description = StringField('description of medication', validators = [DataRequired(), Length(1, 255)])
    source = SelectField('source of medication', validators = [DataRequired()])
    dosage = StringField('dosage', validators = [DataRequired(), Length(1, 64)])
    frequency = StringField('frequency', validators = [DataRequired(), Length(1, 64)])
    administration = SelectField('method of administration', validators = [DataRequired(), Length(1, 120)])
    nature = SelectField('nature of medication', validators = [DataRequired()])
    start_date = DateField('date administered', validators = [DataRequired()])

    submit = SubmitField('submit')


class RegisterAllergyForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(), Length(1, 255)])
    cause = TextField('cause', validators = [DataRequired(), Length(1, 2000)])
    remedy = TextField('remedy', validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')

    def validate_description(self,field):
        if allergy.query.filter_by(description = field.data).first():
            raise ValidationError(f'{field.data} is already recorded')

class AssignServiceForm(FlaskForm):
    service_id = SelectField('select service', validators = [DataRequired()])
    submit = SubmitField('submit')

class RegisterSurgeryForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(), Length(1, 255)])
    status = SelectField('status (Major or Minor)', 
            choices = [(('major'), ('major')), (('minor'), ('minor'))], 
            validators = [DataRequired(), Length(1, 32)])
    body_part_id = SelectField('Select associated part of the body', 
            validators = [DataRequired(), Length(1, 32)])


    date = DateField('date performed', validators = [DataRequired()])
    submit = SubmitField('submit')


class RegisterSymptomForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(), Length(1, 255)])
    submit = SubmitField('submit')

