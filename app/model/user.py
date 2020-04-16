from ..database import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(User, UserMixin):
    def __init__(self):
        pass

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
