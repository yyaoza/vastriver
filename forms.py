from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired


class RegistrationForm:
    username = StringField('Amount')
    email = StringField('Email')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Sign Up')


class FundTransferForm(FlaskForm):
    username = StringField('Amount')
    email = StringField('E-mail')
    password = PasswordField('Password')
    remember = BooleanField('Remember Me')
    amount = StringField('Amount', validators=[InputRequired()])
    add = SubmitField('+')
    subtract = SubmitField('-')


class UserAuthenticationForm(FlaskForm):
    key = 'diyft40000000001'
    token = 'test123'
    hostname = 'diyft4.uat1.evo-test.com'