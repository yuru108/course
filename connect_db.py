import mysql.connector
from init import Student

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

    student = Student(SID=result[0][0], name=result[0][1], major=result[0][2])

    cursor.close()
    return student

def course_data(CID):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM `course` WHERE `SID`=%s;', (CID,))
    result = cursor.fetchall()

    cursor.close()
    return result

def select_table(table):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `{table}`;')
    result = cursor.fetchall()

    cursor.close()
    return result

def init_course(SID):
    cursor = connection.cursor()
    schedule = 'schedule_'+SID

    # clear table
    cursor.execute(f"TRUNCATE TABLE {schedule}")
    
    for i in range(1, 71):
        cursor.execute(f"INSERT INTO `{schedule}` (`time_id`) VALUES (%s)", (i,))

    connection.commit()
    cursor.close()