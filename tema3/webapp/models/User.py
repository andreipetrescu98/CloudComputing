from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, email):
        self.id = id
        self._username = username
        self._email = email

    def getId(self): return self.id

    def getUsername(self): return self._username

    def getEmail(self): return self._email

    @staticmethod
    def from_dict(source):
        return User(id=source['id'], username=source['username'], email=source['email'])

    def to_dict(self):
        user_dict = {
            u'username': self._username,
            u'email': self._email
        }
        return user_dict
