from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, FundTransferForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

user = [
    # {
    #     'balance': 'empty',
    #     'etransid': 'empty',
    #     'transid': 'empty',
    #     'datetime': 'empty',
    #     'euid': 'empty',
    #     'uid': 'empty'
    # }
]


@app.route("/")
def start():

    url = 'http://www.waltyao.com'
    myobj = {'somekey': 'somevalue'}

    x = requests.post(url)

    # print the response text (the content of the requested file):

    print(x.text)

    userdata = {
            'balance': x.text,
            'etransid': '2',
            'transid': '3',
            'datetime': 'em4pty',
            'euid': '5',
            'uid': '6'
            }

    return render_template('layout.html', userdata=userdata)


@app.route("/home")
def home():

    userdata = {
            'balance': '1',
            'etransid': '2',
            'transid': '3',
            'datetime': 'em4pty',
            'euid': '5',
            'uid': '6'
            }
    # render_template('layout.html', userdata=userdata)
    return render_template('control.html', posts=posts)


# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('oneWallet.html', title='One Wallet', form=form, userdata=userdata)


@app.route("/ft", methods=['GET', 'POST'])
def ft():

    userdata = {
            'balance': '1',
            'etransid': '2',
            'transid': '3',
            'datetime': 'em4pty',
            'euid': '5',
            'uid': '6'
            }
    form = FundTransferForm()
    # form.amount.data = "x.text"
    # if form.validate_on_submit():
    #     if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('fundTransfer.html', title='Fund Transfer', form=form, userdata=userdata)


if __name__ == '__main__':
    app.run(debug=True)
