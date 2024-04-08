import yaml
import mysql.connector
from init import Student, Course

def load_config(filename="config.yml"):
    with open(filename, "r", encoding="utf-8") as config_file:
        return yaml.load(config_file, Loader=yaml.Loader)

config_data = load_config()

connection = mysql.connector.connect(
    host=config_data.get('database', {}).get('host', ''),
    port=config_data.get('database', {}).get('port', ''),
    user=config_data.get('database', {}).get('user', ''),
    password=config_data.get('database', {}).get('password', ''),
    database=config_data.get('database', {}).get('database', '')
)

def student_data(SID):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM `student` WHERE `SID`=%s;', (SID,))
    result = cursor.fetchone()

    student = Student(SID=result[0], name=result[1], major=result[2], grade=result[3], total_credit=result[4])

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
    init_required_course(SID)

def init_schedule(SID):
    cursor = connection.cursor()
    schedule_name = 'schedule_'+SID

    # clear credit
    cursor.execute('UPDATE `student` SET `total_credit`=0 WHERE `SID`=%s;', (SID, ))

    # clear table
    cursor.execute(f'TRUNCATE TABLE {schedule_name};')
    
    for i in range(1, 71):
        cursor.execute(f'INSERT INTO `{schedule_name}` (`time_id`) VALUES (%s);', (i,))

    connection.commit()
    cursor.close()

def add_schedule(SID, CID):
    cursor = connection.cursor()
    schedule_name = 'schedule_'+SID

    # get course's time
    cursor.execute(f'SELECT `start`,`end` FROM `course` WHERE `ID`={CID};')
    start, end = (cursor.fetchall())[0]

    cursor.execute(f'UPDATE `{schedule_name}` SET `course_id`={CID} WHERE `time_id` BETWEEN {start} AND {end};')
    connection.commit()

    # update member
    cursor.execute(f'SELECT `current_member` FROM `course` WHERE `ID`={CID};')
    new_member = int(cursor.fetchone()[0]) + 1
    cursor.execute(f'UPDATE `course` SET `current_member`={new_member} WHERE `ID`={CID};')
    connection.commit()

    update_credit(SID, CID)

    cursor.close()

def remove_schedule(SID, CID):
    cursor = connection.cursor()
    schedule = 'schedule_'+SID

    cursor.execute(f'UPDATE `{schedule}` SET `course_id`=NULL WHERE `course_id`={CID};')

    connection.commit()
    cursor.close()

def init_required_course(SID):
    cursor = connection.cursor()
    student = student_data(SID)

    cursor.execute(f'SELECT `CID` FROM `required_course` WHERE `major`=%s AND `grade`=%s;', (student.major, student.grade))
    required_course = cursor.fetchall()

    for i in required_course:
        add_schedule(SID, i[0])

# ========= test ===========

# SID = 'D1150459'
# init_schedule(SID)
# init_required_course(SID)

# ==========================