import yaml
import bcrypt
import mysql.connector
from connect_db import create_schedule
from flask import flash


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

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode(), salt.decode()

def search_account(SID):
    cursor = connection.cursor()
    cursor.execute('SELECT `password`, `salt` FROM `account` WHERE `SID` = %s;', (SID,))

    if cursor.fetchone():
        return True
    return False

def sign_up(SID, password):
    cursor = connection.cursor()

    hashed_password, salt = hash_password(password)

    cursor.execute('INSERT INTO `account` (`SID`, `password`, `salt`) VALUES (%s, %s, %s);', (SID, hashed_password, salt))
    connection.commit()
    cursor.close()

    create_schedule(SID)

    flash('帳號建立成功')
    return True
    
def login(SID, password):
    cursor = connection.cursor()
    cursor.execute('SELECT `password` FROM `account` WHERE `SID`=%s;', (SID, ))
    stored_password = (cursor.fetchone())[0]

    if bcrypt.checkpw(password.encode(), stored_password.encode()):
        return True
    else:
        flash('密碼輸入錯誤')
        return False