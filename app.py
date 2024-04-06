import yaml
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from connect_db import load_config, student_data, course_data, select_table
from account import search_account, login, sign_up
from search import search_courses

app = Flask(__name__)
app.secret_key = load_config().get('app', {}).get('secret_key', 'default_secret_key')

login_flag = False
student_info = None

class LoginForm(FlaskForm):
    SID = StringField('SID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def root():
    return redirect(url_for('login_page'))

@app.route('/index')
def index():
    global student_info
    if login_flag == False:
        return redirect(url_for('login_page'))

    schedule_name = 'schedule_'+student_info.SID
    schedule_data = select_table(schedule_name)

    return render_template('index.html', schedule=schedule_data, student_info=student_info, course_data=course_data)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global login_flag, student_info
    if login_flag:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        SID = form.SID.data
        password = form.password.data

        if search_account(SID) == False:
            flash('此帳號不存在')
            return redirect(url_for('sign_up_page'))
        else:
            login(SID, password)
            login_flag = True
            student_info = student_data(SID)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    form = LoginForm()
    if form.validate_on_submit():
        SID = form.SID.data
        password = form.password.data

        if search_account(SID):
            flash('此帳號已存在')
        else:
            sign_up(SID, password)
            flash('Account created successfully!')
            return redirect(url_for('login_page'))
    return render_template('sign_up.html', form=form)

@app.route('/search', methods=['GET'])
def search():
    search_options = {}
    for key, value in request.args.items():
        if key.endswith('_input'):
            option_name = key.split('_input')[0]
            search_options[option_name] = value

    search_result = search_courses(search_options)

    schedule_name = 'schedule_'+student_info.SID
    schedule_data = select_table(schedule_name)

    return render_template('index.html', search_result=search_result, student_info=student_info, schedule=schedule_data, course_data=course_data)

if __name__ == '__main__':
    app.run(debug=True)