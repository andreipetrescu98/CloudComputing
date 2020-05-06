

class User:

    def __init__(self, username, email, id=None, category="standard"):
        self._username = username
        self._email = email
        self._id = id
        self._category = category

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    def to_dict(self):
        return {k[1:]: v for k, v in vars(self).items()}

    @staticmethod
    def from_dict(user_dict: dict):
        return User(id=user_dict['id'],
                    username=user_dict['username'],
                    email=user_dict['username'],
                    category=user_dict['category'])
