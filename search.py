import mysql.connector
from connect_db import load_config

config_data = load_config()

connection = mysql.connector.connect(
    host=config_data.get('database', {}).get('host', ''),
    port=config_data.get('database', {}).get('port', ''),
    user=config_data.get('database', {}).get('user', ''),
    password=config_data.get('database', {}).get('password', ''),
    database=config_data.get('database', {}).get('database', '')
)

def search_courses(search_options):
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
        
    cursor.close()
    return result

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
        cursor.close()
        
# search_options = {'ID': None, 'cname': '', 'professor': '', 'type': '必修', 'major': '', 'time': None}