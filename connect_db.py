import mysql.connector
from init import Student, Time, Course, Professor, Schedule

connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Yuru_102640',
    database='course'
)

def student_data(SID):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM `student` WHERE `SID`=%s;', (SID,))
    result = cursor.fetchone()

    student = Student(SID=result[0], name=result[1], major=result[2], total_credit=result[3])

    cursor.close()
    return student

def course_data(CID):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `course` WHERE `ID`={CID};')
    result = cursor.fetchone()

    course = Course(ID=result[0], course_id=result[1], cname=result[2], professor=result[3], type=result[4], major=result[5], credit=result[6], max_member=result[7], current_member=result[8], start=result[9], end=result[10])

    cursor.close()
    return course

def select_table(table):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `{table}`;')
    result = cursor.fetchall()
    
    cursor.close()
    return result

def update_credit(SID, CID):
    cursor = connection.cursor()
    cursor.execute('SELECT `total_credit` FROM `student` WHERE `SID`=%s;', (SID, ))
    current_credit = cursor.fetchone()[0]

    cursor.execute(f'SELECT `credit` FROM `course` WHERE `ID`={CID};')
    course_credit = cursor.fetchone()[0]

    cursor.execute(f'UPDATE `student` SET `total_credit`={current_credit+course_credit} where `SID`=%s;', (SID, ))

    connection.commit()
    cursor.close()

def create_schedule(SID):
    cursor = connection.cursor()
    schedule_name = 'schedule_'+SID

    cursor.execute(f'CREATE TABLE `{schedule_name}`(`time_id` int, `course_id` int, foreign key (`time_id`) references `time`(ID) on delete set null, foreign key (`course_id`) references course(ID) on delete set null);')
    
    connection.commit()
    cursor.close()

    init_schedule(SID)

def init_schedule(SID):
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

    cursor.execute(f'SELECT `current_member` FROM `course` WHERE `ID`={CID};')
    current_member = (cursor.fetchall())[0][0]
    cursor.execute(f'UPDATE `course` SET `current_member`={current_member+1} WHERE `ID`={CID};')
    connection.commit()

    cursor.close()

def remove_schedule(SID, CID):
    cursor = connection.cursor()
    schedule = 'schedule_'+SID

    cursor.execute(f'UPDATE `{schedule}` SET `course_id`=NULL WHERE `course_id`={CID};')

    connection.commit()
    cursor.close()