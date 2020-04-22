from app import db


class WordModel(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    dictionary_id = db.Column(db.Integer,
                              db.ForeignKey('dictionaries.id',
                                            ondelete='CASCADE'),
                              nullable=False)
    original = db.Column(db.String(32), nullable=False)
    translate = db.Column(db.String(32), nullable=False)
    transcription = db.Column(db.String(32))
    updateTime = db.Column(db.Float, nullable=False)
