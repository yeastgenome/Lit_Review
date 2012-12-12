from flask_login import UserMixin, AnonymousUser
                             
HOST = '0.0.0.0'
PORT = 5000
SECRET_KEY = "SECRET_KEY_HERE"

class User(UserMixin):
    def __init__(self, name, user_id, active=True):
        self.name = name
        self.id = user_id
        self.active = active

    def is_active(self):
        return self.active
    
    def __repr__(self):
        data = self.id, self.name, self.active
        return 'User(id=%s, name=%s, active=%s)' % data

class Anonymous(AnonymousUser):
    name = u"Anonymous"

    
usernames = {'maria', 'julie', 'kpaskov', 'dwight', 'fisk', 'rama', 'stacia', 'nash', 'marek'}
keys = range(1, len(usernames))
values = map(lambda (i, username): User(username, i+1), enumerate(usernames))

USERS = dict(zip(keys, values))
USERS[len(usernames)+1] = User('guest', len(usernames)+1, False)

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())
