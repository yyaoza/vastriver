from flask import Flask, request, Markup, render_template, url_for, flash, redirect
from forms import FundTransferForm, UserAuthenticationForm
import requests, webbrowser, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'

userdata = {
    'emailaddress': 'x',
    'screenname': 'x',
    'countrycode': 'x',
    'firstName': 'x',
    'lastName': 'x',
    'balance': '0.0',
    'etransid': '###',
    'transid': '###',
    'datetime': '###',
    'euid': 'x',
    'uid': 'x',
}

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

UApayload = {
    'uuid': 'random', # assigned, should be uid
    'player': {
        'id': 'yaoza', # assigned by licensee, should be euid
        'update': False,
        'firstName': 'firstName', # assigned
        'lastName': 'lastName', # assigned
        'nickname': 'nickname', # assigned
        'country': 'DE', # assigned
        'language': 'fr', # assigned
        'currency': 'CNY', # assigned
        'session': {
          'id': '111ssss3333rrrrr45555', # assigned by licensee
          'ip': '192.168.0.1' # assigned
        }
    },
    'config': {
        'brand': {
          'skin': '1'
        },
        'game': {
          'category': 'roulette',
          'interface': 'view1'

        },
        'channel': {
          'wrapped': False,
          'mobile': False
        },
        'urls': {
          'cashier': 'http://www.chs.ee', # assigned by licensee
          'responsibleGaming': 'http://www.RGam.ee', # assigned by licensee
          'lobby': 'http://www.lobb.ee', # assigned by licensee
          'sessionTimeout': 'http://www.sesstm.ee' # assigned by licensee
        },
        'freeGames': False
  }
}

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

    gui = casinoCmd('GUI')
    # rwa = casinoCmd('RWA')

    # global userdata
    userdata.update({
        'emailaddress': gui[0].text,
        'screenname': gui[3].text,
        'countrycode': gui[4].text,
        'firstName': gui[1].text,
        'lastName': gui[2].text,
        # 'balance': rwa[3].text,
        'euid': gui[6].text,
        'uid':  gui[5].text,
        })

    UApayload['player']['firstName'] = gui[1].text
    UApayload['player']['lastName'] = gui[2].text
    UApayload['player']['nickName'] = gui[3].text
    UApayload['player']['country'] = gui[4].text
    UApayload['uuid'] = gui[5].text
    UApayload['player']['id'] = gui[6].text
    # UApayload['player']['language'] = form.language.data
    # UApayload['player']['update'] = True
    UApayload['config']['urls']['cashier'] = request.host_url
    # UApayload['config']['game']['category'] = form.game.data

    x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UApayload)
    # flash(Markup('Game link: <a href=\"https://diyft4.uat1.evo-test.com' + x.json()['entry'] + "\" class=\"alert-link\">Click here</a>"), 'success')

    return render_template('userinfo.html', userdata=userdata)


@app.route('/preLaunch', methods=['GET', 'POST'])
def preLaunch():

    form = UserAuthenticationForm()

    # form.firstName.data = userdata['firstName']
    # form.lastName.data = userdata['lastName']
    # form.nickName.data = userdata['screenname']
    # form.country.data = userdata['countrycode']

    if form.validate_on_submit():
        if form.update.data:
            print(form.firstName.data)
            UApayload['player']['firstName'] = form.firstName.data
            UApayload['player']['lastName'] = form.lastName.data
            UApayload['player']['nickName'] = form.nickName.data
            UApayload['player']['country'] = form.country.data
            UApayload['player']['language'] = form.language.data
            UApayload['player']['update'] = True
            UApayload['config']['urls']['cashier'] = request.host_url
            UApayload['config']['game']['category'] = form.game.data

            x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UApayload)
            print(UApayload)
            # webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])
            flash(Markup('Game link: <a href=\"https://diyft4.uat1.evo-test.com' + x.json()['entry'] + "\" class=\"alert-link\">Click here</a>"), 'success')

    return render_template('userAuthentication.html', form=form, userdata=userdata)


def ua():

    UApayload.update({
    'config': {
    'brand': {
      'skin': '1'
    },
    'game': {
      'category': 'roulette',
      'interface': 'view1'

    },
    'channel': {
      'wrapped': False,
      'mobile': False
    },
    'urls': {
      'cashier': request.host_url, # assigned by licensee
      'responsibleGaming': 'http://www.RGam.ee', # assigned by licensee
      'lobby': 'http://www.lobb.ee', # assigned by licensee
      'sessionTimeout': 'http://www.sesstm.ee' # assigned by licensee
    },
    'freeGames': False
    }})

    x = requests.post('https://diyft4.uat1.evo-test.com/ua/v1/diyft40000000001/test123', json=UApayload)
    webbrowser.open('https://diyft4.uat1.evo-test.com' + x.json()['entry'])

    print(userdata)
    return render_template('userinfo.html', userdata=userdata)

@app.route('/ft', methods=['GET', 'POST'])
def ft():

    form = FundTransferForm()
    rwa = casinoCmd('RWA')
    userdata['balance'] = rwa[3].text

    if form.validate_on_submit():
        if form.subtract.data:
            flash(form.amount.data + ' funds subtracted', 'warning')
            ft_subtract(form.amount.data)
        elif form.add.data:
            flash(form.amount.data + ' funds added', 'success')
            ft_add(form.amount.data)
        else:
            flash('Error:' + form.amount.errors, 'error')

    return render_template('fundTransfer.html', form=form, userdata=userdata)

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

    return render_template('fundTransfer.html', form=form, userdata=userdata)


def ft_subtract(amount):

    form = FundTransferForm()
    edb = casinoCmd('EDB', amount)

    userdata.update({
        'balance': edb[0].text,
        'etransid': edb[1].text,
        'transid': edb[2].text,
        'datetime': edb[3].text
    })

    return render_template('fundTransfer.html', form=form, userdata=userdata)


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
