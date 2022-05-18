from mysql.connector import connect, Error
from getpass import getpass

import sys

connection = None
cursor = None

table_name = "web_server.web_server"

def initialize ():
    print ("initializing database")
    try:
        connection = connect (
                host = "localhost",
                user = "web_server",
                password = "qwerty123")

        cursor = connection.cursor();

    except Error as e:
        print ("Initialization failed. Error:", e)
        sys.exit(0)

def add_user (username, password_hash):
    add_user_query = "INSERT INTO " + table_name + \
                     " (username, password_hash) " + \
                     username + ", " + password_hash + ";"

    try:
        cursor.execute(add_user_quiery)
        connection.commit()
    except Error as e:
        print ("Error!")
        sys.exit(0)
