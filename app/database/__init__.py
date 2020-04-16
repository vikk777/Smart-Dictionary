from app import db


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))
    original = db.Column(db.String(32))
    translate = db.Column(db.String(32))
    transcription = db.Column(db.String(32))
    updateTime = db.Column(db.Float)


class Dictionary(db.Model):
    __tablename__ = 'dictionaries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(24))
    description = db.Column(db.String(32))
    words = db.relationship('Word', backref='dictionary', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    password = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary',
                                   backref='user',
                                   lazy='dynamic')
    mistakes = db.relationship('Word',
                               secondary='mistakes',
                               # backref='user',
                               lazy='dynamic')


# class Mistakes(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
mistakes = db.Table(
    'mistakes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('word_id', db.Integer, db.ForeignKey('words.id')))


# class Users_Dictionaries(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     dictionary_id = db.Column(db.Integer)
