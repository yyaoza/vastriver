from wtforms import Form, FloatField, validators, SubmitField
import secrets


class MoneyForm(Form):
    amount = FloatField('MoneyAmount')
    amount_minus = SubmitField('MinusAmount')
    amount_add = SubmitField('AddAmount')
    transactionID = secrets.token_hex(4)