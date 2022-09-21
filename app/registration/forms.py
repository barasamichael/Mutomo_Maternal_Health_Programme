from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SelectField, BooleanField, SubmitField, IntegerField, 
        FileField, PasswordField, FloatField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError
from ..models import (patient, patient_phone_no, health_center, health_center_department, 
        health_center_type, health_practitioner, health_practitioner_type)


class ImageForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class RegisterPatientForm(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), Length(1, 128)])
    middle_name = StringField('middle name', validators = [Length(0, 128)])
    last_name = StringField('last name', validators = [Length(0, 128)])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])

    email_address = StringField('email address',
            validators = [DataRequired(), Length(1, 128), Email()])

    location_address = StringField('location address',
            validators = [DataRequired(), Length(1, 255)])
    nationality = SelectField('select country', validators = [DataRequired()])
    national_id_no = IntegerField('national ID number', validators = [DataRequired()])
    marital_status = SelectField('marital status', validators = [DataRequired()])

    submit = SubmitField('submit')
