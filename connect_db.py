import mysql.connector
from init import Student, Time, Course, Professor, Schedule

connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Yuru_102640',
    database='course'
)

def close_connect():
    connection.close()

def student_data(SID):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM `student` WHERE `SID`=%s;', (SID,))
    result = cursor.fetchall()

    student = Student(SID=result[0][0], name=result[0][1], major=result[0][2], total_credit=result[0][3])

    cursor.close()
    return student

def course_data(CID):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `course` WHERE `ID`={CID};')
    result = cursor.fetchall()

    course = Course(ID=result[0][0], course_id=result[0][1], cname=result[0][2], professor=result[0][3], type=result[0][4], major=result[0][5], credit=result[0][6], max_member=result[0][7], current_member=result[0][8], start=result[0][9], end=result[0][10])

    cursor.close()
    return course

def select_table(table):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `{table}`;')
    result = cursor.fetchall()

    cursor.close()
    return result

def init_course(SID):
    cursor = connection.cursor()
    schedule_name = 'schedule_'+SID

    # clear table
    cursor.execute(f'TRUNCATE TABLE {schedule_name}')
    
    for i in range(1, 71):
        cursor.execute(f'INSERT INTO `{schedule_name}` (`time_id`) VALUES (%s)', (i,))

    connection.commit()
    cursor.close()

def add_schedule(SID, CID):
    cursor = connection.cursor()
    schedule_name = 'schedule_'+SID

    cursor.execute(f'SELECT `start`,`end` FROM `course` WHERE `ID`={CID};')
    start, end = (cursor.fetchall())[0]

    cursor.execute(f'UPDATE `{schedule_name}` SET `course_id`={CID} WHERE `time_id` BETWEEN {start} AND {end};')

    connection.commit()
    cursor.close()

def remove_schedule(SID, CID):
    cursor = connection.cursor()
    schedule = 'schedule_'+SID

    cursor.execute(f'UPDATE `{schedule}` SET `course_id`=NULL WHERE `course_id`={CID};')

    connection.commit()
    cursor.close()