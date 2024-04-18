from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from connect_db import load_config, student_data, course_data, professor_data, select_table
from account import search_account, login, sign_up
from search import search_courses, in_schedule, selectable
from add_course import add_course
from withdraw_course import withdraw_course
from follow import follow_list, is_followed, add_follow, withdraw_follow, draw_queue

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
    if login_flag == False:
        return redirect(url_for('login_page'))

    schedule_name = 'schedule_'+student_info.SID
    schedule_data = select_table(schedule_name)

    follow = follow_list(student_info.SID)

    return render_template('index.html', schedule=schedule_data, student_info=student_info, follow_list=follow, course_data=course_data, professor_data=professor_data, selectable=selectable)

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
            if login(SID, password):
                login_flag = True
                student_info = student_data(SID)
                return redirect(url_for('index'))
            else:
                flash('密碼輸入錯誤')
    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    form = LoginForm()
    if form.validate_on_submit():
        SID = form.SID.data
        password = form.password.data

        if search_account(SID):
            flash('此帳號已存在')
            return redirect(url_for('login_page'))
        else:
            sign_up(SID, password)
            return redirect(url_for('login_page'))
    return render_template('sign_up.html', form=form)

@app.route('/logout')
def logout():
    global login_flag, student_info
    login_flag = False
    student_info = None
    return redirect(url_for('login_page'))

@app.route('/search', methods=['GET'])
def search():
    global student_info
    search_options = {}
    for key, value in request.args.items():
        if key.endswith('_input'):
            option_name = key.split('_input')[0]
            search_options[option_name] = value

    search_result = search_courses(search_options, student_info)

    student_info = student_data(student_info.SID)

    schedule_name = 'schedule_'+student_info.SID
    schedule_data = select_table(schedule_name)

    follow = follow_list(student_info.SID)

    return render_template('index.html', search_result=search_result, student_info=student_info, schedule=schedule_data, follow_list=follow, course_data=course_data, professor_data=professor_data, in_schedule=in_schedule, is_followed=is_followed, selectable=selectable)

@app.route('/add_course', methods=['POST'])
def add_course_route():
    data = request.get_json()
    SID = data.get('SID')
    CID = data.get('CID')
    result, error_message = add_course(SID, CID)
    if result:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error_message})

@app.route('/withdraw_course', methods=['POST'])
def withdraw_course_route():
    data = request.get_json()
    SID = data.get('SID')
    CID = data.get('CID')
    result, error_message = withdraw_course(SID, CID)
    if result:
        draw_queue(CID)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': error_message})
    
@app.route('/follow_course', methods=['POST'])
def follow_course_route():
    data = request.get_json()
    SID = data.get('SID')
    CID = data.get('CID')
    act = data.get('act')

    try:
        if act == 0:
            withdraw_follow(SID, CID)
        elif act == 1:
            add_follow(SID, CID)
    except:
        return jsonify({'success': False, 'error': "Error 請再試一次"})
    else:
        return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)