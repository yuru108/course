import mysql.connector

def select_student(table):
    connection = mysql.connector.connect(host='127.0.0.1',
                                        port='3306',
                                        user='root',
                                        password='Yuru_102640',
                                        database='course')

    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM `{table}`;')

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def select_course(table):
    connection = mysql.connector.connect(host='127.0.0.1',
                                        port='3306',
                                        user='root',
                                        password='Yuru_102640',
                                        database='course')

    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM `{table}`;')

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result