from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Regexp


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
