import os
from datetime import datetime

import requests
from flask_sqlalchemy import SQLAlchemy

from flask import jsonify, Flask


def db_get_balance(userid):
    dataclass = UserEntry()
    if dataclass.query.filter_by(player_id=userid).all():
        return dataclass.query.filter_by(player_id=userid).all()[0].balance


def db_search_userid(userid):
    dataclass = UserEntry()
    return dataclass.query.filter_by(player_id=userid).all()


def db_check_userid_with_sid(userid, sid):
    sid_class = SidEntry()
    return sid_class.query.filter_by(userID=userid, sid=sid).all()


def db_search_transid(transid):
    dataclass = TransEntry()
    return dataclass.query.filter_by(trans_id=transid).all()


def db_trans_db_exist(transaction):
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

        # write to user db
        user.balance = balance
        the_db.session.commit()

    return balance


def db_new_session_sid(userid, uuid):
    dataclass_sid = SidEntry()
    sid = len(dataclass_sid.query.all()) + 1
    dataclass_sid = SidEntry(userid, sid, uuid)
    the_db.session.add(dataclass_sid)
    the_db.session.commit()
    return sid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://waltyao@localhost/vastriver'
    proxies = ''
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    proxies = {
        "http": os.environ['QUOTAGUARDSTATIC_URL']
    }
    res = requests.get("http://ip.jsontest.com/", proxies=proxies)
    print("!!!!!!!!!!res.text--->", res.text)


the_db = SQLAlchemy(app)
the_db.create_all()
the_db.session.commit()


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


def send_json(status='', sid='', uuid='', balance=''):
    dump = {}
    if status:
        dump["status"] = status
    if sid:
        dump["sid"] = sid
    if balance:
        dump["balance"] = float(balance)
        dump["bonus"] = 0.0
    if uuid:
        dump["uuid"] = uuid
    return jsonify(dump)
