from flask import flash
import psycopg2
import user as u
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
        
        
def createUser(login, password, firstname, lastname, role ):
    password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    try:
        setData(f'INSERT INTO users (lastname, firstname, email, password, role) VALUES {lastname, firstname, login, password_hash, role}')
        flash('Пользователь успешно добавлен!')
    except Exception as error:
        flash('Пользователь с таким email существует!')
        print(error)
        
        
def checkUser(password_hash, password):
    return check_password_hash(password_hash, password)


def getUserById(id):
    user = getData(f"SELECT u.id, u.lastname, u.firstname, u.email, u.password, r.role from users u join roles r on u.role = r.id and u.id = {id}")[0]
    person = u.User(user[0], user[1], user[2], user[3], user[4], user[5])
    return {'id': person.id, 'lastname': person.lastname, 'firstname': person.firstname, 'email': person.email, 'password': person.password, 'role': person.role}
    
    
def getUserByEmail(email):
    user = getData(f"SELECT u.id, u.lastname, u.firstname, u.email, u.password, r.role from users u join roles r on u.role = r.id and u.email = '{email}'")[0]
    person = u.User(user[0], user[1], user[2], user[3], user[4], user[5])
    if person != []:
        return {'id': person.id, 'lastname': person.lastname, 'firstname': person.firstname, 'email': person.email, 'password': person.password, 'role': person.role}
    else: 
        return False
      
        
def getRoleUser(user_id):
    role = getData(f"SELECT r.role FROM role r join users u on u.id = {id} and r.id = u.role")[0]
    if role != []:
        return role
    else: 
        return False
        
