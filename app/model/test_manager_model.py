from app import db


class TestModel(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE'),
                        nullable=False)
    question = db.Column(db.String(32), nullable=False)
    answer = db.Column(db.String(32), nullable=False)
    user_answer = db.Column(db.String(32), nullable=True)
    passed = db.Column(db.Boolean, default=False)
