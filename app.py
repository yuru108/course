from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import bcrypt
from connect_db import select_table
from account import login

app = Flask(__name__)
app.secret_key = 'Yuru102640'

class LoginForm(FlaskForm):
    SID = StringField('SID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        SID = form.SID.data
        password = form.password.data
        if login(SID, password):
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your SID and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/')
def root():
    return redirect(url_for('login_page'))

@app.route('/index')
def index():
    schedule_data = select_table('schedule_D1150459')
    return render_template('index.html', schedule=schedule_data)

if __name__ == '__main__':
    app.run(debug=True)
