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

def search_courses(search_options):
    sql_query = "SELECT * FROM `course` WHERE 1=1"
    
    if 'ID' in search_options:
        sql_query += f" AND ID = {search_options['ID']}"
    if 'cname' in search_options:
        sql_query += f" AND cname = '{search_options['cname']}'"
    if 'professor' in search_options:
        sql_query += f" AND professor = '{search_options['professor']}'"
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

# search_options = {'ID': None, 'cname': '', 'professor': '', 'type': '必修', 'major': '', 'time': None}