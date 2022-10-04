import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


def getData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606',
                                      dbname='pHouse', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)
    finally:
        connection.close()


def setData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606',
                                      dbname='pHouse', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        
def checkUser(login, password):
    pass

def createUser(login, password):
    generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    pass

