import bcrypt
import mysql.connector

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
    if search_account(SID):
        print('此帳號已存在')
        return False
    else:
        cursor = connection.cursor()

        hashed_password, salt = hash_password(password)

        cursor.execute('INSERT INTO `account` (`SID`, `password`, `salt`) VALUES (%s, %s, %s);', (SID, hashed_password, salt))
        connection.commit()

        print('帳號建立成功')

        cursor.close()

        return True
    
def login(SID, password):
    if search_account(SID) == False:
        print('此帳號不存在')
        return False
    else:
        cursor = connection.cursor()
        cursor.execute('SELECT `password` FROM `account` WHERE `SID`=%s;', (SID, ))
        stored_password = (cursor.fetchone())[0]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            print('登入成功')
            return True
        else:
            print('密碼輸入錯誤')
            return False


SID = 'D1150459'
password = 'mypassword'

sign_up(SID, password)
login(SID, password)