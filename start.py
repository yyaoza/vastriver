from flask import Flask           # import flask
from wtforms import Form, FloatField, validators, SubmitField
app = Flask(__name__)             # create an app instance


class MoneyForm(Form):
    amount = FloatField('Username', [validators.Length(min=4, max=25)])
    amount_minus = SubmitField()
    amount_add = SubmitField()

# @app.route("/<param>")                   # at the end point /
# def lets_go(param):                      # call method hello
#     return "Hello " + param         # which returns "hello world"


@app.route("/")                   # at the end point /
def begin(request):                      # call method hello
    form = MoneyForm(request.POST)
    # if request.method == 'POST' and form.validate():
    #     user = User()
    #     user.username = form.username.data
    #     user.email = form.email.data
    #     user.save()
    #     redirect('register')
    # return render_response('register.html', form=form)


# if __name__ == "__main__":        # on running python app.py
#    app.run(debug=True)                     # run the flask app
