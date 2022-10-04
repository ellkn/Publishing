from flask import Flask, render_template, request, redirect, url_for
import db as db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'


@app.route('/', methods = ["GET", "POST"])
def index():
    content = db.getData('SELECT i.*, u.firstname, u.lastname FROM information AS i JOIN users AS u ON i.admin_id = u.id')
    print(content)
    return render_template('index.html', content = content)


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/login', methods = ['POST', 'GET'])
def logIn():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        
        return render_template('registration.html')
    return render_template('registration.html')

@app.route('/changePassword', methods = ['POST', 'GET'])
def changePassword():
    return render_template('changePassword.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/printHouses')
def printHouses():
    return render_template('printHouses.html')

@app.route('/authors')
def authors():
    authors = db.getData(f'SELECT * FROM authors')
    print(authors)
    return render_template('authors.html', authors = authors)

@app.route('/orders')
def orders():
    return render_template('orders.html')

app.run(debug=True)