import mysql.connector

connection = mysql.connector.connect(host='127.0.0.1',
                                    port='3306',
                                    user='root',
                                    password='Yuru_102640',
                                    database='course')

cursor = connection.cursor()

cursor.execute('SELECT * FROM `course`;')

records = cursor.fetchall()
for r in records:
    print(r)

cursor.close()
connection.close()