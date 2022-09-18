import psycopg2


def getData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606',
                                      dbname='pHouse', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Exception as ex:
        print(ex)


def setData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606',
                                      dbname='pHouse', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
    except Exception as ex:
        print(ex)
