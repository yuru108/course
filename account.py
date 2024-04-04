import bcrypt
import mysql.connector
from connect_db import create_schedule
from flask import flash

connection = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='Yuru_102640',
    database='course'
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