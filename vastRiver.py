from datetime import datetime
import random
import string
import requests
import webbrowser
import xml.etree.ElementTree as xmlTree
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, render_template, flash, Markup
from forms import FundTransferForm, UserAuthenticationForm, OneWalletAddUser, OneWalletFindUser
from theSession import Session

url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
ecID = 'diyft40000000001test123'
ow_url = 'http://10.10.88.42:9092/onewallet'
uaform = ''
ftform = ''
theSession = ''

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
db_sid = SQLAlchemy(app)
# db_sid = SQLAlchemy(app)


# create sid model
class SidEntry(db_sid.Model):
    __tablename__ = 'sessions'
    sid = db_sid.Column(db_sid.String(50), nullable=False, primary_key=True)
    uuid = db_sid.Column(db_sid.String(50), nullable=False, unique=True)
    userID = db_sid.Column(db_sid.String(50), nullable=False)
    date_created = db_sid.Column(db_sid.DateTime, default=datetime.now())

    def __init__(self, userID='', sid='', uuid=''):
        self.sid = sid
        self.uuid = uuid
        self.userID = userID


# create sid model
class UserEntry(db_sid.Model):
    __tablename__ = 'users'
    # sid = db_sid.Column(db_sid.String(50), nullable=False, primary_key=True, unique=True)
    player_id = db_sid.Column(db_sid.String(50))
    balance = db_sid.Column(db_sid.String(50))
    uuid = db_sid.Column(db_sid.String(50), primary_key=True)
    # player_update = db_sid.Column(db_sid.String(50), nullable=False)
    # player_firstName = db_sid.Column(db_sid.String(50), nullable=False)
    # player_lastName = db_sid.Column(db_sid.String(50), nullable=False)
    # player_nickname = db_sid.Column(db_sid.String(50), nullable=False)
    # player_country = db_sid.Column(db_sid.String(50), nullable=False)
    # player_language = db_sid.Column(db_sid.String(50), nullable=False)
    # player_currency = db_sid.Column(db_sid.String(50), nullable=False)
    # game_category = db_sid.Column(db_sid.String(50), nullable=False)
    # game_interface = db_sid.Column(db_sid.String(50), nullable=False)
    date_created = db_sid.Column(db_sid.DateTime, default=datetime.now())

    def __init__(self, player_id='', balance='', uuid=''):
        self.uuid = uuid
        self.player_id = player_id
        self.balance = balance
        # self.player_lastName = player_lastName
        # self.player_nickname = player_nickname
        # self.player_country = player_country
        # self.player_language = player_language
        # self.player_currency = player_currency
        # self.game_category = game_category
        # self.game_interface = game_interface

# if ENV == 'dev':
#     db_sid.create_all()
#     db_sid.session.commit()


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
    find_form = OneWalletFindUser()
    add_form = OneWalletAddUser()

    dataclass = UserEntry()
    if find_form.find_userid.data and find_form.validate_on_submit():
        if not dataclass.query.filter_by(player_id=find_form.userID.data).all():
            flash(Markup('<strong>' + find_form.userID.data + '</strong> not found!'), 'danger')
        else:
            dataclass_sid = SidEntry()
            uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            sid = str(len(dataclass_sid.query.all()) + 1)
            print("sid:" + sid)
            dataclass_sid = SidEntry(find_form.userID.data, sid, uuid)
            db_sid.session.add(dataclass_sid)
            db_sid.session.commit()
            userid = find_form.userID.data
            flash(Markup('SID Created for:' + userid + '<br><strong>sid:' + sid + '</strong><br>uuid:' + uuid),
                  'success')


        # if not dataclass.query.filter_by(userID=form.userID.data).all():
        #     flash(Markup('<strong>' + form.userID.data + '</strong> does not exist!'), 'danger')
        # else:
        #     flash(Markup('<strong>' + form.userID.data + '</strong> found!'), 'success')
        # print('heeeeeere onetime!->>>>' + oneitem)

    if add_form.add_userid.data and add_form.validate_on_submit():
        # dataclass = UserEntry()
        if not dataclass.query.filter_by(player_id=add_form.userID_added.data).all():
            # db.session.delete(dataclass.query.filter_by(userID=form.userID.data).all()[0])
            uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # sid = str(len(dataclass.query.all()) + 1)
            dataclass = UserEntry(add_form.userID_added.data, add_form.balance.data, uuid)
            db_sid.session.add(dataclass)
            db_sid.session.commit()
            flash(
                Markup('<strong>' + add_form.userID_added.data + '</strong> found!' + '<br>balance:'
                       + add_form.balance.data + '<br>uuid:' + uuid), 'success')
        else:
            flash(Markup('<strong>' + add_form.userID_added.data + '</strong> already exists!'), 'danger')

    return render_template('oneWallet.html', ow_findUser_form=find_form, ow_addUser_form=add_form, form=uaform,
                           UA_payload=theSession.UA_payload)


if __name__ == '__main__':
    app.debug = True
    app.run()
