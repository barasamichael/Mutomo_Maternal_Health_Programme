from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SelectField, BooleanField, SubmitField, IntegerField, 
        FileField, PasswordField, FloatField, TextField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError
from ..models import (allergy, allergy_symptom, patient)

class RegisterAllergyForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(), Length(1, 255)])
    cause = TextField('cause', validators = [DataRequired(), Length(1, 2000)])
    remedy = TextField('remedy', validators = [DataRequired(), Length(1, 2000)])

    submit = SubmitField('submit')

    def validate_description(self,field):
        if allergy.query.filter_by(description = field.data).first():
            raise ValidationError(f'{field.data} is already recorded')

class RegisterSymptomForm(FlaskForm):
    description = StringField('description', validators = [DataRequired(), Length(1, 255)])
    submit = SubmitField('submit')

