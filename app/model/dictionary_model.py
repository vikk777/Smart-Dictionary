from app import db


class DictionaryModel(db.Model):
    __tablename__ = 'dictionaries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE'),
                        nullable=False)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(32))
    words = db.relationship('WordModel', backref='dictionary',
                            lazy='dynamic')
