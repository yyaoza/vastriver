from flask import Flask, request, render_template, url_for, flash, redirect
from forms import FundTransferForm, UserAuthenticationForm
import requests, webbrowser, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'

userdata = {
    'emailaddress': 'x',
    'screenname': 'x',
    'countrycode': 'x',
    'name': 'x',
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
    'uuid': 'random', # assigned
    'player': {
        'id': 'yaoza', # assigned by licensee
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
    rwa = casinoCmd('RWA')

    global userdata
    userdata.update({
        'emailaddress': gui[0].text,
        'screenname': gui[3].text,
        'countrycode': gui[4].text,
        'name': gui[1].text + ' ' + gui[2].text,
        'balance': rwa[3].text,
        'euid': gui[6].text,
        'uid':  gui[5].text,
        })

    return render_template('userinfo.html', userdata=userdata)


@app.route('/preLaunch', methods=['GET', 'POST'])
def preLaunch():

    form = UserAuthenticationForm()

    # print(form.language)

    if form.validate_on_submit():
        if form.update.data:
            form.get_country()

    return render_template('userAuthentication.html', title='Fund Transfer', form=form, userdata=userdata)


def ua():

    # form = UserAuthenticationForm()

    # print('$$$' + request.host_url)

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
    if form.validate_on_submit():
        if form.subtract.data:
            flash(form.amount.data + ' funds subtracted', 'warning')
            ft_subtract(form.amount.data)
        elif form.add.data:
            flash(form.amount.data + ' funds added', 'success')
            ft_add(form.amount.data)
        else:
            flash('Error:' + form.amount.errors, 'error')

    return render_template('fundTransfer.html', title='Fund Transfer', form=form, userdata=userdata)

def ft_add(amount):

    ecr = casinoCmd('ECR', amount)

    userdata.update({
        'balance': ecr[0].text,
        'etransid': ecr[1].text,
        'transid': ecr[2].text,
        'datetime': ecr[3].text
    })
    print(userdata)

    return render_template('userinfo.html', userdata=userdata)


def ft_subtract(amount):

    edb = casinoCmd('EDB', amount)

    userdata.update({
        'balance': edb[0].text,
        'etransid': edb[1].text,
        'transid': edb[2].text,
        'datetime': edb[3].text
    })

    return render_template('userinfo.html', userdata=userdata)


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
    return render_template('oneWallet.html', title='One Wallet', form=form, userdata=userdata)


if __name__ == '__main__':
    app.run(debug=True)
