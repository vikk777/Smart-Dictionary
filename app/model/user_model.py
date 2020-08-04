from app import db
from flask_login import UserMixin

mistakesTable = db.Table(
    'mistakes',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('word_id',
              db.Integer,
              db.ForeignKey('words.id', ondelete='CASCADE')))


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    dictionaries = db.relationship(
        'DictionaryModel',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic')
    mistakes = db.relationship(
        'WordModel',
        secondary=mistakesTable,
        lazy='dynamic')
    # test = db.relationship(
    #     'TestModel',
    #     backref='user',
    #     cascade='all, delete-orphan',
    #     lazy='dynamic')
