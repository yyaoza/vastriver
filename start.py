from flask import Flask, render_template       # import flask
import ftForm
app = Flask(__name__)             # create an app instance


# @app.route("/<param>")                   # at the end point /
# def lets_go(param):                      # call method hello
#     return "Hello " + param         # which returns "hello world"


@app.route("/")                   # at the end point /
def begin():                      # call method hello
    form = ftForm.MoneyForm()
    return render_template('home.html')


@app.route("/fundtransfer")  # at the end point /
def fundtransfer():  # call method hello
    form = ftForm.MoneyForm()
    return "<h1>Fund Transfer</h1>"


@app.route("/onewallet")  # at the end point /
def onewallet():  # call method hello
    form = ftForm.MoneyForm()
    return "<h1>Fund Transfer</h1>"
    # if request.method == 'POST' and form.validate():
    #     user = User()
    #     user.username = form.username.data
    #     user.email = form.email.data
    #     user.save()
    #     redirect('register')
    # return render_response('result.html', title='the numbers', form=form)


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the flask app
