from flask import flash
import psycopg2
import user as u
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import logging

def getData(query):
    try:
        connection = psycopg2.connect(host='localhost', user='postgres', password='1606',
                                      dbname='pHouse', port=5432)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as ex:
        logging.error(ex)
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
        logging.error(ex)
        print(ex)
    finally:
        connection.close()
    
    
def getContent():
    try:
        return getData('SELECT i.*, u.firstname, u.lastname FROM information AS i JOIN users AS u ON i.admin_id = u.id')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getNews(id):
    try:
        return getData(f'SELECT i.*, u.firstname, u.lastname FROM information AS i JOIN users AS u ON i.admin_id = u.id WHERE i.id = {id}')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

        
def createUser(login, password, firstname, lastname, role ):
    password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    try:
        setData(f'INSERT INTO users (lastname, firstname, email, password, role) VALUES {lastname, firstname, login, password_hash, role}')
        flash('Пользователь успешно добавлен!')
    except Exception as error:
        logging.error(error)
        flash('Пользователь с таким email существует!')
        print(error)
        
        
def checkUser(password_hash, password):
    try:
        return check_password_hash(password_hash, password)
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getUserById(id):
    try:
        user = getData(f"SELECT u.id, u.lastname, u.firstname, u.email, u.password, r.role from users u join roles r on u.role = r.id and u.id = {id}")[0]
        person = u.User(user[0], user[1], user[2], user[3], user[4], user[5])
        return {'id': person.id, 'lastname': person.lastname, 'firstname': person.firstname, 'email': person.email, 'password': person.password, 'role': person.role}
    except Exception as ex:
        logging.error(ex)
        print(ex)
    
    
def getUserByEmail(email):
    try:
        user = getData(f"SELECT u.id, u.lastname, u.firstname, u.email, u.password, r.role from users u join roles r on u.role = r.id and u.email = '{email}'")[0]
        person = u.User(user[0], user[1], user[2], user[3], user[4], user[5])
        if person != []:
            return {'id': person.id, 'lastname': person.lastname, 'firstname': person.firstname, 'email': person.email, 'password': person.password, 'role': person.role}
        else: 
            return False
    except Exception as ex:
        logging.error(ex)
        print(ex)  
        
        
def getAllOrders():
    try:
        return getData('SELECT o.id, u.lastname, u.firstname, p.name ptype, e.code, a.name author, e.name, e."pageCount", e.count_t, t.name typography,  o.date_in, o.date_out, s.name status, o.price FROM orders o JOIN order_takers ot  ON ot.users_id = o.order_taker_id JOIN users u  ON u.id = ot.users_id JOIN print_types p ON p.id = o.print_type JOIN editions e ON e.id = o.edition_id JOIN authors a ON a.id = e.author_id JOIN typographys t ON t.id = o.typography_id JOIN statuses s ON s.id = o.status_id ')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getMyOrders(user_id):
    try:
        return getData(f'SELECT o.id, u.lastname, u.firstname, p.name ptype, e.code, a.name author, e.name, e."pageCount", e.count_t, t.name typography,  o.date_in, o.date_out, s.name status, o.price FROM orders o JOIN order_takers ot  ON ot.users_id = o.order_taker_id JOIN users u  ON u.id = ot.users_id JOIN print_types p ON p.id = o.print_type JOIN editions e ON e.id = o.edition_id JOIN authors a ON a.id = e.author_id JOIN typographys t ON t.id = o.typography_id JOIN statuses s ON s.id = o.status_id WHERE order_taker_id = {user_id}')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def getAuthors():
    try:
        return getData(f'SELECT * FROM authors')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
def getAuthor(id):
    try:
        return getData(f'SELECT * FROM authors WHERE id = {id}')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getTypo():
    try:
        return getData(f'SELECT * FROM typographys')
    except Exception as ex:
        logging.error(ex)
        print(ex)
    
    
def getPrintTypes():
    try:
        return getData(f'SELECT * FROM print_types')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getUsers():
    try:
        return getData(f'SELECT users.id, lastname, firstname, email, r.role  from users join roles r on r.id = users.role')
    except Exception as ex:
        logging.error(ex)
        print(ex)
   
        
def getRoles():
    try:
        return getData(f'SELECT * FROM roles')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        
        
def getAdminsCount():
    try:
        return getData(f'SELECT count(*) FROM users WHERE role = 2')
    except Exception as ex:
        logging.error(ex)
        print(ex)
        

def createNews(title, post, file, user_id):
    date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    try:
        setData(f"INSERT INTO information (name, text, date, photopath, admin_id) VALUES {title, post, date, file, user_id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)
        
   
def createAuthor(name, info, photo):
    try:
        setData(f"INSERT INTO authors (name, info, photopath) VALUES ({name}, {info}, {photo})")
    except Exception as ex:
        print(ex)
        logging.error(ex)
   
   
   
def createOrder(userId, edName, pageCount, tiraj, typo, print_types, adress):
    date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #date_out = 
    try:
        order_taker = getData(f'SELECT * FROM order_takers WHERE users_id = {userId}')
        if order_taker == []:
            setData(f'INSERT INTO order_takers (users_id, adress) VALUES ({userId}, {adress})')
        
        #setData(f"INSERT INTO orders (order_taker_id, print_types, typography_id, date_in, date_out, status_id, price) VALUES ()")
        #данные добавляются в ордертейкер
        #сделать функцию. добавить в эдишн. вернуть айди в ордер. вернуть айди в эдишн
        #данные добавляются в издание с этим ордером и затем обратно
        
        setData(f"")
    except Exception as ex:
        logging.error(ex)
        print(ex)     
        
        
def changeUserData(lastname, firstname, email, role, id):
    try:
        setData(f"UPDATE users SET lastname = '{lastname}', firstname = '{firstname}', email = '{email}', role = {role} WHERE id = {id}")
    except Exception as ex:
        print(ex)
        logging.error(ex)
   
                
        

# def resetPassword(user_id, password):
#     password_hash = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
#     try:
#         setData(f'UPDATE users SET password = {password_hash} WHERE id = {user_id}')
#         flash('Пароль успешно изменен!')
#     except Exception as error:
#         flash('Что-то пошло не так!')
#         print(error)
    
        
