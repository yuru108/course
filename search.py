import mysql.connector
from connect_db import load_config, select_table, course_data

config_data = load_config()

connection = mysql.connector.connect(
    host=config_data.get('database', {}).get('host', ''),
    port=config_data.get('database', {}).get('port', ''),
    user=config_data.get('database', {}).get('user', ''),
    password=config_data.get('database', {}).get('password', ''),
    database=config_data.get('database', {}).get('database', '')
)

def search_courses(search_options, student_info):
    sql_query = "SELECT * FROM `course` WHERE 1=1"
    
    if 'ID' in search_options:
        sql_query += f" AND ID = {search_options['ID']}"
    if 'cname' in search_options:
        sql_query += f" AND cname = '{search_options['cname']}'"
    if 'professor' in search_options:
        sql_query += f" AND professor = (SELECT `PID` FROM `professor` WHERE `name`='{search_options['professor']}')"
    if 'type' in search_options:
        sql_query += f" AND type = '{search_options['type']}'"
    if 'major' in search_options:
        sql_query += f" AND major = '{search_options['major']}'"
    if 'day' in search_options and 'period' in search_options:
        time = (int(search_options['day']) - 1) * 14 + int(search_options['period'])
        sql_query += f" AND {time} BETWEEN `start` AND `end`"

    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    condition = []

    if 'selectable' in search_options:
        for i in result:
            if selectable(i[0], student_info):
                condition.append(i)
    else:
        condition = result

    connection.commit()
    cursor.close()
    return condition

def in_schedule(SID, CID):
    cursor = connection.cursor()
    try:
        schedule_name = "schedule_"+SID
        cursor.execute(f"SELECT * FROM `{schedule_name}` WHERE `course_id`={CID};")
        result = cursor.fetchone()
        if result:
            return True
        return False
    finally:
        cursor.fetchall()
        connection.commit()
        cursor.close()

def same_course(SID, course_id):
    cursor = connection.cursor()
    try:
        schedule_name = "schedule_"+SID
        cursor.execute(f"SELECT * FROM {schedule_name} s JOIN `course` c ON(s.course_id = c.ID) WHERE c.course_id = {course_id};")
        result = cursor.fetchone()
        if result:
            return True
        return False
    finally:
        cursor.fetchall()
        connection.commit()
        cursor.close()

# 判斷是否有衝堂
def check_schedule(SID, start, end):
    schedule_name = 'schedule_'+SID
    schedule = select_table(schedule_name)

    for i in range(start-1, end):
        if schedule[i][1] != None:
            return False            # 有衝堂
    return True                     # 無衝堂

def selectable(CID, student):
    c = course_data(CID)

    if check_schedule(student.SID, c.start, c.end) and (student.major == c.major or c.major == '通識學院') and student.total_credit + c.credit <= 30 and same_course(student.SID, c.course_id) == False and in_schedule(student.SID, c.ID) == False:
        return True
    return False

# SID = "D1150459"
# student_info = student_data(SID)
# search_options = {'selectable': 1}

# search_courses(search_options, student_info)