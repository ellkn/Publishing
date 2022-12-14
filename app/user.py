from flask_login import UserMixin
import db as db
# from time import time
# from routes import app
# import jwt

class User:
    def __init__(self, id, lastname, firstname, email, password, role):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.password = password
        self.role = role
        
        
class Role:
    def __init__(self, role):
        self.id = id
        self.role = role


class UserLogin(UserMixin):
       
    def dbi(self, user_id):
        self.__user = db.getUserById(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self
     
    def is_authenticated():
        return True
    
    def is_active():
        return True
    
    def is_anonymous():
        return False
    
    def get_id(self):
        if self.__user:
            return self.__user['id']
        else:
            return False
        
    def get_role(self):
        if self.__user:
            return self.__user['role']
        else:
            return False
    
    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.id, 'exp': time() + expires_in},
    #         app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        
    # @staticmethod
    # def verify_reset_password_token(token):
    #     try:
    #         id = jwt.decode(token, app.config['SECRET_KEY'],
    #                         algorithms=['HS256'])['reset_password']
    #     except:
    #         return
    #     return UserLogin.get_id()