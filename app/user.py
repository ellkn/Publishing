from flask_login import UserMixin
import db as db

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