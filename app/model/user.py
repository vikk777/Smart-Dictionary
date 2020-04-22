from app import db, loginManager
from .user_model import UserModel
from .dictionary import Dictionary
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user


# class User(UserModel, UserMixin):
class User():
    def __init__(self):
        self._dictionary = Dictionary()

    @loginManager.user_loader
    def load(userId):
        return UserModel.query.get(int(userId))

    def get(self, name):
        return UserModel.query.filter_by(name=name).first()

    def register(self, name, password):
        if UserModel.query.filter_by(name=name).count() > 0:
            return False

        user = UserModel(name=name, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return True

    def login(self, name, password, remember):
        user = self.get(name)
        if user and check_password_hash(user.password, password):
            return login_user(user)
        else:
            return False

    def addMistake(self, userId, mistake):
        user = User.load(userId)
        word = self._dictionary.word(user, mistake)

        if word:
            user.mistakes.append(word)
            db.session.commit()
            return True
        else:
            return False

    def haveMistake(self, userId, mistake):
        user = User.load(userId)
        word = self._dictionary.word(user, mistake)
        return True if word in self.mistakes(userId) else False

    def removeMistake(self, userId, mistake):
        user = User.load(userId)
        word = self._dictionary.word(user, mistake)

        if word:
            user.mistakes.remove(word)
            db.session.commit()
            return True
        else:
            return False

    def mistakes(self, userId):
        user = User.load(userId)
        return user.mistakes.all() if user else None
