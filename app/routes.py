from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/error.html')
def error():
    return render_template('error.html')


@app.route('/login.html')
def logIn():
    return render_template('login.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contacts.html')
def contacts():
    return render_template('contacts.html')

@app.route('/printHouses.html')
def printHouses():
    return render_template('printHouses.html')

app.run(debug=True)