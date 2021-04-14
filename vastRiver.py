from datetime import datetime
# from models import User
import random
import string
import requests
import webbrowser
import xml.etree.ElementTree as xmlTree
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import *
# from typing import Callable

from flask import Flask, request, render_template, flash, Markup
from forms import FundTransferForm, UserAuthenticationForm, OneWalletForm
from theSession import Session

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://waltyao@localhost/vastriver'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SECRET_KEY'] = 'shhh its a secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize
db = SQLAlchemy(app)


# create sid model
class SidEntry(db.Model):
    __tablename__ = 'sessions'
    sid = db.Column(db.String(50), nullable=False, primary_key=True, unique=True)
    uuid = db.Column(db.String(50), nullable=False, unique=True)
    userID = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, userID='', sid='', uuid=''):
        self.sid = sid
        self.uuid = uuid
        self.userID = userID


# create sid model
class UserEntry(db.Model):
    __tablename__ = 'users'
    # sid = db.Column(db.String(50), nullable=False, primary_key=True, unique=True)
    uuid = db.Column(db.String(50), nullable=False, unique=True)
    player_id = db.Column(db.String(50), primary_key=True)
    player_update = db.Column(db.String(50), nullable=False)
    player_firstName = db.Column(db.String(50), nullable=False)
    player_lastName = db.Column(db.String(50), nullable=False)
    player_nickname = db.Column(db.String(50), nullable=False)
    player_country = db.Column(db.String(50), nullable=False)
    player_language = db.Column(db.String(50), nullable=False)
    player_currency = db.Column(db.String(50), nullable=False)
    game_category = db.Column(db.String(50), nullable=False)
    game_interface = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, player_id='', sid='', uuid='', player_update='', player_firstName='',
                 player_lastName='', player_nickname='', player_country='', player_language='',
                 player_currency='', game_category='', game_interface=''):
        self.sid = sid
        self.uuid = uuid
        self.player_id = player_id
        self.player_update = player_update
        self.player_firstName = player_firstName
        self.player_lastName = player_lastName
        self.player_nickname = player_nickname
        self.player_country = player_country
        self.player_language = player_language
        self.player_currency = player_currency
        self.game_category = game_category
        self.game_interface = game_interface


db.create_all()
print('ran create all')
# db.session.commit()

url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
ecID = 'diyft40000000001test123'

ow_url = 'http://10.10.88.42:9092/onewallet'

uaform = ''
ftform = ''
theSession = ''


def casinoCmd(cmd, amount=0):
    payload = {
        'cCode': 'xxx',
        'euID': 'yaoza',
        'ecID': 'diyft40000000001test123',
        'eTransID': 'fake_eTransID',
        'output': '1'
    }
    if cmd == 'GUI':
        payload.update({'cCode': cmd})

    else:
        payload.update({'cCode': cmd,
                        'amount': amount,
                        })

    x = requests.get(url, params=payload)
    return xmlTree.fromstring(x.text)


@app.route('/', methods=['GET', 'POST'])
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
    global theSession
    x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=theSession.UA_payload)
    webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])

    return render_template('editUser.html', form=uaform, UA_payload=theSession.UA_payload)


@app.route('/ft', methods=['GET', 'POST'])
def ft():
    global theSession
    theSession.get_user_balance()
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

    return render_template('fundTransfer.html', ft_form=form, form=uaform, UA_payload=theSession.UA_payload)


@app.route('/ow', methods=['GET', 'POST'])
def ow():
    form = OneWalletForm()

    if form.validate_on_submit():
        if form.add_userid.data:
            dataclass = SidEntry()
            if not dataclass.query.filter_by(userID=form.userID.data).all():
                uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                sid = str(len(dataclass.query.all()) + 1)
                dataclass = SidEntry(form.userID.data, sid, uuid)
                db.session.add(dataclass)
                db.session.commit()
                userid = form.userID.data
                flash(Markup('<strong>Created:</strong><br>userid:'+userid+'<br>sid:'+sid+'<br>uuid:'+uuid), 'success')
            else:
                flash(Markup('<strong>' + form.userID.data + '</strong> already exists!'), 'danger')

            # if not dataclass.query.filter_by(userID=form.userID.data).all():
            #     flash(Markup('<strong>' + form.userID.data + '</strong> does not exist!'), 'danger')
            # else:
            #     flash(Markup('<strong>' + form.userID.data + '</strong> found!'), 'success')
            # print('heeeeeere onetime!->>>>' + oneitem)

        elif form.find_userid.data:
            dataclass = SidEntry()
            if not dataclass.query.filter_by(userID=form.userID.data).all():
                flash(Markup('<strong>' + form.userID.data + '</strong> does not exist!'), 'danger')
            else:
                # db.session.delete(dataclass.query.filter_by(userID=form.userID.data).all()[0])
                uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                sid = str(len(dataclass.query.all()) + 1)
                dataclass = SidEntry(form.userID.data, sid, uuid)
                db.session.add(dataclass)
                db.session.commit()
                userid = form.userID.data
                flash(Markup('<strong>' + form.userID.data + '</strong> found!'+'<br>sid:'+sid+'<br>uuid:'+uuid), 'success')

    return render_template('oneWallet.html', ow_form=form, form=uaform, UA_payload=theSession.UA_payload)


if __name__ == '__main__':
    app.debug = True
    app.run()
