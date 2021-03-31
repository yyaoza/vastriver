from flask import Flask, render_template, url_for, flash, redirect
from forms import FundTransferForm
import requests, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'
# '5791628bb0b13ce0c676dfde280ba245'


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


@app.route('/')
def start():

    url = 'https://diyft.uat1.evo-test.com/api/ecashier'
    payload = {'cCode': 'GUI',
             'euID': 'c1c2c3c4',
             'ecID': 'diyft00000000001lwwnvexgmzfaaaac',
             'output': '1'
             }
    x = requests.get(url, params=payload)
    gui = ET.fromstring(x.text)

    url = 'https://diyft.uat1.evo-test.com/api/ecashier'
    payload = {'cCode': 'RWA',
             'euID': 'c1c2c3c4',
             'ecID': 'diyft00000000001lwwnvexgmzfaaaac',
             'output': '1'
             }
    x = requests.get(url, params=payload)
    rwa = ET.fromstring(x.text)


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
    url = 'https://diyft.uat1.evo-test.com/api/ecashier'
    payload = {'cCode': 'ECR',
               'euID': 'c1c2c3c4',
               'amount': amount,
               'ecID': 'diyft00000000001lwwnvexgmzfaaaac',
               'eTransID': 'fake_eTransID',
               'output': '1'
               }
    x = requests.get(url, params=payload)
    ecr = ET.fromstring(x.text)

    userdata.update({
        'balance': ecr[0].text,
        'etransid': ecr[1].text,
        'transid': ecr[2].text,
        'datetime': ecr[3].text
    })
    print(userdata)

    return render_template('userinfo.html', userdata=userdata)


def ft_subtract(amount):
    url = 'https://diyft.uat1.evo-test.com/api/ecashier'
    payload = {'cCode': 'EDB',
               'euID': 'c1c2c3c4',
               'amount': amount,
               'ecID': 'diyft00000000001lwwnvexgmzfaaaac',
               'eTransID': 'fake_eTransID',
               'output': '1'
               }
    x = requests.get(url, params=payload)
    edb = ET.fromstring(x.text)

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
