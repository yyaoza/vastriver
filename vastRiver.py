from datetime import datetime
import os
import json
import random
import string
import requests
import webbrowser
import xml.etree.ElementTree as xmlTree
from flask_sqlalchemy import SQLAlchemy

import userAuth
from flask import Flask, request, render_template, flash, Markup, jsonify
from forms import FundTransferForm, UserAuthenticationForm, OneWalletAddUser, OneWalletFindUser

url = 'https://diyft4.uat1.evo-test.com/api/ecashier'
ecID = 'diyft40000000001test123'
ow_url = 'http://10.10.88.42:9092/onewallet'
uaform = None
ftform = None
theSession = None

app = Flask(__name__)

# ENV = 'dev'
# if ENV == 'dev':
#     app.debug = True
# else:
#     app.debug = False

# production db
# postgres://rtdjyavocrnvgd:adfc33630f7ec16f6d7a366b0bd90539b0f381415f382a0231fcac1be2d25f52@ec2-54-205-183-19.compute-1.amazonaws.com:5432/d125pokplf1vlb

app.config['SECRET_KEY'] = 'shhh its a secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://waltyao@localhost/vastriver'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# initialize
the_db = SQLAlchemy(app)


class TransEntry(the_db.Model):
    __tablename__ = 'transactions'
    id = the_db.Column(the_db.Integer, primary_key=True)
    type = the_db.Column(the_db.String(50), nullable=False)
    trans_id = the_db.Column(the_db.String(50), nullable=False)
    ref_id = the_db.Column(the_db.String(50), nullable=False)
    user_id = the_db.Column(the_db.String(50), nullable=False)
    uuid = the_db.Column(the_db.String(50), nullable=False)
    settled = the_db.Column(the_db.Boolean, nullable=False)
    date_created = the_db.Column(the_db.DateTime, default=datetime.now())

    def __init__(self, trans_type='', user_id='', trans_id='', ref_id='', uuid='', settled=''):
        self.type = trans_type
        self.ref_id = ref_id
        self.trans_id = trans_id
        self.uuid = uuid
        self.user_id = user_id
        self.settled = settled


class SidEntry(the_db.Model):
    __tablename__ = 'sessions'
    sid = the_db.Column(the_db.Integer, nullable=False, primary_key=True)
    uuid = the_db.Column(the_db.String(50), nullable=False)
    userID = the_db.Column(the_db.String(50), nullable=False)
    date_created = the_db.Column(the_db.DateTime, default=datetime.now())

    def __init__(self, userID='', sid=0, uuid=''):
        self.sid = sid
        self.uuid = uuid
        self.userID = userID


class UserEntry(the_db.Model):
    __tablename__ = 'users'
    # sid = db_sid.Column(db_sid.String(50), nullable=False, primary_key=True, unique=True)
    player_id = the_db.Column(the_db.String(50), primary_key=True)
    balance = the_db.Column(the_db.String(50))
    # uuid = the_db.Column(the_db.String(50))
    date_created = the_db.Column(the_db.DateTime, default=datetime.now())

    def __init__(self, player_id='', balance=''):
        # self.uuid = uuid
        self.player_id = player_id
        self.balance = balance


the_db.create_all()
the_db.session.commit()


def get_user_info(cmd, amount=0):
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


def db_search_userid(userid):
    dataclass = UserEntry()
    return dataclass.query.filter_by(player_id=userid).all()


def db_check_userid_with_sid(userid, sid):
    sid_class = SidEntry()
    return sid_class.query.filter_by(userID=userid, sid=sid).all()
    # max_value = None
    # for x in the_list:
    #     if max_value is None or x.sid > max_value:
    #         max_value = x.sid
    # if max_value is int(sid):
    #     return True
    # else:
    #     return False


def db_search_transid(transid):
    dataclass = TransEntry()
    return dataclass.query.filter_by(trans_id=transid).all()


# only for debits
def db_trans_db_exist(transaction):
    # ref id
    # the_list = TransEntry().query.filter_by(type='Debit', ref_id=transaction['refId']).all()
    # if len(the_list) > 0:
    #     return not the_list[len(the_list)-1].settled
    # trans id
    the_list = TransEntry().query.filter_by(type='Debit', trans_id=transaction['id']).all()
    if len(the_list) > 0:
        return not the_list[len(the_list) - 1].settled

    return False


def db_trans_settled_by_cancel(id_num):
    trans_list = TransEntry().query.filter_by(type='Debit', trans_id=id_num).all()
    if trans_list[len(trans_list) - 1].settled:
        return True
    else:
        trans_list[len(trans_list) - 1].settled = True
        the_db.session.commit()
        return False


def db_trans_settled(trans_type, id_num):
    # write into the settled field
    trans_list = TransEntry().query.filter_by(type=trans_type, ref_id=id_num).all()

    # transid_list = TransEntry().query.filter_by(type='Debit', ref_id=transaction['id']).all()
    # get the last one and see if it's been settled
    if len(trans_list) > 0:
        if trans_list[len(trans_list) - 1].settled:
            return True
        else:
            # it will be settled now
            trans_list[len(trans_list) - 1].settled = True
            the_db.session.commit()
            return False
    else:
        return False


def db_trans_exist(trans_type, id_num):
    # write into the settled field for the credit
    trans_list = TransEntry().query.filter_by(type=trans_type, trans_id=id_num).all()

    return len(trans_list) > 0


def db_new_trans_dbcr(cr_or_db, userid, request_data, uuid):
    if cr_or_db == 'Debit':
        transaction = TransEntry(cr_or_db, userid, request_data['transaction']['id'],
                                 request_data['transaction']['refId'],
                                 uuid, False)
    else:
        transaction = TransEntry(cr_or_db, userid, request_data['transaction']['id'],
                                 request_data['transaction']['refId'],
                                 uuid, True)
    the_db.session.add(transaction)
    the_db.session.commit()


def db_new_user_dbcr(cr_or_db, userid, request_data):
    user = UserEntry().query.filter_by(player_id=userid).all()[0]
    if cr_or_db:
        balance = round(float(user.balance) + request_data['transaction']['amount'], 2)
    else:
        balance = round(float(user.balance) - request_data['transaction']['amount'], 2)

    if balance >= 0:
        if cr_or_db:
            trans_type = 'Credit'
        else:
            trans_type = 'Debit'

        # write to user db
        user.balance = balance
        the_db.session.commit()

    return balance


def db_new_session_sid(userid, uuid):
    dataclass_sid = SidEntry()
    # find_form = OneWalletFindUser()
    sid = len(dataclass_sid.query.all()) + 1
    # print("sid:" + sid)
    # uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    dataclass_sid = SidEntry(userid, sid, uuid)
    the_db.session.add(dataclass_sid)
    the_db.session.commit()
    return sid


def db_get_balance(userid):
    dataclass = UserEntry()
    if dataclass.query.filter_by(player_id=userid).all():
        return dataclass.query.filter_by(player_id=userid).all()[0].balance


def send_json(status='', sid='', uuid='', balance=''):
    dump = {}
    if status:
        dump["status"] = status
    if sid:
        dump["sid"] = sid
    if balance:
        dump["balance"] = balance
        dump["bonus"] = 0.0
    if uuid:
        dump["uuid"] = uuid
    return jsonify(dump)


def valid_token_id(valid=True):
    if valid:
        if 'authToken' in request.args and request.args['authToken'] == 's3cr3tV4lu3':
            return True
        else:
            return False
    else:
        return send_json('INVALID_TOKEN_ID')


def valid_user(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        if 'userId' in request_data:
            return request_data['userId']
        else:
            return False

    else:
        return send_json('INVALID_PARAMETER')


def match_userid_sid(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        if db_search_userid(request_data['userId']):
            return request_data['userId']
        else:
            return False
    else:
        return send_json('INVALID_PARAMETER')


def valid_check_user(userid, uuid):
    request_data = request.get_json(force=True)

    if db_check_userid_with_sid(userid, request_data['sid']):
        return send_json("OK", request_data['sid'], uuid)
    else:
        return send_json('INVALID_PARAMETER')


def valid_uuid(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        if 'uuid' in request_data:
            return request_data['uuid']
        else:
            return False

    else:
        return send_json('INVALID_PARAMETER')


def valid_sid(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'sid' in request_data
    else:
        return send_json('INVALID_SID')


def valid_channel(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'channel' in request_data and 'type' in request_data['channel']

    else:
        return send_json('INVALID_PARAMETER')


def valid_game(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'game' in request_data

    else:
        return send_json('INVALID_PARAMETER')


def valid_currency(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'currency' in request_data
    else:
        return send_json('INVALID_PARAMETER')


def valid_transaction(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'transaction' in request_data

    else:
        return send_json('INVALID_PARAMETER')


def valid_amount(valid=True):
    if valid:
        request_data = request.get_json(force=True)

        return 'amount' in request_data['transaction']

    else:
        return send_json('INVALID_PARAMETER')


def valid_cancel(userid='', uuid=''):
    request_data = request.get_json(force=True)
    # check if bet exists (match id and if settled = false)
    if not db_trans_exist('Debit', request_data['transaction']['id']):
        return send_json('BET_DOES_NOT_EXIST')

    # check if the debit has been settled
    if db_trans_settled_by_cancel(request_data['transaction']['id']):
        return send_json('BET_ALREADY_SETTLED')
    else:
        # write to user db
        balance = db_new_user_dbcr(True, userid, request_data)
        # write to transaction db
        db_new_trans_dbcr('Cancel', userid, request_data, uuid)
        return send_json("OK", False, uuid, '${:,.2f}'.format(balance))


def valid_credit(userid='', uuid=''):
    request_data = request.get_json(force=True)
    # check if the debit has been settled
    if db_trans_settled('Debit', request_data['transaction']['refId']):
        return send_json('BET_ALREADY_SETTLED')
    else:
        # write to user db
        balance = db_new_user_dbcr(True, userid, request_data)
        # write to transaction db
        db_new_trans_dbcr('Credit', userid, request_data, uuid)
        return send_json("OK", False, uuid, '${:,.2f}'.format(balance))
        # {'balance': '${:,.2f}'.format(balance), 'valid': 0}


def valid_debit(userid='', uuid=''):
    request_data = request.get_json(force=True)
    # check if a debit already exists
    if db_trans_db_exist(request_data['transaction']):
        return send_json('BET_ALREADY_EXIST')
    else:
        # db cr from user db and check for insufficient funds
        balance = db_new_user_dbcr(False, userid, request_data)
        if balance >= 0:
            # write to transaction db
            db_new_trans_dbcr('Debit', userid, request_data, uuid)
            return send_json("OK", False, uuid, '${:,.2f}'.format(balance))
            # {'balance': '${:,.2f}'.format(balance), 'valid': 0}
        else:
            return send_json('INSUFFICIENT_FUNDS')


@app.route('/api/credit', methods=['POST'])
def credit():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():
            if valid_sid():
                userid = match_userid_sid()
                if userid:
                    if valid_game():
                        if valid_currency():
                            if valid_transaction():
                                uuid = valid_uuid()
                                if uuid:
                                    if valid_amount():
                                        return valid_credit(userid, uuid)
                                    else:
                                        return valid_amount(False)
                                else:
                                    return valid_uuid(False)
                            else:
                                return valid_transaction(False)
                        else:
                            return valid_currency(False)
                    else:
                        return valid_game(False)
                else:
                    return match_userid_sid(False)
            else:
                return valid_sid(False)
        else:
            return valid_token_id(False)


@app.route('/api/cancel', methods=['POST'])
def cancel():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():
            if valid_sid():
                userid = match_userid_sid()
                if userid:
                    if valid_game():
                        if valid_currency():
                            if valid_transaction():
                                uuid = valid_uuid()
                                if uuid:
                                    if valid_amount():
                                        return valid_cancel(userid, uuid)
                                else:
                                    return valid_uuid(False)
                            else:
                                return valid_transaction(False)
                        else:
                            return valid_currency(False)
                    else:
                        return valid_game(False)
                else:
                    return match_userid_sid(False)
            else:
                return valid_sid(False)
        else:
            return valid_token_id(False)


@app.route('/api/debit', methods=['POST'])
def debit():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():
            if valid_sid():
                userid = match_userid_sid()
                if userid:
                    if valid_game():
                        if valid_currency():
                            if valid_transaction():
                                uuid = valid_uuid()
                                if uuid:
                                    if valid_amount():
                                        # balance_status = {'balance': 0, 'valid': 0}
                                        # balance_status = valid_debit(userid, balance_status)
                                        # if balance_status['valid'] == 0:
                                        return valid_debit(userid, uuid)
                                    # else:
                                    #     return valid_debit(userid, balance_status['valid'])
                                    else:
                                        return valid_amount(False)
                                else:
                                    return valid_uuid(False)
                            else:
                                return valid_transaction(False)
                        else:
                            return valid_currency(False)
                    else:
                        return valid_game(False)
                else:
                    return match_userid_sid(False)
            else:
                return valid_sid(False)
        else:
            return valid_token_id(False)


@app.route('/api/balance', methods=['POST'])
def get_balance():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():
            if valid_sid():
                userid = match_userid_sid()
                if userid:
                    if valid_game():
                        if valid_currency():
                            uuid = valid_uuid()
                            if uuid:
                                return send_json("OK", False, uuid, db_get_balance(userid))
                            else:
                                return valid_uuid(False)
                        else:
                            return valid_currency(False)
                    else:
                        return valid_game(False)
                else:
                    return match_userid_sid(False)
            else:
                return valid_sid(False)
        else:
            return valid_token_id(False)


@app.route('/api/sid', methods=['POST'])
def sid_user():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():

            userid = valid_user()
            if userid:
                if valid_channel():
                    uuid = valid_uuid()
                    if uuid:
                        if valid_sid():
                            sid = db_new_session_sid(userid, uuid)
                            return send_json("OK", sid, uuid)
                        else:
                            return valid_sid(False)
                    else:
                        return valid_uuid(False)
                else:
                    return valid_channel(False)
            else:
                return valid_user(False)

        else:
            return valid_token_id(False)


@app.route('/api/check', methods=['POST'])
def check_user():
    # handle the POST request
    if request.method == 'POST':
        if valid_token_id():
            if valid_sid():
                if valid_channel():
                    uuid = valid_uuid()
                    if uuid:
                        userid = valid_user()
                        if userid:
                            return valid_check_user(userid, uuid)
                        else:
                            return valid_user(False)
                    else:
                        return valid_uuid(False)
                else:
                    return valid_channel(False)
            else:
                return valid_sid(False)
        else:
            return valid_token_id(False)


@app.route('/api/rb', methods=['GET', 'POST'])
def rb():
    if not UserEntry().query.filter_by(player_id='walt').all():
        print('test')
        user = UserEntry('walt', '1000')
        the_db.session.add(user)
    if not UserEntry().query.filter_by(player_id='jim').all():
        user = UserEntry('jim', '1000')
        the_db.session.add(user)
    the_db.session.commit()
    return 'done'


@app.route('/', methods=['GET', 'POST'])
def start():
    global theSession
    theSession = userAuth.UA2(request.host_url)
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
        if not db_search_userid(find_form.userID.data):
            flash(Markup('<strong>' + find_form.userID.data + '</strong> not found!'), 'danger')
        else:
            dataclass_sid = SidEntry()
            uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            sid = str(len(dataclass_sid.query.all()) + 1)
            print("sid:" + sid)
            dataclass_sid = SidEntry(find_form.userID.data, sid, uuid)
            the_db.session.add(dataclass_sid)
            the_db.session.commit()
            userid = find_form.userID.data
            flash(Markup('SID Created for:' + userid + '<br><strong>sid:' + sid + '</strong><br>uuid:' + uuid),
                  'success')

    if add_form.add_userid.data and add_form.validate_on_submit():
        if not db_search_userid(find_form.userID.data):
            # db.session.delete(dataclass.query.filter_by(userID=form.userID.data).all()[0])
            uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            # sid = str(len(dataclass.query.all()) + 1)
            dataclass = UserEntry(add_form.userID_added.data, add_form.balance.data)
            the_db.session.add(dataclass)
            the_db.session.commit()
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

