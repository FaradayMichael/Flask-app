from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm
import psycopg2
from sqlalchemy import create_engine

database = "FlaskApp"
user = "postgres"
password = "root"
host = "127.0.0.1"
port = "5432"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        connection = psycopg2.connect(user="postgres",
                                      password="root",
                                      host="localhost",
                                      port="5432",
                                      database="FlaskApp")
        cur = connection.cursor()
        cur.execute("select * from public.\"USERS\"")
        print(cur.fetchone())
    return render_template("login.html", form=form)
