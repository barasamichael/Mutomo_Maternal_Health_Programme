from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (StringField, SelectField, BooleanField, SubmitField, IntegerField, 
        FileField, PasswordField, FloatField, TextField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import DateField
from wtforms import ValidationError
from ..models import (patient, checkup_document_type)

class ImageForm(FlaskForm):
    file = FileField('select file', validators = [FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Select Image Files Only.')])

    submit = SubmitField('submit')


class RegisterCheckUpDocumentTypeForm(FlaskForm):
    title = StringField('title', validators = [DataRequired(), Length(1, 16)])
    description = TextField('description', validators = [DataRequired()])

    submit = SubmitField('submit')
    
    def validate_title(self,field):
        if checkup_document_type.query.filter_by(title = field.data).first():
            raise ValidationError(f'{field.data} already exists.')
