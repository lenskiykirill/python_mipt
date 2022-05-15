import getpass
from mysql.connector import connect, Error

import sys, random

connection = None
table = None

def init (host = "localhost", user = "web_server",
          password = "qwerty123", database = "web_server"):
    
    global connection
    try:
        connection = connect (host=host, user=user, password=password, database=database)
    except:
        print("Connection to database \"%s\" failed. user: \"%s@%s\"" % (database, user, host),
              file = sys.stderr)
        quit ()

def check_user (username):
    global connection

    check_query = """
    SELECT COUNT(0) FROM users WHERE username=\"%s\";
    """ % (username,)

    try:
        with connection.cursor() as cursor:
            cursor.execute(check_query)
            res = cursor.fetchall()

            connection.commit()

            if res[0] != (0,):
                return True
            return False
    except Error as e:
        print ("Check query failed!\n%s" % (check_query,))
        print (e)
        raise

def get_id (username):
    global connection

    get_query = """
    SELECT id FROM users WHERE username=\"%s\";
    """

    get_query = get_query % (username,)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(get_query)
            res = cursor.fetchall()

            connection.commit()
            
            if res == []:
                return None
            return res[0][0]
    except:
        print ("query failed\n%s" % (get_query,), file = sys.stderr)
        return False


def create_user (username, passhash):
    global connection

    insert_query = """
    INSERT INTO users (username, pass_hash)
    VALUES (\"%s\", \"%s\");
    """

    try:
        used = check_user (username)
        if (used):
            return ("fail",)
    except:
        return False

    insert_query = insert_query % (username, passhash)

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            cursor.fetchall()

            connection.commit()
    except:
        print ("query failed\n%s" % (insert_query,), file = sys.stderr)
        return False

    return ("ok",)

def delete_user (username):
    global connection

    if not check_user (username):
        return "fail"

    delete_query = """
    DELETE FROM users WHERE username = \"%s\"
    """ % (username,)

    try:
        with connection.cursor() as cursor:
            cursor.execute(delete_query)
            cursor.fetchall()

            connection.commit()
    except:
        print ("Delete query failed\n%s" % (delete_query,), file = sys.stderr)
        return False

    return "ok"

def create_article (author_id, text):
    global connection

    insert_query = """
    INSERT INTO articles (author_id, text) VALUES (%d, \"%s\");
    """

    insert_query = insert_query % (author_id, text)

    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            cursor.fetchall()

            cursor.execute ("SELECT LAST_INSERT_ID()")
            res = cursor.fetchall()

            connection.commit()

            return ("ok", res[0][0])
    except:
        print ("Article creation failed\n%s" % (insert_query,), file = sys.stderr)
        return False

def autorize (username, pass_hash):
    global connection
    
    search_query = """
    SELECT id from users WHERE username=\"%s\" AND pass_hash=\"%s\";
    """

    update_query = """
    UPDATE users SET token = \"%s\" WHERE id = %d;
    """

    search_query = search_query % (username, pass_hash)

    res = None

    try:
        with connection.cursor() as cursor:

            cursor.execute(insert_query)
            res = cursor.fetchall()

            connection.commit()
    except:
        print ("Request failed\n%s" % (search_query,), file = sys.stderr)
        return False

    user_id = None

    if (res[0] == "ok"):
        user_id = res[1]
    else:
        return ("fail",)

    token = random.randint(1, 2**62)
    update_query = update_query % (token, user_id)

    try:
        with connection.cursor() as cursor:
            cursor.execute (update_query)
            cursor.fetchall()

            connection.commit()

            return ("ok", token)
    except:
        print ("Request failed\n%s" % (update_query,), file = sys.stderr)
        return False

def get_articles (number=100):
    global connection

    get_query = """
    SELECT author_id, date, text FROM articles ORDER BY date ASC LIMIT %d;
    """

    get_query = get_query % (number,)

    try:
        with connection.cursor() as cursor:
            cursor.execute (get_query)
            articles = cursor.fetchall()

            connection.commit()

            return ("ok", articles)
    except:
        print ("Request failed\n%s" % (get_query,), file=sys.stderr)

        return False

def get_username (user_id):
    global connection

    if user_id == 0:
        return ("ok", "anonimous")

    get_query = """
    SELECT username FROM users WHERE id=%d;
    """

    get_query = get_query % user_id

    try:
        with connection.cursor() as cursor:
            cursor.execute (get_query)
            username = cursor.fetchall()
            username = username[0][0]

            connection.commit()

            return ("ok", username)
    except:
        return False

if __name__ == "__main__":
    init();
    username, password = input().split()
    print (get_id (username))

    text = input()
    print(create_article (get_id (username), text)[1])
