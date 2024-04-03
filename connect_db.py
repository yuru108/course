import mysql.connector

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

    cursor.close()
    return result

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
