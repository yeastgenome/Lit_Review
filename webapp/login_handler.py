"""

This is a small application that provides a login page for curators to view/edit the
information in Oracle database. This application is using Flask-Login package (created
by Matthew Frazier, MIT) for handling the login sessions and everything. 

"""
from flask_login import LoginManager, login_user, logout_user, confirm_login, \
    current_user
from webapp.config import Anonymous, USER_NAMES, USERS

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

#Exceptions
class LoginException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class NotOnListException(LoginException):
    def __init__(self):
        super(LoginException, self).__init__('You are not allowed to use this interface. Contact sgd-programmers to add your name to the list.')
        
class BadUsernamePasswordException(LoginException):
    def __init__(self):
        super(LoginException, self).__init__('You typed in an invalid username/password')
        
class LogoutException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
def setup_app(app):
    login_manager.setup_app(app)
        

def login_lit_review_user(username, password, model, remember):
    import os

    try:
        model.connect(username, password)
    except Exception as e:
        path = os.getenv('LD_LIBRARY_PATH')
        if path is None:
            output = ". LD_LIBRARY_PATH has not been set."
        else:
            output = ". LD_LIBRARY_PATH = " + path
        raise LoginException(str(e) + output)
    
    if not model.is_connected():
        raise BadUsernamePasswordException()
    
    if username in USER_NAMES:
        if login_user(USER_NAMES[username], remember=remember):
            return True
        else:
            raise LoginException('Sorry, but Flask-login could not log you in.')
    else:
        raise NotOnListException()

@login_manager.user_loader
def load_lit_review_user(user_id):
    return USERS.get(int(user_id))

def confirm_login_lit_review_user():
    confirm_login()
    return 'Reauthenticated'
    
def logout_lit_review_user():
    if logout_user():
        return True
    else:
        raise LogoutException('Sorry, but Flask-login could not log you out.')

def get_current_user():
    return current_user




    




