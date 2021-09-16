from app import app
from flask import render_template
from app.forms import LoginForm
from app import con


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if con.find_user(form.username.data, form.password.data):
            pass  # TODO action after login
    return render_template("login.html", form=form)
