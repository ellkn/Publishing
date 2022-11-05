from flask import Flask, render_template, request, redirect, url_for
import db as db
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'


@app.route('/', methods = ["GET", "POST"])
def index():
    content = db.getData('SELECT i.*, u.firstname, u.lastname FROM information AS i JOIN users AS u ON i.admin_id = u.id')
    print(content)
    return render_template('index.html', content = content, title = "ELL_KN")


@app.route('/error')
def error():
    return render_template('error.html', title = "SORRY, WE HAVE SOME TROUBLES")


@app.route('/login', methods = ['POST', 'GET'])
def logIn():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        return render_template('login.html')
    
    return render_template('login.html', title = "АВТОРИЗАЦИЯ")

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        select = request.form.get('select')
        db.createUser(email, password, name, lastname, select)
         #СДЕЛАТЬ ОБРАБОТКУ ВЫБОРА РОЛИ НА СТРАНИЦЕ
        return redirect('/login')
    return render_template('registration.html', title = "РЕГИСТРАЦИЯ")

@app.route('/changePassword', methods = ['POST', 'GET'])
def changePassword():
    return render_template('changePassword.html', title = "СМЕНИТЬ ПАРОЛЬ")

@app.route('/about')
def about():
    return render_template('about.html', title = "О НАС")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title = "КОНТАКТЫ")

@app.route('/printHouses')
def printHouses():
    return render_template('printHouses.html', title = "ТИПОГРАФИИ")

@app.route('/authors')
def authors():
    authors = db.getData(f'SELECT * FROM authors')
    return render_template('authors.html', authors = authors, title = "АВТОРЫ")

@app.route('/orders')
def orders():
    return render_template('orders.html', title = "ЗАКАЗЫ")

app.run(debug=True)