from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import db as db
import user as u
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_mail import Mail
import datetime
import logging
#import emailtest as email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'
# app.config['ADMINS'] = ['rgrphotogallery@gmail.com']
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(filename="logs/info.log", filemode='a', level=logging.INFO, format='%(asctime)s | %(message)s')
logging.basicConfig(filename="logs/error.log", filemode='a', level=logging.ERROR)
# mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return u.UserLogin().dbi(user_id)


@app.route('/', methods = ["GET", "POST"])
def index():
    try:
        content = db.getContent()
        if current_user.get_id():
            role = current_user.get_role()
            return response(render_template('index.html', con = content, title = "ИЗДАТЕЛЬСТВО - ELL_KN", role=role))
        return response(render_template('index.html', con = content, title = "ИЗДАТЕЛЬСТВО - ELL_KN", role='USER'))
    except:
        return response(render_template('error.html'))

@app.route('/news/<id>')
def news(id):
    try:
        news = db.getNews(id)
        return response(render_template('news.html', title = news[0][1], news = news[0]))
    except:
            return response(render_template('error.html'))


@app.route('/error')
def error():
    return response(render_template('error.html', title = "SORRY, WE HAVE SOME TROUBLES"))


@app.route('/login', methods = ['POST', 'GET'])
def logIn():
    try:
        if not current_user.get_id():
            if request.method == 'POST':
                user = db.getUserByEmail(request.form.get("email"))
                if user:
                    if db.checkUser(user['password'], request.form.get("password")):
                        login_user(u.UserLogin().create(user))
                        flash("Успешный вход")
                        return redirect("/")
                    else:
                        flash("Неверный логин или пароль")
                        return response(render_template('login.html', title = "АВТОРИЗАЦИЯ"))
                return response(render_template('login.html', title = "АВТОРИЗАЦИЯ"))
            
            return response(render_template('login.html', title = "АВТОРИЗАЦИЯ"))
        else:
            return redirect("/")
    except:
        return response(render_template('error.html'))
        

@app.route('/logout')
@login_required
def logout():
    if current_user.get_id():
        logout_user()
        return redirect("/login")
    else:
        return redirect("/")        


@app.route('/registration', methods = ['POST', 'GET'])
def registration():
    try:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            if request.method == 'POST':
                if request.form.get("select") == "-1":
                    flash("Вы ввели некорректные данные, повторите попытку")
                    return response(render_template('registration.html', title = "РЕГИСТРАЦИЯ"))
                else:
                    email = request.form.get('email')
                    password = request.form.get('password')
                    name = request.form.get('name')
                    lastname = request.form.get('lastname')
                    select = request.form.get('select')
                    phone = request.form.get('phone')
                    db.createUser(email, password, name, lastname, select, phone)
                    return redirect('/login')
            return response(render_template('registration.html', title = "РЕГИСТРАЦИЯ"))
    except:
        return response(render_template('error.html'))

@app.route('/changePassword', methods = ['POST', 'GET'])
def changePassword():
    try:
        if current_user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            user = db.getUserByEmail(request.form.get("email"))
            if user:
                #email.send_password_reset_email(user)
                flash('Check your email for the instructions to reset your password')
            return redirect('/login')
        return response(render_template('changePassword.html', title = "СМЕНИТЬ ПАРОЛЬ"))
    except:
        return response(render_template('error.html'))

# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect('/')
#     user = u.UserLogin.verify_reset_password_token(token)
#     print(user)
#     if not user:
#         return redirect('/')
#     if request.method == 'POST':
#         db.resetPassword(user, request.form.get("password"))
#         return redirect('/login')
#     return render_template('reset_password.html')


@app.route('/contacts')
def contacts():
    try:
        typo = db.getTypo()
        return response(render_template('contacts.html', title = "КОНТАКТЫ", typo = typo))
    except:
        return response(render_template('error.html'))


@app.route('/authors')
def authors():
    try:
        authors = db.getAuthors()
        return response(render_template('authors.html', authors = authors, title = "АВТОРЫ"))
    except:
        return response(render_template('error.html'))


@app.route('/author/<id>')
def author(id):
    try:
        author = db.getAuthor(id)
        return response(render_template('author.html', title = author[0][1], author = author[0]))
    except:
            return response(render_template('error.html'))


@app.route('/createAuthor', methods = ["GET", "POST"])
def createAuthor():
    try:
        if request.method == "POST":
            db.createAuthor(request.form.get("name"), request.form.get("info"), request.form.get("photo"))
            return redirect('/author')
        return response(render_template('createAuthor.html', title = "ДОБАВИТЬ АВТОРА"))
    except:
            return response(render_template('error.html'))


@app.route('/orders')
def orders():
    try:
        allOrders = db.getAllOrders()
        myOrders = db.getMyOrders(current_user.get_id())
        return response(render_template('orders.html', title = "ЗАКАЗЫ", allOrders=allOrders, myOrders=myOrders ))
    except:
        return response(render_template('error.html'))

@app.route('/createNews',  methods = ["GET", "POST"])
def createNews():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            if request.method == 'POST':
                db.createNews(request.form.get("title"),request.form.get("post"),request.form.get("file"),current_user.get_id())
                flash('Новость создана')
                return redirect('/')
            #доделать обработку фотографии и вывод нормальный на экран (стили)
            return response(render_template('createNews.html', title = "СОЗДАТЬ НОВОСТЬ"))
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')
    except:
        return response(render_template('error.html'))
    
    
@app.route('/createOrder',  methods = ["GET", "POST"])
def createOrder():
    try:
        if current_user.is_authenticated and (current_user.get_role() == 'ORGANIZATION' or current_user.get_role() == 'PRIVATE'):
            typo = db.getTypo() 
            print_types = db.getPrintTypes()
            if request.method == 'POST':
                if request.form.get("typo") == "-1" or request.form.get("print_types") == "-1":
                    flash("Введите корректные данные")
                else:
                    db.createOrder(current_user.get_id(), request.form.get("edName"), request.form.get("pageCount"),  request.form.get("tiraj"), request.form.get("typo"), request.form.get("print_types"))
                    flash('Заказ создан')
                    return redirect('/orders')
            return response(render_template('createOrder.html', title = "СОЗДАТЬ ЗАКАЗ", typo = typo, print_types = print_types))
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return response(render_template('error.html'))  
    
    
@app.route('/users')
def users():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            users = db.getUsers()
            return response(render_template('users.html', title = "ПОЛЬЗОВАТЕЛИ", users = users))    
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')
    except:
        return response(render_template('error.html'))
    
    
@app.route('/edit/<id>', methods = ["POST", "GET"])
def edit(id):
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            user = db.getUserById(id)
            role = db.getRoles()
            if request.method == "POST":
                if request.form.get("role") == "-1":
                    flash("Введите корректные данные")
                else:
                    if db.getAdminsCount()[0][0] == 1 and current_user.get_role() == 'ADMIN' and request.form.get("role") != 2:
                        flash("Вы не можете изменить роль у единственного пользователя с ролью ADMIN")
                    else:
                        db.changeUserData(request.form.get("lastname"), request.form.get("firstname"), request.form.get("email"), request.form.get("role"), id)
                    return response(render_template('edit.html', title = "РЕДАКТИРОВАТЬ", user = user, role = role))    
                
            return response(render_template('edit.html', title = "РЕДАКТИРОВАТЬ", user = user, role = role))    
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return response(render_template('error.html') ) 
        
    
@app.route('/addTypo',  methods = ["GET", "POST"])
def addTypo():
    try:
        if current_user.is_authenticated and current_user.get_role() == 'ADMIN':
            if request.method == 'POST':
                db.addTypo(request.form.get('name'), request.form.get('address'), request.form.get('phone'))
                flash('Типография добавлена!')
                return redirect('/contacts')
            return response(render_template('addTypo.html', title = "ДОБАВИТЬ ТИПОГРАФИЮ"))
        else:
            flash('Вы не имеете достаточных прав для перехода на данную страницу')
            return redirect('/')  
    except:
        return response(render_template('error.html'))  
        

def response(site):
    response = make_response(site)
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
    
    
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('error.html', title="Страница не найдена")
    
    
app.run(debug=True)
