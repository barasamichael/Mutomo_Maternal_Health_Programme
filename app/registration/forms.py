from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SelectField, BooleanField, SubmitField, IntegerField, 
        FileField, PasswordField, FloatField, TextField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError
from ..models import (patient, patient_phone_no, health_center, health_center_department, 
        health_center_type, health_practitioner, health_practitioner_type, hc_contact,
        health_practitioner_phone_no)

class ImageForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class RegisterDepartmentForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')

    def validate_title(self,field):
        if health_center_department.query.filter_by(title = field.data).first():
            raise ValidationError(f'{field.data} already registered')


class RegisterHealthPractitionerTypeForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')

    def validate_title(self,field):
        if health_center_type.query.filter_by(title = field.data).first():
            raise ValidationError(f'{field.data} already registered')


class RegisterHealthCenterTypeForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    description = TextField('description', 
            validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')

    def validate_title(self,field):
        if health_center_type.query.filter_by(title = field.data).first():
            raise ValidationError(f'{field.data} already registered')


class RegisterHealthCenterForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 255)])
    hc_type_id = SelectField('select type of health center', 
            validators = [DataRequired()])

    email_address = StringField('email address',
            validators = [DataRequired(), Length(1, 128), Email()])
    location_address = StringField('location address', 
            validators = [DataRequired(), Length(1, 255)])
    
    x_coordinate = FloatField('x coordinate', validators = [DataRequired()])
    y_coordinate = FloatField('y coordinate', validators = [DataRequired()])
    z_coordinate = FloatField('z coordinate', validators = [DataRequired()])

    submit = SubmitField('submit')
    
    def validate_title(self,field):
        if health_center.query.filter_by(title = field.data).first():
            raise ValidationError(f'{field.data} already exists')
    
    def validate_email_address(self,field):
        if health_center.query.filter_by(email_address = field.data).first():
            raise ValidationError(f'{field.data} email address is already in use')

class RegisterHealthPractitionerForm(FlaskForm):
    first_name = StringField('first name', validators = [DataRequired(), Length(1, 128)])
    middle_name = StringField('middle name', validators = [Length(0, 128)])
    last_name = StringField('last name', validators = [Length(0, 128)])
    gender = SelectField('gender', validators = [DataRequired()])

    date_of_birth = DateField('date of birth', validators = [DataRequired()])

    email_address = StringField('email address',
            validators = [DataRequired(), Length(1, 128), Email()])

    location_address = StringField('location address',
            validators = [DataRequired(), Length(1, 255)])
    nationality = SelectField('select country', validators = [DataRequired()])
    national_id_no = IntegerField('national ID number', validators = [DataRequired()])
    
    practitioner_id = IntegerField('practitioner ID', validators = [DataRequired()])
    hp_type_id = SelectField('speciality', validators = [DataRequired()])

    submit = SubmitField('submit')


class RegisterPregnancyForm(FlaskForm):
    conception_date = DateField('enter date of conception', validators = [DataRequired()])
    due_date = DateField('enter approximated due date', validators = [DataRequired()])

    submit = SubmitField('submit')
    

class RegisterHealthCenterContactForm(FlaskForm):
    description = StringField('contact', validators = [DataRequired(), Length(1, 16)])
    emergency = BooleanField('this is an emergency contact')

    submit = SubmitField('submit')
    
    def validate_description(self,field):
        if hc_contact.query.filter_by(description = field.data).first():
            raise ValidationError(f'{field.data} already exists. Please try another contact')


class RegisterHealthPractitionerPhoneNoForm(FlaskForm):
    contact = StringField('contact', validators = [DataRequired(), Length(1, 16)])
    emergency = BooleanField('this is an emergency contact')

    submit = SubmitField('submit')
    
    def validate_contact(self,field):
        if health_practitioner_phone_no.query.filter_by(contact = field.data).first():
            raise ValidationError(f'{field.data} already exists. Please try another number')
    


class RegisterPatientPhoneNoForm(FlaskForm):
    contact = StringField('contact', validators = [DataRequired(), Length(1, 16)])
    emergency = BooleanField('this is an emergency contact')

    submit = SubmitField('submit')
    
    def validate_contact(self,field):
        if patient_phone_no.query.filter_by(contact = field.data).first():
            raise ValidationError(f'{field.data} already exists. Please try another number')
    

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
