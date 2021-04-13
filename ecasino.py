from flask import Flask, request, Markup, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import FundTransferForm, UserAuthenticationForm, OneWalletForm
from structures import userdataStruct, UA_dataStruct, Session
import requests, webbrowser, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onewallet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize
db = SQLAlchemy(app)
# create db model
class user(db.Model):
    sid = db.Column(db.String(50), nullable=False)
    uuid = db.Column(db.String(50), nullable=False)
    userID = db.Column(db.String(50), primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<userID %r' % self.userID

payload = {
    'cCode': 'xxx',
    'euID': 'yaoza',
    'ecID': 'diyft40000000001test123',
    'eTransID': 'fake_eTransID',
    'output': '1'
}
url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
ecID = 'diyft40000000001test123'

ow_url = 'http://10.10.88.42:9092/onewallet'

UA_payload = UA_dataStruct
# print(UA_payload)
x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)

uaform = ''
ftform = ''
theSession = ''

def casinoCmd(cmd, amount=0):
    if cmd=='GUI':
        payload.update({'cCode': cmd})

    else:
        payload.update({'cCode': cmd,
                        'amount': amount,
                        })

    x = requests.get(url, params=payload)
    return ET.fromstring(x.text)

@app.route('/')
def start():

    global theSession
    theSession = Session(request.host_url)
    global uaform
    uaform = UserAuthenticationForm()

    if uaform.validate_on_submit():
        if uaform.update.data:
            theSession.update_user_info(uaform)
            flash('User Info Updated!', 'success')

    return render_template('editUser.html', form=uaform, UA_payload=theSession.UA_payload)

@app.route('/gameLaunch')
def gameLaunch():

    x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)
    webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])

    return render_template('userinfo.html', UA_payload=theSession.UA_payload, link=theSession.link, form=uaform)

@app.route('/ft', methods=['GET', 'POST'])
def ft():

    form = FundTransferForm()
    global userdata

    if form.validate_on_submit():
        if form.subtract.data:
            flash(form.amount.data + ' funds subtracted', 'warning')
            theSession.ft_subtract(form.amount.data)
        elif form.add.data:
            flash(form.amount.data + ' funds added', 'success')
            theSession.ft_add(form.amount.data)
        else:
            flash('Error:' + form.amount.errors, 'error')

    return render_template('fundTransfer.html', ft_form=form, form=uaform, userdata=theSession.userdata, UA_payload=theSession.UA_payload)

def ft_add(amount):

    form = FundTransferForm()

    print(userdata)

    theSession.ft_add(amount)

    return render_template('fundTransfer.html', form=form, userdata=theSession.userdata, UA_payload=UA_payload)


def ft_subtract(amount):

    form = FundTransferForm()

    theSession.ft_subtract(amount)

    return render_template('fundTransfer.html', form=form, userdata=theSession.userdata, UA_payload=UA_payload)


@app.route('/ow', methods=['GET', 'POST'])
def ow():

    form = OneWalletForm()

    # if form.validate_on_submit():
    #     if form.subtract.data:
    #         flash(form.amount.data + ' funds subtracted', 'warning')
    #         theSession.ft_subtract(form.amount.data)
    #         # ft_subtract(form.amount.data)
    #     elif form.add.data:
    #         flash(form.amount.data + ' funds added', 'success')
    #         # ft_add(form.amount.data)
    #         theSession.ft_add(form.amount.data)
    #     else:
    #         flash('Error:' + form.amount.errors, 'error')

    return render_template('oneWallet.html', ow_form=form, form=uaform, userdata=theSession.userdata,
                           UA_payload=theSession.UA_payload)

if __name__ == '__main__':
    app.debug=True
    app.run()
