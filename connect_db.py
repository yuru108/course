import mysql.connector

connection = mysql.connector.connect(host='127.0.0.1',
                                    port='3306',
                                    user='root',
                                    password='Yuru_102640',
                                    database='course')

cursor = connection.cursor()

# cursor.execute('')

# for i in range(1, 71):
#     cursor.execute("INSERT INTO `schedule_D1150459` (`time_id`) VALUES (%s)", (i,))

# connection.commit()

input_SID = 'D1150080'
input_CID = '2'

table = 'course'

cursor.execute(f'SELECT * FROM `{table}` 
               WHERE `ID` = {input_CID};')

records = cursor.fetchall()
for r in records:
    print(r)

cursor.close()
connection.close()