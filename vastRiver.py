import random
import string
import requests
import webbrowser
import solana
from solana.rpc.api import Client
from os import listdir
from os.path import isfile, join
import pathlib

import userAuth
from flask import request, render_template, flash, Markup, jsonify
from data import db_get_balance, db_search_userid, db_new_session_sid, SidEntry, UserEntry, send_json, the_db, app
from forms import FundTransferForm, UserAuthenticationForm, OneWalletAddUser, OneWalletFindUser, ConnectWallet
from oneWallet import valid_cancel, valid_credit, valid_debit
from valid import valid_token_id, valid_user, match_userid_sid, valid_check_user, valid_uuid, valid_sid, \
    valid_channel, valid_game, valid_currency, valid_transaction, valid_amount

uaform = None
ftform = None
theSession = None
iframe_game_toggle = False
stream = ''
datastream = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    current_path = 'static/icons/top_games/'
    icon_files = [f for f in listdir(current_path) if isfile(join(current_path, f)) and not f.endswith('.DS_Store')]
    icon_files = [current_path + sub for sub in icon_files]

    # myColours = request.form.get('login', type=object)
    # connect to wallet
    if request.method == 'POST':
        if 'login' in request.form:
            myColours = request.form.get('login')
            http_client = Client("https://api.devnet.solana.com")

    return render_template('gallery.html', which_tab=request.url.rsplit('/', 1)[1], icon_files=icon_files,
                           num_icons=len(icon_files)-1)


@app.route('/sports', methods=['GET', 'POST'])
def sports():
    current_path = 'static/icons/sports/'
    icon_files = [f for f in listdir(current_path) if isfile(join(current_path, f)) and not f.endswith('.DS_Store')]
    icon_files = [current_path + sub for sub in icon_files]

    return render_template('sports.html', which_tab=request.url.rsplit('/', 1)[1], form=uaform)


@app.route('/slots', methods=['GET', 'POST'])
def slots():
    current_path = 'static/icons/slots/'
    icon_files = [f for f in listdir(current_path) if isfile(join(current_path, f)) and not f.endswith('.DS_Store')]
    icon_files = [current_path + sub for sub in icon_files]

    return render_template('gallery.html', which_tab=request.url.rsplit('/', 1)[1], form=uaform, icon_files=icon_files,
                           num_icons=len(icon_files)-1)


@app.route('/live', methods=['GET', 'POST'])
def live():
    current_path = 'static/icons/live/'
    icon_files = [f for f in listdir(current_path) if isfile(join(current_path, f)) and not f.endswith('.DS_Store')]
    icon_files = [current_path + sub for sub in icon_files]

    return render_template('gallery.html', which_tab=request.url.rsplit('/', 1)[1], form=uaform, icon_files=icon_files,
                           num_icons=len(icon_files)-1)


@app.route('/ft', methods=['GET', 'POST'])
def ft():
    # which_tabs = request.url.rsplit('/', 1)[1]
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

    return render_template('fundTransfer.html', which_tab=request.url.rsplit('/', 1)[1], ft_form=form, form=uaform,
                           UA_payload=theSession.UA_payload)


@app.route('/ow', methods=['GET', 'POST'])
def ow():
    # global which_tab
    # which_tab =
    find_form = OneWalletFindUser()
    add_form = OneWalletAddUser()

    # dataclass = UserEntry()
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
            uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            dataclass = UserEntry(add_form.userID_added.data, add_form.balance.data)
            the_db.session.add(dataclass)
            the_db.session.commit()
            flash(
                Markup('<strong>' + add_form.userID_added.data + '</strong> found!' + '<br>balance:'
                       + add_form.balance.data + '<br>uuid:' + uuid), 'success')
        else:
            flash(Markup('<strong>' + add_form.userID_added.data + '</strong> already exists!'), 'danger')

    return render_template('oneWallet.html', which_tab=request.url.rsplit('/', 1)[1], ow_findUser_form=find_form,
                           ow_addUser_form=add_form, form=uaform, UA_payload=theSession.UA_payload)


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
                                        return valid_debit(userid, uuid)
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


@app.route('/settings', methods=['GET', 'POST'])
def start():
    global which_tab
    which_tab = 'home'
    global theSession
    theSession = userAuth.UA2(request.host_url)
    global uaform
    uaform = UserAuthenticationForm()
    # requests.close()

    if uaform.validate_on_submit():
        if uaform.update.data:
            theSession.update_user_info(uaform)
            flash('User Info Updated!', 'success')

    return render_template('editUser.html', which_tab=which_tab, form=uaform, UA_payload=theSession.UA_payload)


@app.route('/game_window')
def game_window():
    global theSession
    if 'table' in theSession.UA_payload['config']['game']:
        theSession.UA_payload['config']['game']['table']['id'] = ''
    ua_url = theSession.url + '/ua/v1/' + theSession.casino_id + '/' + theSession.auth_key
    x = requests.post(ua_url, json=theSession.UA_payload)
    webbrowser.open(theSession.url + x.json()['entry'])

    return render_template('editUser.html', form=uaform, UA_payload=theSession.UA_payload)


@app.route('/game_window_slots')
def game_window_slots():
    global theSession
    if 'table' in theSession.UA_payload['config']['game']:
        theSession.UA_payload['config']['game']['table']['id'] = 'streetfighter200'

    theSession.UA_payload['config']['game']['category'] = 'slots'
    ua_url = theSession.url + '/ua/v1/' + theSession.casino_id + '/' + theSession.auth_key
    x = requests.post(ua_url, json=theSession.UA_payload)
    webbrowser.open(theSession.url + x.json()['entry'])

    return render_template('editUser.html', form=uaform, UA_payload=theSession.UA_payload)


@app.route('/mini_roulette')
def mini_roulette():
    global theSession
    global iframe_game_toggle
    if iframe_game_toggle:
        iframe_game_toggle = False
    else:
        iframe_game_toggle = True

    theSession.mini_roulette()
    # mini_roulette_payload = theSession.UA_payload
    #
    # mini_roulette_payload['config']['game']['table'] = {'id': 'pegck3qfanmqbgbh'}
    #
    # x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=mini_roulette_payload)
    # theSession.UA_payload['game_url'] = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']

    return render_template('game_iframe.html', launch_game=iframe_game_toggle, form=uaform,
                           UA_payload=theSession.UA_payload)


@app.route('/daily_report', methods=['GET', 'POST'])
def daily_report():
    report = theSession.daily_report()

    return render_template('daily_report.html', len=len(report), daily_report=report,
                           which_tab=request.url.rsplit('/', 1)[1], form=uaform, UA_payload=theSession.UA_payload)


@app.route('/direct_game_launch', methods=['GET', 'POST'])
def direct_game_launch():
    game_launch_info = theSession.direct_game_launch()

    return render_template('direct_game_launch.html', len=len(game_launch_info), game_launch_info=game_launch_info,
                           which_tab=request.url.rsplit('/', 1)[1], form=uaform, UA_payload=theSession.UA_payload)


@app.route('/game_stream', methods=['GET', 'POST'])
def game_stream():
    global datastream
    datastream.clear()
    stream = 'Waiting for game data...'
    waiting = 'Waiting for game data...'

    return render_template('game_stream.html', datastream=stream, which_tab=request.url.rsplit('/', 1)[1], form=uaform,
                           UA_payload=theSession.UA_payload)


@app.route('/update_stream', methods=['POST'])
def update_stream():
    global datastream
    datastream[theSession.game_stream()['id']] = theSession.game_stream()
    # walt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    return jsonify("", render_template('input_stream.html', datastream=datastream, count=len(datastream)))


if __name__ == '__main__':
    app.debug = True
    app.run()
