from wtforms import Form, ValidationError, EmailField, DateField, PasswordField, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, DecimalField, SelectMultipleField, widgets
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from flask import session, Flask
from werkzeug.security import generate_password_hash, check_password_hash

from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms.widgets import MonthInput
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import InputRequired 

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FileUploadForm(FlaskForm):
    file_upload_field = FileField('File Upload', [FileRequired(message="Please upload a file.")])
    masking_options = MultiCheckboxField('Masking Options', choices=[
                                      ('Password', 'Password'), 
                                      ('NRIC', 'NRIC'), 
                                      ('Credit Card Number', 'Credit Card Number'),
                                      ('CVC', 'CVC'),])
    # masking_options = SelectField('Masking Options',
    #                               choices=[
    #                                   ('Passwords', 'Passwords'), 
    #                                   ('NRIC', 'NRIC'), 
    #                                   ('Credit Card Details', 'Credit Card Details')], default='Singapore')
