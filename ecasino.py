from flask import Flask, request, Markup, render_template, url_for, flash, redirect
from forms import FundTransferForm, UserAuthenticationForm
from structures import userdataStruct, UA_dataStruct, Session
import requests, webbrowser, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'

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
# print(x.text)
launchLink = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']

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

def getUserInfo():
    gui = casinoCmd('GUI')
    # rwa = casinoCmd('RWA')

    # global userdata
    # userdata.update({
    #     'emailaddress': gui[0].text,
    #     'screenname': gui[3].text,
    #     'countrycode': gui[4].text,
    #     'firstName': gui[1].text,
    #     'lastName': gui[2].text,
    #     # 'balance': rwa[3].text,
    #     'euid': gui[6].text,
    #     'uid': gui[5].text,
    # })
    #
    # print("*Getting userdata", userdata, sep="---->")
    global UA_payload
    # UA_payload.clear()
    UA_payload = UA_dataStruct
    UA_payload['player']['firstName'] = gui[1].text
    UA_payload['player']['lastName'] = gui[2].text
    UA_payload['player']['nickname'] = gui[3].text
    UA_payload['player']['country'] = gui[4].text
    UA_payload['player']['update'] = False
    UA_payload['uuid'] = gui[5].text
    UA_payload['player']['id'] = gui[6].text
    # UApayload['player']['language'] = form.language.data
    # UApayload['player']['update'] = True
    UA_payload['config']['urls']['cashier'] = request.host_url
    # UApayload['config']['game']['category'] = form.game.data

    return
    # for things in gui:
    #     print("*Getting GUI call", things.text, sep="---->")

@app.route('/')
def start():

    global theSession
    theSession = Session(request.host_url)
    # theSession.get_user_info()
    # getUserInfo()
    global uaform
    uaform = UserAuthenticationForm()

    # launchLink = theSession.get_link()
    # x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)
    # launchLink = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']

    return render_template('userinfo.html', UA_payload=theSession.UA_payload, link=theSession.link, form=uaform)


@app.route('/updateInfo', methods=['GET', 'POST'])
def updateInfo():
    # global UApayload
    # UA_payload = UA_dataStruct
    # form = UserAuthenticationForm()
    # x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)
    # launchLink = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']

    global theSession
    uaform = UserAuthenticationForm()
    # uaform.firstName.data = theSession.UA_payload['player']['firstName']
    # uaform.lastName.data = theSession.UA_payload['player']['lastName']
    # uaform.nickName.data = theSession.UA_payload['player']['nickname']
    # uaform.country.data = theSession.UA_payload['player']['country']
    if uaform.validate_on_submit():
        if uaform.update.data:
            print('**Update button pressed --->' + uaform.firstName.data)
            theSession.update_user_info(uaform)
            #
            # global UApayload
            # UA_payload = UA_dataStruct
            # UA_payload['player']['firstName'] = form.firstName.data
            # UA_payload['player']['lastName'] = form.lastName.data
            # UA_payload['player']['nickname'] = form.nickName.data
            # UA_payload['player']['country'] = form.country.data
            # UA_payload['player']['language'] = form.language.data
            # UA_payload['player']['update'] = True
            # UA_payload['config']['urls']['cashier'] = request.host_url`
            # UA_payload['config']['game']['category'] = form.game.data
            #
            # x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)
            # link = 'https://diyft4.uat1.evo-test.com' + x.json()['entry']
            # print("*Writing payload", UA_payload, sep="---->")

            # getUserInfo()
            # webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])
            # flash(Markup('Game link: <a href=\"https://diyft4.uat1.evo-test.com' + x.json()['entry'] + "\" class=\"alert-link\">Click here</a>"), 'success')
            flash('User Info Updated!', 'success')

    return render_template('editUser.html', form=uaform, UA_payload=theSession.UA_payload, link=theSession.link)

@app.route('/gameLaunch')
def gameLaunch():
    # uaform = UserAuthenticationForm()
    # theSession.UA_payload['player']['language'] = uaform.language.data
    # theSession.UA_payload.update({
    # 'config': {
    # 'brand': {
    #   'skin': '1'
    # },
    # 'game': {
    #   'category': uaform.game.data,
    #   'interface': 'view1'
    #
    # },
    # 'channel': {
    #   'wrapped': False,
    #   'mobile': False
    # },
    # 'urls': {
    #   'cashier': request.host_url, # assigned by licensee
    #   'responsibleGaming': 'http://www.RGam.ee', # assigned by licensee
    #   'lobby': 'http://www.lobb.ee', # assigned by licensee
    #   'sessionTimeout': 'http://www.sesstm.ee' # assigned by licensee
    # },
    # 'freeGames': False
    # }})

    x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UA_payload)
    webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])

    return render_template('userinfo.html', UA_payload=theSession.UA_payload, link=theSession.link, form=uaform)

@app.route('/ft', methods=['GET', 'POST'])
def ft():

    form = FundTransferForm()
    # rwa = casinoCmd('RWA')
    global userdata
    # userdata['balance'] = rwa[3].text

    if form.validate_on_submit():
        if form.subtract.data:
            flash(form.amount.data + ' funds subtracted', 'warning')
            theSession.ft_subtract(form.amount.data)
            # ft_subtract(form.amount.data)
        elif form.add.data:
            flash(form.amount.data + ' funds added', 'success')
            # ft_add(form.amount.data)
            theSession.ft_add(form.amount.data)
        else:
            flash('Error:' + form.amount.errors, 'error')

    return render_template('fundTransfer.html', ft_form=form, form=uaform, userdata=theSession.userdata, UA_payload=theSession.UA_payload, link=theSession.link)

def ft_add(amount):

    form = FundTransferForm()
    ecr = casinoCmd('ECR', amount)

    userdata.update({
        'balance': ecr[0].text,
        'etransid': ecr[1].text,
        'transid': ecr[2].text,
        'datetime': ecr[3].text
    })
    print(userdata)

    return render_template('fundTransfer.html', form=form, userdata=userdata, UA_payload=UA_payload, link=launchLink)


def ft_subtract(amount):

    form = FundTransferForm()
    edb = casinoCmd('EDB', amount)

    userdata.update({
        'balance': edb[0].text,
        'etransid': edb[1].text,
        'transid': edb[2].text,
        'datetime': edb[3].text
    })

    return render_template('fundTransfer.html', form=form, userdata=userdata, UA_payload=UA_payload, link=launchLink)


@app.route('/ow', methods=['GET', 'POST'])
def ow():

    userdata = {
            'balance': '1',
            'etransid': '2',
            'transid': '3',
            'datetime': 'em4pty',
            'euid': '5',
            'uid': '6'
            }
    form = FundTransferForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('oneWallet.html', form=form, userdata=userdata)


if __name__ == '__main__':
    app.run(debug=True)
