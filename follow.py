import yaml
import mysql.connector
import random
from add_course import add_course

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

def follow_list(SID):
    cursor = connection.cursor()

    cursor.execute(f'SELECT `CID` FROM `follow` WHERE `SID`="{SID}";')
    follow_list = cursor.fetchall()
    connection.commit()
    cursor.close()

    return follow_list

def is_followed(SID, CID):
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT * FROM `follow` WHERE `SID`="{SID}" AND `CID`={CID};')
        result = cursor.fetchone()
        if result:
            return True
        return False
    finally:
        cursor.fetchall()
        connection.commit()
        cursor.close()

def add_follow(SID, CID):
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO `follow`(`CID`,`SID`) VALUES({CID},"{SID}");')
    connection.commit()
    cursor.close()

def withdraw_follow(SID, CID):
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM `follow` WHERE `SID`="{SID}" AND `CID`={CID};')
    connection.commit()
    cursor.close()

def draw_queue(CID):
    cursor = connection.cursor()
    cursor.execute(f'SELECT `SID` FROM `follow` WHERE `CID`={CID};')
    queue = cursor.fetchall()

    print(queue)

    while queue:
        selected_SID = random.choice(queue)[0]
        result, error = add_course(selected_SID, CID)

        if result:
            cursor.execute(f'DELETE FROM `follow` WHERE `SID`="{selected_SID}" AND `CID`={CID};')
            connection.commit()
            cursor.close()
            withdraw_follow(selected_SID, CID)
            return True
        else:
            queue.remove((selected_SID,))
            cursor.execute(f'DELETE FROM `follow` WHERE `SID`="{selected_SID}" AND `CID`={CID};')
            connection.commit()
        
    cursor.close()
    return False


# SID = "D1150459"
# print(follow_list(SID))
# print(is_followed(SID, 1))
# add_follow(SID, 4)
# print(follow_list(SID))
# withdraw_follow(SID, 4)
# print(follow_list(SID))

# print(draw_queue(1012))