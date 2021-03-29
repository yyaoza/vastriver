from flask import Flask, render_template, url_for, flash, redirect

from forms import FundTransferForm
import requests, xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhh its a secret'
# '5791628bb0b13ce0c676dfde280ba245'

userdata = {
    'emailaddress': '',
    'screenname': '',
    'countrycode': '',
    'name': '',
    'balance': 'xxx',
    'etransid': 'xxx',
    'transid': 'xxx',
    'datetime': 'empty',
    'euid': '',
    'uid': '',
}


@app.route("/")
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

    global userdata
    userdata = {
        'emailaddress': gui[0].text,
        'screenname': gui[3].text,
        'countrycode': gui[4].text,
        'name': gui[1].text + ' ' + gui[2].text,
        'balance': rwa[3].text,
        'etransid': 'xxx',
        'transid': 'xxx',
        'datetime': 'empty',
        'euid': gui[6].text,
        'uid':  gui[5].text,
        }

    return render_template('layout.html', userdata=userdata)


@app.route("/ft", methods=['GET', 'POST'])
def ft():

    form = FundTransferForm()
    # if form.add.validate:
    #     flash('Account created for !', 'success')
        # return redirect(url_for('home'))
    return render_template('fundTransfer.html', title='Fund Transfer', form=form, userdata=userdata)

@app.route("/ft-add", methods=['GET', 'POST'])
def ft_add():
    flash('Account created for !', 'success')
    return render_template('fundTransfer.html', title='Fund Transfer', form=form, userdata=userdata)


@app.route("/ow", methods=['GET', 'POST'])
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
