from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', 
                          choices=[('donor', 'Donor'), ('requester', 'Requester')],
                          validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DonationForm(FlaskForm):
    blood_type = SelectField('Blood Type',
                           choices=[('A+', 'A+'), ('A-', 'A-'), 
                                  ('B+', 'B+'), ('B-', 'B-'),
                                  ('AB+', 'AB+'), ('AB-', 'AB-'),
                                  ('O+', 'O+'), ('O-', 'O-')],
                           validators=[DataRequired()])
    quantity = FloatField('Quantity (units)', validators=[DataRequired()])
    submit = SubmitField('Submit Donation')

class RequestForm(FlaskForm):
    blood_type = SelectField('Blood Type',
                           choices=[('A+', 'A+'), ('A-', 'A-'), 
                                  ('B+', 'B+'), ('B-', 'B-'),
                                  ('AB+', 'AB+'), ('AB-', 'AB-'),
                                  ('O+', 'O+'), ('O-', 'O-')],
                           validators=[DataRequired()])
    quantity = FloatField('Quantity (units)', validators=[DataRequired()])
    urgency = SelectField('Urgency Level',
                        choices=[('high', 'High'), 
                                ('medium', 'Medium'),
                                ('low', 'Low')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit Request') 