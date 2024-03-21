# db_connect.py

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="facerecog_attendance_db"
    )

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="",
#         database="dev_monitoring"
#     )

def get_dev_eguro_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="dev_eguro"
    )


def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
