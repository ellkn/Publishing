from flask import Flask, render_template, request, redirect, url_for, flash
import db as db
import user as u
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_mail import Mail
import datetime
#import emailtest as email


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOPSECRETKEY'
app.config['ADMINS'] = ['rgrphotogallery@gmail.com']
login_manager = LoginManager()
login_manager.init_app(app)
# mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return u.UserLogin().dbi(user_id)


@app.route('/', methods = ["GET", "POST"])
def index():
    content = db.getContent()
    print(content)
    if current_user.get_id():
        role = db.getRoleUser(current_user.get_id())
        return render_template('index.html', con = content, title = "ELL_KN", role=role[0])
    return render_template('index.html', con = content, title = "ELL_KN", role='USER')


@app.route('/error')
def error():
    return render_template('error.html', title = "SORRY, WE HAVE SOME TROUBLES")


@app.route('/login', methods = ['POST', 'GET'])
def logIn():
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
                    return render_template('login.html', title = "АВТОРИЗАЦИЯ")
            return render_template('login.html', title = "АВТОРИЗАЦИЯ")
        
        return render_template('login.html', title = "АВТОРИЗАЦИЯ")
    else:
        return redirect("/")
        

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
    if current_user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            lastname = request.form.get('lastname')
            select = request.form.get('select')
            db.createUser(email, password, name, lastname, select)
            return redirect('/login')
        return render_template('registration.html', title = "РЕГИСТРАЦИЯ")

@app.route('/changePassword', methods = ['POST', 'GET'])
def changePassword():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user = db.getUserByEmail(request.form.get("email"))
        if user:
            #email.send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        return redirect('/login')
    return render_template('changePassword.html', title = "СМЕНИТЬ ПАРОЛЬ")

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


@app.route('/about')
def about():
    return render_template('about.html', title = "О НАС")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title = "КОНТАКТЫ")

@app.route('/printHouses')
def printHouses():
    typo = db.getTypo()
    return render_template('printHouses.html', title = "ТИПОГРАФИИ", typo = typo)

@app.route('/authors')
def authors():
    authors = db.getAuthors()
    return render_template('authors.html', authors = authors, title = "АВТОРЫ")

@app.route('/orders')
def orders():
    allOrders = db.getAllOrders()
    myOrders = db.getMyOrders(current_user.get_id())
    return render_template('orders.html', title = "ЗАКАЗЫ", allOrders=allOrders, myOrders=myOrders )

@app.route('/createNews',  methods = ["GET", "POST"])
def createNews():
    if current_user.is_authenticated and db.getRoleUser(current_user.get_id())[0] == 'ADMIN':
        if request.method == 'POST':
            db.createNews(request.form.get("title"),request.form.get("post"),request.form.get("file"),current_user.get_id())
            flash('Новость создана')
            return redirect('/')
        #доделать обработку фотографии и вывод нормальный на экран (стили)
        return render_template('createNews.html', title = "СОЗДАТЬ НОВОСТЬ")
    else:
        flash('Вы не имеете достаточных прав для перехода на данную страницу')
        return redirect('/')
    
    
@app.route('/createOrder',  methods = ["GET", "POST"])
def createOrder():
    if current_user.is_authenticated and db.getRoleUser(current_user.get_id())[0] == 'ADMIN':
        if request.method == 'POST':
            db.createOrder()
            #СДЕЛАТЬ СТРАНИЦУ И ЗАПРОС ДЛЯ ДОБАВЛЕНИЯ ЗАКАЗА
            flash('Заказ создан')
            return redirect('/orders')
        return render_template('createOrder.html', title = "СОЗДАТЬ ЗАКАЗ")
    else:
        flash('Вы не имеете достаточных прав для перехода на данную страницу')
        return redirect('/')    
    
app.run(debug=True)